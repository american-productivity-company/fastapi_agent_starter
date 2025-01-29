"""
File: tools.py
Description: Tools
"""

# imports
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from datetime import datetime, timezone

from langchain_core.tools import Tool, tool

class BasicTools(BaseModel):
    """Basic tools"""

    tools: List[Tool] = Field(default_factory=list, description="The tools")

    def __init__(self, **data) -> None:
        """Initializes the system tools."""
        super().__init__(**data)
        self.tools = [
            self.get_hello_world_tool()
        ]
    
    def get_hello_world_tool(self) -> Tool:
        """Returns a hello world message."""

        @tool
        def hello_world() -> str:
            """Returns a hello world message to the agent."""
            return "Hello, world!"
            
        return hello_world