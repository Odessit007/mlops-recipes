# Relevant papers
* 2014: [Improvements to BM25 and Language Models Examined](https://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf)
* 2020: [Which BM25 Do You Mean? A Large-Scale Reproducibility Study of Scoring Variants](https://link.springer.com/chapter/10.1007/978-3-030-45442-5_4)
* 2024: [BM25S: Orders of magnitude faster lexical search via eager sparse scoring](https://arxiv.org/pdf/2407.03618)


# Implementations
According to https://huggingface.co/blog/xhluca/bm25s
* ElasticSearch:
  * pro: high performance and scalability, allowing you to search among billions of documents in real-time
  by leveraging multi-node setups
  * pro: wide range of features
  * con: you need to set up a web server that runs Apache Lucene in Java, and access it via a separate web client
* [rank-bm25](https://pypi.org/project/rank-bm25/)
  * pro: more accessible, as it is solely Numpy
  * pro: you can use your own tokenizer
  * pro: you can change parameters during search
  * con: unable to achieve the same performance in terms of queries/seconds for large corpora (>1M docs)
* [bm25s](https://bm25s.github.io/)
  * pro: uses scipy's sparse matrices to achieve orders of magnitudes faster search compared to Rank-BM25
    * in the single-threaded and multicore setting (4 threads), it achieves performance on par with Elasticsearch
* [pyserini](https://github.com/castorini/pyserini/tree/master)
  * pro: includes *many* different retrievers
  * pro: includes sparse, dense and hybrid search algorithms and many reproducibility tools
  * con: depends on some Java stuff
* BM25-PT: can be used on GPUs via PyTorch


# Customization
```python
import bm25s
retriever = bm25s.BM25()

# You can provide a list of queries instead of a single query
queries = ["What is a cat?", "is the bird a dog?"]

# Provide your own stopwords list if you don't like the default one
stopwords = ["a", "the"]

# For stemming, use any function that is callable on each word list
stemmer_fn = lambda lst: [word for word in lst]

# Tokenize the queries
query_token_ids = bm25s.tokenize(queries, stopwords=stopwords, stemmer=stemmer_fn)

# If you want the tokenizer to return strings instead of token ids, you can do this
query_token_strs = bm25s.tokenize(queries, return_ids=False)

# You can use a different corpus for retrieval, e.g., titles instead of full docs
titles = ["About Cat", "About Dog", "About Bird", "About Fish"]

# You can also choose to only return the documents and omit the scores
# note: if you pass a new corpus here, it must have the same length as your indexed corpus
results = retriever.retrieve(query_token_ids, corpus=titles, k=2, return_as="documents")

# The documents are returned as a numpy array of shape (n_queries, k)
for i in range(results.shape[1]):
    print(f"Rank {i+1}: {results[0, i]}")
```
