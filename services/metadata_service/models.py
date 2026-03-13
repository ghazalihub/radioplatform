from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True, nullable=False) # DICOM PatientID
    name = Column(String)
    birth_date = Column(DateTime)
    sex = Column(String(1))
    studies = relationship("Study", back_populates="patient")

class Study(Base):
    __tablename__ = "studies"
    id = Column(Integer, primary_key=True, index=True)
    study_instance_uid = Column(String, unique=True, index=True, nullable=False)
    study_date = Column(DateTime)
    study_description = Column(String)
    accession_number = Column(String, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="studies")
    series = relationship("Series", back_populates="study")

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    series_instance_uid = Column(String, unique=True, index=True, nullable=False)
    modality = Column(String, index=True)
    series_description = Column(String)
    series_number = Column(Integer)
    study_id = Column(Integer, ForeignKey("studies.id"))
    study = relationship("Study", back_populates="series")
    instances = relationship("Instance", back_populates="series")

class Instance(Base):
    __tablename__ = "instances"
    id = Column(Integer, primary_key=True, index=True)
    sop_instance_uid = Column(String, unique=True, index=True, nullable=False)
    sop_class_uid = Column(String)
    instance_number = Column(Integer)
    file_path = Column(String) # Path in object storage
    series_id = Column(Integer, ForeignKey("series.id"))
    series = relationship("Series", back_populates="instances")
    metadata_json = Column(JSON) # Store extra DICOM tags

class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True, index=True)
    sop_instance_uid = Column(String, index=True)
    label = Column(String)
    data = Column(JSON) # e.g. bounding box coordinates
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String)
    action = Column(String)
    resource = Column(String)
    details = Column(Text)
