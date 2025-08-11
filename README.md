# VectorMCP

A Model Context Protocol (MCP) server that provides vector search capabilities using Supabase and OpenAI embeddings. This server allows MCP-compatible clients (like Claude Desktop) to perform semantic search over documents stored in a Supabase vector database.

## Features

- **Vector Search**: Semantic document search using OpenAI embeddings
- **MCP Integration**: Compatible with Model Context Protocol clients
- **Supabase Backend**: Uses Supabase for vector storage and retrieval
- **FastAPI Server**: Built with FastAPI and Starlette for high performance

## Prerequisites

- Python 3.11 or higher
- Supabase account with vector database setup
- OpenAI API key
- MCP-compatible client (optional, for testing)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd VectorMCP
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with the following variables:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Configuration

### Supabase Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Set up a table for storing documents with embeddings
3. Create a PostgreSQL function for vector similarity search:

```sql
-- Example function for vector similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_count int DEFAULT 5,
  filter jsonb DEFAULT '{}'
)
RETURNS TABLE (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE documents.embedding IS NOT NULL
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anonymous key | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## Usage

### Running the Server

1. **Start the MCP server**:
   ```bash
   python server.py
   ```

   The server will start on `http://0.0.0.0:10000`

2. **Test the server** (optional):
   ```bash
   python main.py
   ```

### MCP Tool: GoogleDrive_search

The server provides a tool called `GoogleDrive_search` that performs semantic search:

- **Parameters**:
  - `query` (string): The search query
  - `match_count` (int, optional): Number of results to return (default: 5)

- **Returns**: List of matching documents with content and metadata

### Example Usage with MCP Client

If you're using an MCP-compatible client like Claude Desktop, you can:

1. Add the server to your MCP configuration
2. Use the `GoogleDrive_search` tool to search your documents
3. Get semantically relevant results based on your query

## Project Structure

```
VectorMCP/
├── server.py          # Main MCP server implementation
├── main.py           # Simple test script
├── requirements.txt  # Python dependencies
├── pyproject.toml    # Project configuration
├── .env             # Environment variables (create this)
└── README.md        # This file
```

## Dependencies

- `fastapi` - Web framework
- `starlette` - ASGI framework
- `uvicorn` - ASGI server
- `openai` - OpenAI API client
- `supabase` - Supabase client
- `python-dotenv` - Environment variable management
- `mcp[cli]` - Model Context Protocol implementation

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use environment variables for all sensitive configuration
- Consider using Supabase Row Level Security (RLS) for data protection

## Troubleshooting

### Common Issues

1. **Missing environment variables**: Ensure all required variables are set in your `.env` file
2. **Supabase connection issues**: Verify your Supabase URL and key are correct
3. **OpenAI API errors**: Check your OpenAI API key and billing status
4. **Port conflicts**: The server runs on port 10000 by default

### Error Messages

- `"SUPABASE_URL environment variable is required"` - Add SUPABASE_URL to your .env file
- `"SUPABASE_KEY environment variable is required"` - Add SUPABASE_KEY to your .env file
- `"OPENAI_API_KEY environment variable is required"` - Add OPENAI_API_KEY to your .env file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the Supabase and OpenAI documentation
- Open an issue in the repository
