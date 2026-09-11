from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


def list_indices():
    response = es.cat.indices(format="json")

    return [
        {
            "index": index["index"],
            "status": index["status"],
            "docs_count": index["docs.count"]
        }
        for index in response
        if not index["index"].startswith(".")
    ]


def get_index_mapping(index: str):
    response = es.indices.get_mapping(index=index)

    return response[index]["mappings"]


def search_documents(index: str, query: dict):
    response = es.search(
        index=index,
        query=query
    )

    return {
        "total": response["hits"]["total"]["value"],
        "documents": [
            {
                "id": hit["_id"],
                "score": hit.get("_score"),
                "source": hit["_source"]
            }
            for hit in response["hits"]["hits"]
        ]
    }


def get_document(index: str, document_id: str):
    response = es.get(
        index=index,
        id=document_id
    )

    return {
        "id": response["_id"],
        "source": response["_source"]
    }


def create_document(index: str, document: dict):
    response = es.index(
        index=index,
        document=document
    )

    return {
        "id": response["_id"],
        "result": response["result"]
    }


def update_document(index: str, document_id: str, document: dict):
    response = es.update(
        index=index,
        id=document_id,
        doc=document
    )

    return {
        "id": response["_id"],
        "result": response["result"]
    }


def delete_document(index: str, document_id: str):
    response = es.delete(
        index=index,
        id=document_id
    )

    return {
        "id": response["_id"],
        "result": response["result"]
    }