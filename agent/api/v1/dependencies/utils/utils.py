"""
File: utils.py
Description: This file contains utility functions for Tools.
"""

# imports
from langchain_core.messages import ToolMessage, HumanMessage
from langchain_core.runnables import RunnableLambda, Runnable, RunnableConfig
from langgraph.prebuilt import ToolNode

from typing import Dict, Any

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )