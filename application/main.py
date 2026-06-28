from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import ManifestDoctorRAG
import time


app = FastAPI(title="K8s Manifest Doctor API")

print("Starting up the K8s Manifest Doctor...")
doctor = ManifestDoctorRAG()
doctor.load_knowledge_base()

class YamlRequest(BaseModel):
    yaml_content: str

@app.post("/diagnose/yaml")
async def diagnose_yaml(request: YamlRequest):
    start_time = time.perf_counter()
    ai_response = doctor.diagnose_manifest(request.yaml_content)
    end_time = time.perf_counter()
    elapsed = round(end_time - start_time, 3)
    return {
        "diagnosis": ai_response,
        "response_time_seconds": elapsed
    }