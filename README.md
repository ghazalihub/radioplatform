# Advanced Radiology Imaging Platform (Next-Gen PACS + AI Research System)

## Overview
This platform is a production-grade, hospital-scale radiology imaging system that securely ingests, stores, indexes, processes, and distributes medical imaging studies across departments. It functions as a modern replacement for traditional PACS while acting as a research data lake for AI development.

## Core Capabilities
- **Native DICOM Support**: C-STORE, C-FIND, C-MOVE, C-GET, and DICOMweb (QIDO-RS, WADO-RS, STOW-RS).
- **Advanced 2D/3D Viewer**: Window/Level, Pan, Zoom, MPR, and GPU-accelerated rendering.
- **AI-Powered Pipeline**: Automated fracture and lung nodule detection with model registry and worker queue.
- **Hospital Integration**: Native HL7 and FHIR support for EMR/RIS synchronization.
- **Security & Compliance**: RBAC, JWT/OAuth2, audit logging, and HIPAA-ready data anonymization.

## Architecture & Services
The system is composed of 13 modular microservices:

| Service | Port | Description |
| --- | --- | --- |
| `auth_service` | 8001 | Handles authentication, RBAC, and user management. |
| `metadata_service` | 8002 | Manages patient/study/series/instance relational data (PostgreSQL). |
| `storage_service` | 8003 | Handles raw DICOM storage with encryption at rest. |
| `dicom_ingestion`| 11112| C-STORE SCP for medical device connections. |
| `dicomweb_service`| 8005 | Implements QIDO-RS, WADO-RS, and STOW-RS standards. |
| `ai_service` | 8007 | Manages AI processing tasks (Celery + Redis + GPU-ready). |
| `reporting_service`| 8004 | Structured reporting, voice dictation, and PDF export. |
| `analytics_service`| 8009 | Departmental performance and modality usage metrics. |
| `education_service`| 8008 | Case library, teaching datasets, and resident quizzes. |
| `integration_service`| 8010 | Hospital-level integration (HL7 v2.x and FHIR R4). |
| `audit_service` | 8006 | Centralized log collection and compliance auditing. |
| `collaboration_service`| 8011 | Real-time WebSocket-based synchronized viewing. |
| `compliance_service`| 8012 | HIPAA/GDPR consent and data retention management. |

## Frontend Applications
- **Web Viewer (`apps/web_viewer`)**: Built with React and Cornerstone3D.
- **Workstation (`apps/desktop_workstation`)**: Electron wrapper for diagnostic use.

## Deployment & Setup

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend build)
- Python 3.12 (for service development)

### Running with Docker
```bash
docker compose up -d --build
```

### Manual Service Start (Example: Auth Service)
```bash
cd services/auth_service
pip install -r requirements.txt
export SECRET_KEY=mysecret
python main.py
```

### Manual Frontend Start
```bash
cd apps/web_viewer
npm install
npm start
```

## API Specifications
All services provide a Swagger/OpenAPI UI at `/docs`.
- **Auth**: `/token` (POST)
- **Metadata**: `/studies` (GET), `/instances` (POST)
- **DICOMweb**: `/rs/studies` (GET/QIDO), `/rs/studies/{uid}` (GET/WADO)

## Data Schema
The metadata engine uses a hierarchical schema:
- **Patients**: 1:N with Studies.
- **Studies**: 1:N with Series.
- **Series**: 1:N with Instances.
- **Instances**: Stores SOP Instance UIDs and file paths to raw DICOM.
- **Annotations**: Linked to Instances for AI results and radiologist measurements.

## AI Research Dataset Builder
Anonymized datasets can be exported from the metadata service. Supported formats include:
- **DICOM**: Original but de-identified.
- **NIfTI**: For research consumption.
- **PNG Stacks**: For quick manual labeling.

## Security Controls
- **Centralized Authentication**: JWT/OAuth2 enforced on all sensitive endpoints.
- **Internal Service Auth**: Microservices use service-to-service tokens for internal communication.
- **RBAC**: Fine-grained access control for Radiologist, Referring Physician, Resident, and Admin roles.
- **TLS**: Required for all communication in production environments.
- **Encryption**: AES-256 for data at rest (Storage Service).
