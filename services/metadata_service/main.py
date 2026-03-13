from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/radiology")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Radiology Metadata Service")

# Pydantic Schemas
class PatientCreate(BaseModel):
    patient_id: str
    name: str
    birth_date: Optional[datetime] = None
    sex: str

class StudyCreate(BaseModel):
    study_instance_uid: str
    study_date: Optional[datetime] = None
    study_description: str
    accession_number: str
    patient_id: str # The internal patient_id string

class SeriesCreate(BaseModel):
    series_instance_uid: str
    modality: str
    series_description: str
    series_number: int
    study_instance_uid: str

class InstanceCreate(BaseModel):
    sop_instance_uid: str
    sop_class_uid: str
    instance_number: int
    file_path: str
    series_instance_uid: str
    metadata_json: dict

class AnnotationCreate(BaseModel):
    sop_instance_uid: str
    label: str
    data: dict

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient.patient_id).first()
    if not db_patient:
        db_patient = models.Patient(**patient.dict())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
    return db_patient

@app.post("/studies")
def create_study(study: StudyCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == study.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient not found")

    db_study = db.query(models.Study).filter(models.Study.study_instance_uid == study.study_instance_uid).first()
    if not db_study:
        study_data = study.dict()
        study_data['patient_id'] = patient.id
        db_study = models.Study(**study_data)
        db.add(db_study)
        db.commit()
        db.refresh(db_study)
    return db_study

@app.post("/series")
def create_series(series: SeriesCreate, db: Session = Depends(get_db)):
    study = db.query(models.Study).filter(models.Study.study_instance_uid == series.study_instance_uid).first()
    if not study:
        raise HTTPException(status_code=400, detail="Study not found")

    db_series = db.query(models.Series).filter(models.Series.series_instance_uid == series.series_instance_uid).first()
    if not db_series:
        series_data = series.dict()
        series_data.pop('study_instance_uid')
        series_data['study_id'] = study.id
        db_series = models.Series(**series_data)
        db.add(db_series)
        db.commit()
        db.refresh(db_series)
    return db_series

@app.post("/instances")
def create_instance(instance: InstanceCreate, db: Session = Depends(get_db)):
    series = db.query(models.Series).filter(models.Series.series_instance_uid == instance.series_instance_uid).first()
    if not series:
        raise HTTPException(status_code=400, detail="Series not found")

    db_instance = db.query(models.Instance).filter(models.Instance.sop_instance_uid == instance.sop_instance_uid).first()
    if not db_instance:
        instance_data = instance.dict()
        instance_data.pop('series_instance_uid')
        instance_data['series_id'] = series.id
        db_instance = models.Instance(**instance_data)
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    return db_instance

@app.get("/patients")
def get_patients(patient_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Patient)
    if patient_id:
        query = query.filter(models.Patient.patient_id == patient_id)
    return query.all()

@app.get("/studies")
def get_studies(patient_id: Optional[str] = None, study_instance_uid: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Study).join(models.Patient)
    if patient_id:
        query = query.filter(models.Patient.patient_id == patient_id)
    if study_instance_uid:
        query = query.filter(models.Study.study_instance_uid == study_instance_uid)
    return query.all()

@app.get("/instances/{sop_instance_uid}")
def get_instance(sop_instance_uid: str, db: Session = Depends(get_db)):
    instance = db.query(models.Instance).filter(models.Instance.sop_instance_uid == sop_instance_uid).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance

@app.post("/annotations")
def create_annotation(annotation: AnnotationCreate, db: Session = Depends(get_db)):
    db_annotation = models.Annotation(**annotation.dict())
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

@app.get("/annotations/{sop_instance_uid}")
def get_annotations(sop_instance_uid: str, db: Session = Depends(get_db)):
    return db.query(models.Annotation).filter(models.Annotation.sop_instance_uid == sop_instance_uid).all()
