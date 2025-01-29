"""
File: invoke.py
Description: The invoke endpoint for the agent.
"""

# imports
from fastapi import APIRouter
from pydantic import BaseModel

from api.v1.dependencies.agent import Agent

# initialize router
router = APIRouter(prefix="/invoke", tags=["invoke"])

class InvokeAgentRequest(BaseModel):
    """Request to invoke the agent."""
    task: str
    context: str

@router.post("/")
async def invoke(request: InvokeAgentRequest):
    """Invoke the agent."""

    agent = Agent(task=request.task)

    # run the agent
    response = agent.invoke(context=request.context)

    return {"message": response}

