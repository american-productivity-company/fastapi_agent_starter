"""
File: agent.py
Description: This file contains the agent.
"""

# imports
from pydantic import BaseModel, Field
from typing import Dict, Any, Literal

import operator
from typing import List, Dict, Any, Literal, TypedDict, Annotated, Optional
from uuid import UUID

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import Tool

from langgraph.graph import StateGraph, END, START

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from datetime import datetime, timezone

from .prompts import system_message
from .tools import BasicTools
from .utils import create_tool_node_with_fallback

from logging import getLogger, INFO
logger = getLogger("Agent Logger")
logger.setLevel(INFO)

class State(TypedDict):
    """State for the agent's execution"""
    messages: Annotated[List[BaseMessage], operator.add]

class Agent(BaseModel):
    """An agent schema."""

    name: str = "Agent"
    version: str = "1.0.0"

    task: str = Field(description="The task to perform")

    runnable: Runnable = None
    tools: List[Tool] = []

    max_iterations: int = 10
    max_llm_retries: int = 1

    class Config:
        arbitrary_types_allowed = True

    def __init__(
            self,
            **data
    ) -> None:
        super().__init__(**data)

        # Initialize the tools
        self.tools = (
            BasicTools().tools
        )

        # Load the Config
        self.load_config()

        # Load the runnable
        self.load_runnable()

    def load_config(self) -> None:
        """Loads the config for the agent."""
        
        # OpenAI
        self._llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.5
        ).bind_tools(self.tools)

        # Anthropic
        # self._llm = ChatAnthropic(
        #     model="claude-3-5-sonnet-20240620",
        #     temperature=0.5
        # ).bind_tools(self.tools)

    def load_runnable(self) -> None:
        """Loads the runnable for the agent."""
        
        workflow = StateGraph(State)

        # Add the core nodes
        workflow.add_node("llm_node", self.llm_node)
        workflow.add_node("tool_executor", create_tool_node_with_fallback(self.tools))

        # Add edges
        workflow.add_edge(START, "llm_node")
        workflow.add_edge("tool_executor", "llm_node")

        # Add conditional routing based on tool calls and suspension
        workflow.add_conditional_edges(
            "llm_node",
            self.route_tool_calls,
            {
                "continue": "tool_executor",
                "end": END
            }
        )

        self.runnable = workflow.compile()

    def invoke(self, context: str) -> None:
        """Invokes the agent."""
        config = RunnableConfig(recursion_limit=self.max_iterations)
        state = State(
            messages=[
                SystemMessage(content=system_message), 
                HumanMessage(content=f"The task is: {self.task}"), 
                HumanMessage(content=context)
            ]
        )
        state = self.runnable.invoke(state, config=config)
        return state["messages"][-1].content

    """
    Core Nodes
    """

    def llm_node(self, state: State) -> State:
        """LLM node"""

        # Get the existing messages
        messages = state["messages"]

        if len(messages) == 0:
            logger.error("No messages to process")
            return {}
        
        messages.append(HumanMessage(content=f"The current time is {datetime.now(timezone.utc)} UTC."))
        
        for i in range(self.max_llm_retries):
            try:
                result = self._llm.invoke(messages)
                break
            except Exception as e:
                logger.warning(
                    msg=f"LLM call failed: {repr(e)}"
                )
                result = AIMessage(content="FAILED LLM RETRIEVAL")

        return {
            "messages": [result]
        }

    """
    Conditional Routing
    """

    def route_tool_calls(self, state: State) -> Literal["continue", "end"]:
        """Routes tool calls"""
        if state["messages"][-1].content == "FAILED LLM RETRIEVAL":
            return "end"
        if type(state["messages"][-1]) == AIMessage:
            if state["messages"][-1].tool_calls:
                return "continue"
            else:
                return "end"
        return "end"