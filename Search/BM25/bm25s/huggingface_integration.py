import bm25s
from bm25s.hf import BM25HF

# Create your corpus here
corpus = [
    "a cat is a feline and likes to purr",
    "a dog is the human's best friend and loves to play",
    "a bird is a beautiful animal that can fly",
    "a fish is a creature that lives in water and swims",
]

# Index corpus
retriever = BM25HF()
retriever.index(bm25s.tokenize(corpus))

# Save index to HuggingFace Hub (assumes that HUGGING_FACE_HUB_TOKEN environment variable is set)
user = "your-username"
retriever.save_to_hub(f"{user}/bm25s-animals")

# Load index from HuggingFace Hub
retriever = BM25HF.load_from_hub("{user}/bm25s-animals", load_corpus=True)  # Add mmap=True for lower memory usage

# Use retriever
query = "a cat is a feline"
docs, scores = retriever.retrieve(bm25s.tokenize(query), k=2)
