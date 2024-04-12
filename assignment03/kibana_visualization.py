from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import pandas as pd

# Connect to Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])

# Elasticsearch query
query = {
    "size": 0,
    "aggs": {
        "top_entities": {
            "terms": {
                "field": "entities",
                "size": 10
            }
        }
    }
}

response = es.search(index="named_entities", body=query)

# Process and plot the data
buckets = response['aggregations']['top_entities']['buckets']
entities = [bucket['key'] for bucket in buckets]
counts = [bucket['doc_count'] for bucket in buckets]

df = pd.DataFrame({
    'Entity': entities,
    'Count': counts
})

df.plot(kind='bar', x='Entity', y='Count', legend=None)
plt.xlabel('Named Entities')
plt.ylabel('Count')
plt.title('Top 10 Named Entities')
plt.tight_layout()
plt.show()
