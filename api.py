from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from rag_service import RAGService
from config import Config


config = Config()
rag = RAGService()



app = FastAPI(title="Hybrid RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Request / Response Models
# ----------------------------

class QueryRequest(BaseModel):
    query: str
    mode: str = "offline"


class QueryResponse(BaseModel):
    answer: str


# ----------------------------
# Routes
# ----------------------------

@app.get("/")
def root():
    return {"status": "Hybrid RAG API running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and index a document (PDF / PPT).
    """

    os.makedirs(config.UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(config.UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # This will load existing index if present
    rag.index_document(file_path)

    return {"message": f"{file.filename} indexed successfully"}


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system.
    """

    answer = rag.answer_query(request.query, mode=request.mode)

    return {"answer": answer}