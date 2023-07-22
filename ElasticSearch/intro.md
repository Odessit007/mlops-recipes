Key terms:
* **Document**: everything you store in ES is a JSON document
* **Index**: a logical collection of documents
* **Shard**: a physical instance of Apache Lucene which is maintained by an index; index can have multiple shards,
and they will store your documents
* **Node**: an ES instance
* **Cluster**: a set of nodes
  * the simplest setup is a cluster consisting of a single node



* [Local setup](#local_setup)
* [Some REST API examples](#rest_api)
  * [Add document to the index](#add_doc)
  * [Get document by ID](#get_doc)



<a id="local_setup"></a>
# Local setup
Running ES with Docker:
```bash
docker network create elastic

ES_IMAGE=docker.elastic.co/elasticsearch/elasticsearch:8.8.2
ES_CONTAINER=elasticsearch
docker pull $ES_IMAGE
docker run --name $ES_CONTAINER --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t $ES_IMAGE
```

When you start Elasticsearch for the first time, the generated `elastic` user password and Kibana enrollment token are output to the terminal.

Copy the generated password and enrollment token and save them in a secure location.
* These values are shown only when you start Elasticsearch for the first time.
* You can reset the `elastic` user's password with this command:
```bash
docker exec -it $ES_CONTAINER /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```
  * add `-i` flag to provide a desired password, otherwise it will be auto-generated
* You can generate new Kibana enrollment token with this command:
```bash
docker exec -it $ES_CONTAINER /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

Further, you may need to copy the `http_ca.cert` security certificate from your Docker cotainer to your local machine:
```bash
docker cp $ES_CONTAINER:/usr/share/elasticsearch/config/certs/http_ca.crt .
```

Finally, check that you can connect to the cluster (you will be prompted for the password):
```bash
curl --cacert http_ca.crt -u elastic https://localhost:9200
```

Run Kibana with Docker:
```bash
KIBANA_IMAGE=docker.elastic.co/kibana/kibana:8.8.2
KIBANA_CONTAINER=kibana
docker pull $KIBANA_IMAGE
docker run --name $KIBANA_CONTAINER --net elastic -p 5601:5601 $KIBANA_IMAGE
```

When you start Kibana, a unique URL is output to your terminal. o access Kibana, open the generated URL in your browser.
1. Paste the enrollment token that you copied when starting Elasticsearch and click the button to connect your Kibana instance with Elasticsearch.
2. Log in to Kibana as the elastic user with the password that was generated when you started Elasticsearch.



<a id="indexes"></a>
# Indexes
If you run `GET {index_name}/` in Kibana dev console, you'll get a JSON like this (filled with data, of course):
```json
{
  "index_name": {
    "aliases": {},
    "mappings": {},
    "settings": {}
  }
}
```

You can assign an `alias` for an index or a set of indexes, then you can search in a set of indexes using a common name
instead of searching in each index separately.

The `mappings` define the fields in the document: their types and how to index them. For example,
```json
"mappings": {
  "properties": {
    "field_1": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    },
    "field_2": {
      "type": "long"
    }
  }
```

The `settings` include stuff like the number of shards and replicas for the data stored in the index. For example,
```json
"settings": {
  "index": {
    "routing": {
      "allocation": {
        "include": {
          "_tier_preference": "data_content"
        }
      }
    },
    "number_of_shards": "1",
    "provided_name": "test_index",
    "creation_date": "1689871127549",
    "number_of_replicas": "1",
    "uuid": "_LTwhfIlQMef3Yp3fFKE8w",
    "version": {
      "created": "8080299"
    }
  }
}
```

Settings have defualt values when you create an index and mappings can be automatically created when you add documents to the index.
But you can also define mappings and settings during index creation. For example,
```bash
PUT index_name
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      }
    }
  },
  "settings": {
    "number_of_replicas": 3
  }
}
```





<a id="rest_api"></a>
# Some REST API examples

<a id="add_doc"></a>
## Add document to the index
(will auto-create index if it doesn't exist)
```bash
PUT {index_name}/_doc/{doc_id}
{
  "field_1": "val_1",
  "field_2": 42
}
```

The possible result (if index is `test_index` and doc_id is `abc`) may look like
```json
{
  "_index": "test_index",
  "_id": "abc",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

If you try the same command again (for example, if the field values have changed), you'll get result
`updated` instead of `created` and the `_version` will increase:
```json
{
  "_index": "test_index",
  "_id": "abc",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1
}
```

If you omit `doc_id` then it will be auto-generated. You need to use `POST` method in such case:
```bash
POST test_index/_doc/
{
  "field_1": "val"
}
```

A possible (truncated) output:
```json
{
  "_index": "test_index",
  "_id": "5OEwdIkB11VxMfu70Ojy",
  "_version": 1,
  "result": "created",
}
```


<a id="get_doc"></a>
## Get document by ID
```bash
GET {index_name}/_doc/{doc_id}
```

If we run `GET test_index/_doc/abc` then the output will be
```json
{
  "_index": "test_index",
  "_id": "abc",
  "_version": 2,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "field_1": "val_2",
    "field_2": 0
  }
}
```

The original document is accessible from the `_source` field in the output JSON.