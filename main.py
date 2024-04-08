# import
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import time

# load the document and split it into chunks
loader = TextLoader("list.txt")
data = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(separator='\n', chunk_size=0, chunk_overlap=0)
lines = text_splitter.split_documents(data)
# lines = data[0].split("\n")

# print(lines)
print(len(lines))

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(lines, embedding_function, persist_directory="./chroma_db")
Chroma.save(db, "./chroma_db")


# query it
start_time = time.time()
query = "cat singing happy birthday"
docs = db.similarity_search(query)
print(f"Search took {time.time() - start_time:.2f} seconds")

for doc in docs:
    print(doc.page_content)
print(docs[0].page_content)