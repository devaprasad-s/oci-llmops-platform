from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import ManifestDoctorRAG

app = FastAPI(title="K8s Manifest Doctor API")

print("Starting up the K8s Manifest Doctor...")
doctor = ManifestDoctorRAG()
doctor.load_knowledge_base()

class YamlRequest(BaseModel):
    yaml_content: str

@app.post("/diagnose/yaml")
async def diagnose_yaml(request: YamlRequest):
    ai_response = doctor.diagnose_manifest(request.yaml_content)
    return {"diagnosis": ai_response}