"""
File: server.py
Description: This file contains the server for the agent.
"""

# imports
from fastapi import FastAPI
from api.v1.endpoints import invoke

from logging import getLogger, INFO

# globals
logger = getLogger("Agent Server")
logger.setLevel(INFO)

app = FastAPI(title="Agent Server")

# Add routes
app.include_router(invoke.router)

# Run the app
if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=8000, workers=1)
    except Exception as e:
        logger.error(f"Failed to run agent server: {str(e)[:500]}")
        raise e
