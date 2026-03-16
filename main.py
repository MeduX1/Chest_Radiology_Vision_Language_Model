from fastapi import FastAPI, File,  UploadFile, Form, Depends
from worker import celery_app,process_medical_image
from celery.result import AsyncResult
import shutil
import os
from database import SessionLocal, RadiologyRecord
from sqlalchemy.orm import Session


app = FastAPI(title = "Mediscan Async Radiology API")
os.makedirs('Uploads',exist_ok=True)

@app.post('/upload-scan')
def upload_scan(patient_id:str = Form(...), file: UploadFile = File(...)):
    file_location = f"Uploads/{file.filename}"
    with open(file_location , "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)

    task = process_medical_image.delay(patient_id, file.filename)
    return {
        "message": "Image received. Multimodal AI processing initiated.",
        "task": task.id,
        "patient_id":patient_id,
    }

@app.get("task_result/{task_id}")
def get_scan_result(task_id:str):
    task_result = AsyncResult(task_id, app = celery_app )
    if task_result.state == "SUCCESSFUL":
        return {
            "task_id": task_id,
            "task_status": task_result.state,
            "task_result": task_result.result  
        }
    else:
        return {
            "task_id": task_id,
            "task_status": task_result.state,
            "task_result": "No result yet, AI is still Analyzing"
        }
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
     db.close()

@app.get("/get_patient_history/{patient_id}")
def get_patient_record(patient_id: str, db: Session = Depends(get_db)):
    records = db.query(RadiologyRecord).filter(RadiologyRecord.patient_id == patient_id).all()
    if not records:
        return {"message": f"No radiological history found for {patient_id}."}
    
    return {"patient_id": patient_id, "total_scans": len(records), "history": records}
    





