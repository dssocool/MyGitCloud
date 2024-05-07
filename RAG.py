from langchain.chains import RetrievalQA
from langchain import FAISS, HuggingFaceHub
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# Load documents for retrieval
documents = [
    "Python is an interpreted high-level programming language.",
    "It is dynamically typed and garbage-collected.",
    "Python is widely used for web development, data analysis, and more."
]

# Split documents into manageable chunks
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
texts = text_splitter.split_text("\n".join(documents))

# Initialize embeddings using Sentence Transformers (open-source model)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Create a FAISS vector store from the text chunks
vector_store = FAISS.from_texts(texts, embeddings)

# Load a local generative model from Hugging Face (you can replace this model)
generator = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0})

# Create the retrieval-based QA chain
qa = RetrievalQA.from_chain_type(
    llm=generator,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# Test the QA system with a query
query = "What is Python used for?"
result = qa.run(query)
print("Answer:", result)

