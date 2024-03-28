import os
import openai
import uuid

from typing import Coroutine, List

# Canopy Imports
from canopy.tokenizer import Tokenizer
from canopy.models.data_models import Document
from canopy.knowledge_base.knowledge_base import KnowledgeBase
from canopy.knowledge_base import KnowledgeBase, list_canopy_indexes
from canopy.knowledge_base.chunker.base import Chunker
from canopy.knowledge_base.models import KBDocChunk
from canopy.knowledge_base.chunker import recursive_character

# GoogleDrive Loader
from langchain_community.document_loaders import GoogleDriveLoader

# Environment Variables
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

os.environ["PINECONE_API_KEY"] = os.environ.get('PINECONE_API_KEY')
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')

Tokenizer.initialize()

# Knowledge Base

INDEX_NAME = "google-drive"
kb = KnowledgeBase(index_name=INDEX_NAME)

if not any(name.endswith(INDEX_NAME) for name in list_canopy_indexes()):
    kb.create_canopy_index()

# Google Drive

GDRIVE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

# Load Documents from Google Drive
LOADER = GoogleDriveLoader(
    folder_id = GDRIVE_FOLDER_ID,
    file_types = ["application/pdf"],
    recursive = True
)

documents = LOADER.load()

# Establish Document Data Structure
gdrive_docs = []
for doc in documents:
    rid = uuid.uuid4()
    gdrive_docs.extend([Document(
        id=str(rid),
        text = doc.page_content,
        source = doc.metadata['source'],
        metadata =  {
            "title": doc.metadata['title'], 
            "page": doc.metadata['page']
        }
    )])

# Chunk the documents
class newLineChunker(Chunker):

    def chunk_single_document(self, document: Document) -> List[KBDocChunk]:
        return recursive_character.RecursiveCharacterChunker(chunk_size=1500, chunk_overlap=150).chunk_single_document(document)
    
    def achunk_single_document(self, document: Document) -> Coroutine[GoogleDriveLoader, GoogleDriveLoader, List[KBDocChunk]]:
        raise NotImplementedError()
    
    def chunk_documents(self, documents: List[Document]) -> List[KBDocChunk]:
        return super().chunk_documents(documents)
    
chunker = newLineChunker()

chunker.chunk_documents(gdrive_docs)

# Upsert Chunks
kb = KnowledgeBase(index_name=INDEX_NAME, chunker=chunker)
kb.connect()
kb.upsert(gdrive_docs)

# Test Query
results = kb.query([Query(text="What is the Paid time off policy?", metadata_filter={"title": "PAID TIME OFF POLICY.pdf"})])

print(results)