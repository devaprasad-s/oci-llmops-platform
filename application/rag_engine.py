from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

class ManifestDoctorRAG:
    def __init__(self):
        # 1. Load the small, fast CPU-friendly embedding model
        print("Initializing Embedding Model (MiniLM)...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Spin up an in-memory ChromaDB instance
        print("Initializing Ephemeral ChromaDB...")
        self.vectorstore = Chroma(embedding_function=self.embeddings)
        
        # 3. Connect to the local Ollama instance running Phi-3
        # Added temperature=0 to make the model deterministic and stop it from rambling
        print("Connecting to local Ollama (Phi-3)...")
        self.llm = OllamaLLM(model="phi3", temperature=0)

    def load_knowledge_base(self):
        print("Loading internal policies into Vector Database...")
        # A list of strict rules we want our AI to enforce
        rules = [
            "Rule 1: All Kubernetes apps/v1 Deployments MUST have a 'selector' block that matches the template labels.",
            "Rule 2: All containers should have memory and cpu limits defined to prevent OOM errors.",
            "Rule 3: Ingress resources must specify an ingressClassName, typically 'nginx'.",
            "Rule 4: Services must define a targetPort if it differs from the exposed port."
        ]
        
        # Convert the strings into LangChain Document objects
        docs = [Document(page_content=rule) for rule in rules]
        
        # Embed and store them in Chroma
        self.vectorstore.add_documents(docs)
        print("Knowledge Base successfully loaded!")

    def diagnose_manifest(self, broken_yaml: str) -> str:
        # 1. Retrieve: Find the 2 rules that are most mathematically similar to the broken YAML
        relevant_docs = self.vectorstore.similarity_search(broken_yaml, k=2)
        
        # Extract just the text from the retrieved documents
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # 2. Augment: Construct the prompt with strict structural constraints
        prompt_template = """
        You are a strict Kubernetes Platform Engineer. 
        Analyze the broken Kubernetes YAML manifest using ONLY the provided Internal Policies.
        
        Internal Policies:
        {context}
        
        Broken YAML:
        {yaml}
        
        You must reply using EXACTLY this format and nothing else. Stop generating after the YAML:
        
        ERROR: 
        [1 sentence explanation]
        
        CORRECTED YAML:
        ```yaml
        [Corrected YAML here]
        ```
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "yaml"]
        )
        formatted_prompt = prompt.format(context=context, yaml=broken_yaml)
        
        # 3. Generate: Send it to Phi-3 and get the answer
        print("Sending prompt to Phi-3...")
        response = self.llm.invoke(formatted_prompt)
        
        return response