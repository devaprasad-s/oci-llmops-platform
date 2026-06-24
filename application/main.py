from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import ManifestDoctorRAG

app = FastAPI(title="K8s Manifest Doctor API")

# Instantiate the engine globally so it loads models on startup
doctor = ManifestDoctorRAG()
doctor.load_knowledge_base()

class YamlRequest(BaseModel):
    yaml_content: str

@app.post("/diagnose/yaml")
async def diagnose_yaml(request: YamlRequest):
    # Call your doctor.diagnose_manifest() method here
    # Return the AI's response in a JSON dictionary
    pass