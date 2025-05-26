from typing import List, Dict

from mcp.server.fastmcp import FastMCP, Context
from supabase import create_client
import openai
import os


SUPABASE_URL = "https://kfsykxpudjoopziididi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtmc3lreHB1ZGpvb3B6aWlkaWRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgwMjMzMzksImV4cCI6MjA2MzU5OTMzOX0.goGnx2jo84WBjISqCBGTZ62fnTD3a5G0wSQa05FGvZY"

openai.api_key = "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"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

mcp = FastMCP(
    "MCP Supabase Server",
    dependencies=["supabase", "openai"]
)
@mcp.tool()
def GoogleDrive_search(ctx: Context, query: str, match_count: int = 5) -> list:
    response = openai.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding

    res = supabase.rpc("match_documents", {
        "query_embedding": embedding,
        "match_count": match_count,
        "filter": {}
    }).execute()

    return [
        {
            "pageContent": row["content"],
            "metadata": row.get("metadata", {})
        }
        for row in (res.data or [])
    ]

@mcp.prompt()
def handle_prompt(ctx: Context, messages: List[Dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "user":
            return f"You said: {message['content']}"
    return "I didn't receive a user message."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port
    mcp.run(transport="sse")