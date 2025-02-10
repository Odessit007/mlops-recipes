Sources:
* https://huggingface.co/blog/xhluca/bm25s -- Official HuggingFace post
* https://bm25s.github.io/ -- Official BM25s docs


<a id="installation"></a>
# Installation
`pip install bm25s`
`poetry add bm25s`
etc.

Optional dependencies:
* to speed up indexing: `numba`
* to speed up top-k selection: `jax[cpu]`
* to use stemming: `PyStemmer`


# Documentation:
README: https://github.com/xhluca/bm25s/blob/main/README.md
Examples: https://github.com/xhluca/bm25s/tree/main/examples


# Basic usage
```python
import bm25s

# Index
corpus = ["list of strings", "that", "represent documents", "to be searched"]
retriever = bm25s.BM25(method="preferred variant of BM25")
retriever.index(bm25s.tokenize(corpus))

# Retrieve
query = "Query string"
results, scores = retriever.retrieve(bm25s.tokenize(query), k=2)
doc, score = results[0, 0], scores[0, 0]
print(f"Score: {score:.2f}. Doc: {corpus[doc]}")
```

Key parameters:
* `k1: float = 1.5`
  * The k1 parameter in the BM25 formula.
* `b: float = 0.75`
  * The b parameter in the BM25 formula.
* `delta: float = 0.5`
  * The delta parameter in the BM25L and BM25+ formulas; it is ignored for other methods.
* `method: str = "lucene"`
    * The method to use for scoring term frequency. Choose from 'robertson', 'lucene', 'atire'.
* `idf_method: str = None`
    * The method to use for scoring inverse document frequency (same choices as `method`).
    * If None, it will use the same method as `method`. If you are unsure, please do not
    change this parameter.
* `backend: str = "numpy"`
  * The backend used during retrieval. By default, it uses the numpy backend, which 
    only requires numpy and scipy as dependencies. You can also select `backend="numba"`
    to use the numba backend, which requires the numba library.
  * If you select `backend="auto"`, the function will use the numba backend if it is available, otherwise it will use the numpy backend.


# Selecting a BM25 variant
BM25S offers the following variants:
* Original (method="robertson")
* ATIRE (method="atire")
* BM25L (method="bm25l")
* BM25+ (method="bm25+")
* Lucene (method="lucene") - default

* You can change this by simply specifying BM25(method="<preferred variant>").


# Memory-efficient retrieval
`bm25s` is designed to be memory efficient. You can use the `mmap` option to load the BM25 index as a memory-mapped file,
  which allows you to load the index without loading the full index into memory.
  This is useful when you have a large index and want to save memory.
```python
# Create a BM25 index
# ...

# let's say you have a large corpus
corpus = [
    "a very long document that is very long and has many words",
    "another long document that is long and has many words",
    # ...
]
# Save the BM25 index to a file
retriever.save("bm25s_very_big_index", corpus=corpus)

# Load the BM25 index as a memory-mapped file, which is memory efficient
# and reduce overhead of loading the full index into memory
retriever = bm25s.BM25.load("bm25s_very_big_index", mmap=True)
```
