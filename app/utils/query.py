import os
import json
import faiss
from uuid import uuid4
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  


DATA_FOLDER = "data\raw"

documents = []
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".json"):  
        file_path = os.path.join(DATA_FOLDER, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                if any(keyword in filename.lower() for keyword in ["events", "news", "notices"]):
                    
                    page_content = item["content"].get("text", "") if isinstance(item["content"], dict) else item["content"]
                    
                    doc = Document(
                        page_content=page_content,  
                        metadata={"title": item.get("title", "No Title"), "category": "event", "url": item.get("url", "")}
                    )
                
                elif "industries" in filename.lower():
                    page_content = item.get("content", "")  
                    doc = Document(
                        page_content=page_content,  
                        metadata={"title": item.get("program_name", "No title"), "category": "industry"}
                    )

                else:
                    page_content = item["content"].get("text", "") if isinstance(item["content"], dict) else item["content"]
                    
                    doc = Document(
                        page_content=page_content,  
                        metadata={"category": "unknown"}
                    )

                documents.append(doc)

print(f"📂 Đã load {len(documents)} tài liệu từ {DATA_FOLDER}")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(len(embeddings.embed_query("test")))
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)

query = "Sự kiện về công nghệ tại PTIT"
results = vector_store.similarity_search(query, k=2)

print("\n🔍 Kết quả tìm kiếm:")
for res in results:
    print(f"{res.metadata.get('title', 'No Title')} ({res.metadata.get('date', 'No Date')})\n{res.page_content[:300]}...\n🔗 {res.metadata.get('url', 'No URL')}\n")
