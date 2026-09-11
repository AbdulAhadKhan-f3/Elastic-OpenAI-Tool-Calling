from mcp.server import MCPServer

from tools.elastic_tools import (
    list_indices as elastic_list_indices,
    get_index_mapping as elastic_get_index_mapping,
    search_documents as elastic_search_documents,
    get_document as elastic_get_document,
    create_document as elastic_create_document,
    update_document as elastic_update_document,
    delete_document as elastic_delete_document
)

mcp = MCPServer("User Management Server")

@mcp.tool()
def list_indices() -> list:
    """Return all Elasticsearch indices."""
    return elastic_list_indices()


@mcp.tool()
def get_index_mapping(index: str) -> dict:
    """Return the mapping and field definitions for an Elasticsearch index."""
    return elastic_get_index_mapping(index)


@mcp.tool()
def search_documents(index: str, query: dict) -> dict:
    """
    Search documents in an Elasticsearch index.

    The query parameter must contain only the Elasticsearch Query DSL
    query object, such as:
    {"match_all": {}}
    or
    {"match": {"name": "Ahmed"}}
    or
    {"term": {"role": "customer"}}

    Do not include top-level Elasticsearch search parameters such as
    "query", "size", or "sort" inside this parameter.
    """
    return elastic_search_documents(index, query)

@mcp.tool()
def create_document(index: str, document: dict) -> dict:
    """Create a document in an Elasticsearch index. Elasticsearch generates the document ID."""
    return elastic_create_document(index, document)

@mcp.tool()
def get_document(index: str, document_id: str) -> dict:
    """Get a specific document from an Elasticsearch index by its document ID."""
    return elastic_get_document(index, document_id)


@mcp.tool()
def update_document(index: str, document_id: str, document: dict) -> dict:
    """Update fields in an existing Elasticsearch document."""
    return elastic_update_document(index, document_id, document)


@mcp.tool()
def delete_document(index: str, document_id: str) -> dict:
    """Delete a document from an Elasticsearch index."""
    return elastic_delete_document(index, document_id)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8000
    )