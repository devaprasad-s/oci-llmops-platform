from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate

class ManifestDoctorRAG:
    def __init__(self):
        # 1. Initialize the HuggingFaceEmbeddings (use "all-MiniLM-L6-v2")
        # 2. Initialize Chroma in ephemeral (in-memory) mode
        # 3. Initialize the Ollama LLM pointing to model="phi3"
        pass

    def load_knowledge_base(self):
        # 1. Create a list of hardcoded K8s rules (e.g., "Rule 1: Always use memory limits.")
        # 2. Convert them into LangChain Document objects
        # 3. Add them to your Chroma vector store
        pass

    def diagnose_manifest(self, broken_yaml: str) -> str:
        # 1. Search Chroma for the top 2 rules related to the broken_yaml
        # 2. Construct a PromptTemplate instructing Phi-3 to act as an SRE, 
        #    giving it the rules and the broken_yaml.
        # 3. Pass the prompt to Ollama and return the string response.
        pass