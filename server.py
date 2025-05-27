from typing import List, Dict

from mcp.server.fastmcp import FastMCP, Context
from supabase import create_client
import openai
import os
from starlette.applications import Starlette
from starlette.routing import Mount, Host
import json

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

app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)