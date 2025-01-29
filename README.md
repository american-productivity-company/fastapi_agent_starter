# Agent Service

## Quickstart

To get started, ensure that:

 - Docker CLI Tools are installed. This can be done by [installing Docker Desktop](https://docs.docker.com/get-started/docker_cheatsheet.pdf) or just the Docker CLI tools.
 - You have a [Pinecone](https://www.pinecone.io/) account and have setup a hybrid-search index with dimension 1536. [Here](https://www.pinecone.io/learn/hybrid-search-intro/) is a helpful article if you are new to hybrid search indexes.
 - You have  Supabase account and have setup the appropriate tables.

Next, you'll need to create the environment variables file, `development.env` in `synthetic_manger/server/`. To get started, create a copy of or rename `synthetic_manager/server/.env.example` to `synthetic_manager/server/development.env` and uncomment all variables that begin with `# -> `. Add the appropriate API keys for each environment variables. For example, `# -> OPENAI_API_KEY=''` should become `OPENAI_API_KEY='your_key'`.

Finally, from the root directory, use the Docker Compose file to build and start the Docker Containers.

```bash
>>> docker compose up
```

## Invoke the agent via curl

```bash
curl -X POST http://localhost:8000/invoke -H "Content-Type: application/json" -d '{"task": "Write a short story about a cat", "context": "The cat is a fluffy orange cat with a white belly and a black stripe on its face."}'
```

## Invoke the agent via Python

```python
import requests

response = requests.post("http://localhost:8000/invoke", json={"task": "Write a short story about a cat", "context": "The cat is a fluffy orange cat with a white belly and a black stripe on its face."})
print(response.json())
```

## Invoke the agent via Browser

Open the browser and navigate to http://localhost:8000/docs.
