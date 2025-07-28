"""Tools for the report generation workflow."""

import asyncio
import logging
import os
from typing import Literal

from langchain_core.tools import tool

_LOGGER = logging.getLogger(__name__)

INCLUDE_RAW_CONTENT = False
MAX_TOKENS_PER_SOURCE = 1000
MAX_RESULTS = 5
SEARCH_DAYS = 30


def _create_simulated_search_results(query: str) -> dict:
    """
    Create simulated search results for demonstration purposes.
    This replaces the Tavily API functionality.
    """
    # Simulated search results based on common topics
    simulated_results = {
        "ai": [
            {
                "title": "Artificial Intelligence: A Comprehensive Overview",
                "url": "https://example.com/ai-overview",
                "content": "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding.",
                "raw_content": "AI has evolved significantly over the past decades, from simple rule-based systems to complex neural networks and deep learning models. The field encompasses various sub-disciplines including machine learning, natural language processing, computer vision, and robotics."
            },
            {
                "title": "Machine Learning Fundamentals",
                "url": "https://example.com/ml-fundamentals", 
                "content": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.",
                "raw_content": "Machine learning algorithms can be categorized into supervised learning, unsupervised learning, and reinforcement learning. Each approach has different applications and use cases in various industries."
            }
        ],
        "technology": [
            {
                "title": "Emerging Technologies in 2024",
                "url": "https://example.com/emerging-tech",
                "content": "The technology landscape continues to evolve rapidly with innovations in quantum computing, blockchain, and renewable energy technologies shaping the future of various industries.",
                "raw_content": "Quantum computing promises to revolutionize cryptography and complex problem-solving, while blockchain technology is transforming financial services and supply chain management."
            }
        ],
        "science": [
            {
                "title": "Recent Advances in Scientific Research",
                "url": "https://example.com/scientific-advances",
                "content": "Scientific research continues to push boundaries in fields such as medicine, physics, and environmental science, leading to breakthroughs that improve human life and understanding of the universe.",
                "raw_content": "Recent developments include advances in gene editing technology, discoveries in particle physics, and innovations in renewable energy systems."
            }
        ]
    }
    
    # Default results for any query
    default_results = [
        {
            "title": f"Information about {query}",
            "url": f"https://example.com/{query.replace(' ', '-')}",
            "content": f"This is simulated information about {query}. In a real implementation, this would contain actual search results from the web.",
            "raw_content": f"Detailed simulated content about {query}. This demonstrates how the document generation agent would work with real search results."
        }
    ]
    
    # Try to match query to simulated topics
    query_lower = query.lower()
    for topic, results in simulated_results.items():
        if topic in query_lower:
            return {"results": results[:MAX_RESULTS]}
    
    return {"results": default_results}


def _deduplicate_and_format_sources(
    search_response, max_tokens_per_source, include_raw_content=True
):
    """
    Takes either a single search response or list of responses and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    include_raw_content specifies whether to include the raw_content in the formatted string.

    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results

    Returns:
        str: Formatted string with deduplicated sources
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response["results"]
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and "results" in response:
                sources_list.extend(response["results"])
            else:
                sources_list.extend(response)
    else:
        raise ValueError(
            "Input must be either a dict with 'results' or a list of search results"
        )

    # Deduplicate by URL
    unique_sources = {}
    for source in sources_list:
        if source["url"] not in unique_sources:
            unique_sources[source["url"]] = source

    # Format output
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += (
            f"Most relevant content from source: {source['content']}\n===\n"
        )
        if include_raw_content:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4
            # Handle None raw_content
            raw_content = source.get("raw_content", "")
            if raw_content is None:
                raw_content = ""
                print(f"Warning: No raw_content found for source {source['url']}")
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"

    return formatted_text.strip()


@tool(parse_docstring=True)
async def search_tavily(
    queries: list[str],
    topic: Literal["general", "news", "finance"] = "news",
) -> str:
    """Search the web using simulated search results (no API key required).

    Args:
        queries: List of queries to search.
        topic: The topic of the provided queries.
          general - General search.
          news - News search.
          finance - Finance search.

    Returns:
        A string of the search results.
    """
    _LOGGER.info("Searching using simulated results (Tavily API not available)")

    search_jobs = []
    for query in queries:
        _LOGGER.info("Searching for query: %s", query)
        # Create simulated search results
        simulated_results = _create_simulated_search_results(query)
        search_jobs.append(asyncio.create_task(asyncio.sleep(0.1)))  # Simulate async delay

    # Wait for all simulated searches to complete
    await asyncio.gather(*search_jobs)

    # Get results for the first query (in a real implementation, this would be all queries)
    if queries:
        search_docs = [_create_simulated_search_results(queries[0])]
    else:
        search_docs = [{"results": []}]

    formatted_search_docs = _deduplicate_and_format_sources(
        search_docs,
        max_tokens_per_source=MAX_TOKENS_PER_SOURCE,
        include_raw_content=INCLUDE_RAW_CONTENT,
    )
    _LOGGER.debug("Search results: %s", formatted_search_docs)
    return formatted_search_docs
