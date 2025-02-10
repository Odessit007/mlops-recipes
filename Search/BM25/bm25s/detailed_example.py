import bm25s
import Stemmer  # optional: for stemming

# Create your corpus here
corpus = [
    "a cat is a feline and likes to purr",
    "a dog is the human's best friend and loves to play",
    "a bird is a beautiful animal that can fly",
    "a fish is a creature that lives in water and swims",
]

# optional: Create a stemmer
stemmer = Stemmer.Stemmer("english")

# Tokenize corpus
corpus_tokens = bm25s.tokenize(
    texts=corpus,  # A list of strings or a single string
    lower=True,  # Whether to convert the text to lowercase before tokenization (default: True)
    stopwords="english",  # The list of stopwords to remove from the text. If "english" or "en" is provided,
                          # the function will use the default English stopwords
    stemmer=stemmer,  # An optional callable (default: None)
)
print(f"{type(corpus_tokens) = }")
print("Unique token ids for corpus:", corpus_tokens.ids)
print("Token-to-id vocabulary for corpus:", corpus_tokens.vocab)


# Create the BM25 model and index the corpus
retriever = bm25s.BM25()
retriever.index(corpus_tokens)

# Query the corpus and get top-k results
queries = [
    "does the fish purr like a cat?",
    "which animal lives in water?"
]
query_tokens = bm25s.tokenize(queries, stemmer=stemmer)  # A single string can be passed if only one query is considered
print(f"{type(query_tokens) = }")
print("Unique token ids for queries:", query_tokens.ids)
print("Token-to-id vocabulary for queries:", query_tokens.vocab)

# Explore results
results, scores = retriever.retrieve(query_tokens, k=4)
print()
print(f"{type(results) = }; {results.shape = }")
print(f"{type(scores) = }; {scores.shape = }")
for query_index in range(results.shape[0]):
    print(f"Query: {queries[query_index]}")
    for result_index in range(results.shape[1]):
        doc, score = results[query_index, result_index], scores[query_index, result_index]
        print(f"\tRank {result_index+1} result: (score: {score:.2f}, doc: {corpus[doc]})")

# You can save the arrays to a directory...
retriever.save("animal_index_bm25")
# You can save the corpus along with the model
retriever.save("animal_index_bm25", corpus=corpus)
# ...and load them when you need them (set load_corpus=False if you don't need the corpus)
reloaded_retriever = bm25s.BM25.load("animal_index_bm25", load_corpus=True)
