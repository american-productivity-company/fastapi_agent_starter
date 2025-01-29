# Agent Service

## Run the service

```bash
docker compose up --build
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
