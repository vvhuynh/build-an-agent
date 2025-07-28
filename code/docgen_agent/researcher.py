import json
import logging
import os
from typing import Annotated, Any, Sequence
from dotenv import load_dotenv

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import tools
from .prompts import research_prompt

# Load environment variables
load_dotenv("../../variables.env")

# Set the API key directly in environment
api_key = os.getenv("NVIDIA_API_KEY")
if api_key:
    os.environ["NVIDIA_API_KEY"] = api_key

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

# Initialize LLM with API key
llm = ChatNVIDIA(
    model="meta/llama-3.3-70b-instruct", 
    temperature=0,
    nvidia_api_key=api_key
)
llm_with_tools = llm.bind_tools([tools.search_tavily])


class ResearcherState(BaseModel):
    topic: str
    # the topic to be researched
    number_of_queries: int = 5
    # how many searches should be done per topic?
    messages: Annotated[Sequence[Any], add_messages] = []
    # a chat log of the research results


async def tool_node(state: ResearcherState):
    _LOGGER.info("Executing tool calls.")
    outputs = []
    for tool_call in state.messages[-1].tool_calls:
        _LOGGER.info("Executing tool call: %s", tool_call["name"])
        tool = getattr(tools, tool_call["name"])
        tool_result = await tool.ainvoke(tool_call["args"])
        outputs.append(
            {
                "role": "tool",
                "content": json.dumps(tool_result),
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
        )
    return {"messages": outputs}


async def call_model(
    state: ResearcherState,
    config: RunnableConfig,
) -> dict[str, Any]:
    _LOGGER.info("Calling model.")
    system_prompt = research_prompt.format(
        topic=state.topic, number_of_queries=state.number_of_queries
    )

    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await llm_with_tools.ainvoke(messages, config)

        if response:
            return {"messages": [response]}

        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


def has_tool_calls(state: ResearcherState) -> bool:
    """Check if the last message has tool calls."""
    messages = state.messages
    last_message = messages[-1]
    return bool(last_message.tool_calls)


workflow = StateGraph(ResearcherState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    has_tool_calls,
    {
        True: "tools",
        False: END,
    },
)
workflow.add_edge("tools", "agent")
graph = workflow.compile()
