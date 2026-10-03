# Container deployment notes

Build and validate the image locally before publishing it to Azure Container Registry. Create an Azure Container App with HTTP ingress on port 8000. Store Azure OpenAI credentials as managed secrets and map them to the environment variables in `.env.example`. Mount persistent storage or migrate ChromaDB to a managed vector database for multi-replica deployments. Configure health probes against `/health`.
