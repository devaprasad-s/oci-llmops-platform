# **Kubernetes Manifest Doctor: Edge LLMOps Platform**

An enterprise-grade, zero-touch GitOps platform hosting an AI-powered API that automatically diagnoses and corrects Kubernetes YAML manifests.

This project demonstrates the deployment of a Retrieval-Augmented Generation (RAG) LLM application on resource-constrained Edge hardware, fully orchestrated via Kubernetes and automated via Jenkins CI/CD.

## **Architecture Overview**

The infrastructure is provisioned on Oracle Cloud Infrastructure (OCI) using a mixed-architecture node topology to optimize compute and memory constraints.

* **Control Plane (AMD Node):** Resource-constrained node (1 GB RAM) running Jenkins for CI/CD orchestration and webhook interception.  
* **Edge/AI Node (ARM Ampere A1):** Native arm64 compute node running K3s, a bare-metal Ollama daemon, and the containerized FastAPI inference payload.

### **Tech Stack**

* **AI/ML Engine:** Ollama (serving quantized Phi-3 Mini natively on bare metal), LangChain, ChromaDB, HuggingFace Embeddings.  
* **Application Layer:** Python, FastAPI, Docker.  
* **Orchestration & Routing:** K3s, containerd, Traefik Ingress.  
* **CI/CD GitOps:** GitHub Webhooks, Jenkins, Declarative Groovy Pipelines, SSH Remote Execution.

## **The GitOps Pipeline**

To eliminate the heavy performance penalty of cross-compiling Machine Learning containers (PyTorch/LangChain) through QEMU emulators on resource-constrained hardware, this platform utilizes a distributed master-worker CI/CD topology.

1. **Trigger:** Code pushed to the repository triggers a GitHub Webhook.  
2. **Orchestrate:** The Jenkins control plane (AMD) intercepts the payload and establishes a secure SSH tunnel to the target production node (ARM).  
3. **Native Build:** Jenkins delegates the docker build natively to the ARM node, reducing compilation times from 77 minutes to 2 minutes.  
4. **Inject:** The image is exported to a tarball and injected directly into the K3s containerd runtime, bypassing public registry bandwidth overhead.  
5. **Rollout:** Jenkins triggers a kubectl rollout restart, deploying the new application state via Traefik Ingress with zero downtime.

## **API Usage**

The application utilizes an ephemeral Vector Database to ground the LLM's responses against strict, predefined Kubernetes structural policies, preventing AI hallucination. The endpoint is exposed to the public internet via a Traefik Ingress Controller.

**Endpoint:** POST http://\<NODE\_PUBLIC\_IP\>/diagnose/yaml

**Request:**

```
curl \-X POST http://\<NODE\_PUBLIC\_IP\>/diagnose/yaml \\  
\-H "Content-Type: application/json" \\  
\-d '{  
  "yaml\_content": "apiVersion: apps/v1\\nkind: Deployment\\nmetadata:\\n  name: frontend\\nspec:\\n  replicas: 3\\n  template:\\n    metadata:\\n      labels:\\n        app: frontend\\n    spec:\\n      containers:\\n      \- name: nginx\\n        image: nginx:latest"  
}'
```

**Response (Generated via local Phi-3 contextually grounded by RAG):**

```
{  
  "diagnosis": "ERROR: The Deployment manifest lacks a 'selector' block that matches the template labels.\\n\\nCORRECTED YAML:\\n\`\`\`yaml\\napiVersion: apps/v1\\nkind: Deployment\\nmetadata:\\n  name: frontend\\nspec:\\n  replicas: 3\\n  selector:\\n    matchLabels:\\n      app: frontend\\n  template:\\n    metadata:\\n      labels:\\n        app: frontend\\n    spec:\\n      containers:\\n      \- name: nginx\\n        image: nginx:latest\\n\`\`\`",  
  "response\_time\_seconds": 46.358  
}
```

## **Key Engineering Challenges Solved**

* **The Localhost Container Trap:** Remapped isolated container runtimes to route through Flannel bridge gateways (10.42.0.1) to successfully connect isolated Kubernetes pods to bare-metal systemd AI services.  
* **Ingress Port Alignment:** Configured Traefik Ingress resources to successfully route standard HTTP traffic (Port 80\) across the Kubernetes abstraction layer directly to the internal Uvicorn ASGI server (Port 8000).  
* **Cloud Perimeter Security:** Navigated Dual-Firewall routing (Linux iptables \+ OCI VCN Security Lists) to safely expose automated webhooks to GitHub and Traefik Ingress controllers to the public internet.  
* **Remote Native Compilation:** Bypassed heavy QEMU hardware emulation penalties by designing a Jenkins pipeline that delegates ML dependency compilation to native ARM processors via secure SSH tunneling.