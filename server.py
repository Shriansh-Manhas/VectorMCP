from typing import List, Dict

from mcp.server.fastmcp import FastMCP, Context
from supabase import create_client
import openai
import os
from starlette.applications import Starlette
from starlette.routing import Mount, Host
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate required environment variables
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is required")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY environment variable is required")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

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
    uvicorn.run(app, host="0.0.0.0", port=10000)