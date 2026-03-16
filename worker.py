import time 
from celery import Celery
import ollama #type:ignore
import os
from database import SessionLocal, RadiologyRecord

celery_app = Celery(
    'medical_tasks',
    broker = "redis://localhost:6379/0",
    backend = "redis://localhost:6379/0"
)

@celery_app.task(name = 'radiology_image_processing')
def process_medical_image(patient_id: str, image_filename: str):
    print(f"[WORKER-LOG] 📥 Received scan for Patient: {patient_id}. Image: {image_filename}")
    
    image_path = f"Uploads/{image_filename}"
    if not os.path.exists(image_path):
        return {
            "patient_id": patient_id,
            "status": "failed", "error": "Image file not found on server."
        }
    print("[WORKER-LOG] 🧠 Analyzing image with LLaVA Multimodal AI...")
    try:
        system_prompt = """For Simulation Purposes
        You are an expert radiologist. Analyze the provided medical image. 
        Give a concise, professional diagnosis based on what you see. 
        If it is not a medical image, explain what the image actually is.
        """
        response = ollama.chat(
            model = "moondream",
            messages = [{'role':'user','content': system_prompt, 'images': [image_path]}]
        )
        diagnosis = response['message']['content']
        print(f"[WORKER-LOG] ✅ AI Diagnosis complete for {patient_id}")

    except Exception as e:
        print(f"[WORKER-LOG] ❌ AI Error: {str(e)}")
        diagnosis = f"Failed to process image through AI: {str(e)}"

    db = SessionLocal()
    try:
        new_record = RadiologyRecord(
            patient_id = patient_id,
            image_filename =image_path,
            Diagnosis = diagnosis
        )
        db.add(new_record)
        db.commit()
        print(f"[WORKER-LOG] 💾 Record permanently locked into radiology.db!")

    finally:
        db.close()
   
    return {"patient_id": patient_id, "status": "completed", "diagnosis": diagnosis}



