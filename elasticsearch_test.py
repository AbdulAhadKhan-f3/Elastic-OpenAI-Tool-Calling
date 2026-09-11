from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

print("Connected:", es.ping())

response = es.search(
    index="users",
    query={
        "match": {
            "name": "Ahmed"
        }
    }
)

for hit in response["hits"]["hits"]:
    print(hit["_source"])