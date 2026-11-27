from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
from similarity import cosine_similarity

load_dotenv()

client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY"),
)

def load_documents():
  documents = {}
  folder = Path("knowledge")

  for file in folder.glob("*.txt"):
    documents[file.name] = file.read_text(encoding="utf-8")

  return documents

def retrieve(question):
  documents = load_documents()
  question = question.lower()
  for filename, content in documents.items():
    if question in content.lower():
      return filename, content
  return None, None

def create_embedding(text):
  response = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input=text
  )

  return response.data[0].embedding