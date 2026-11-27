from openai import OpenAI
from dotenv import load_dotenv
import os
from similarity import cosine_similarity

load_dotenv()

client = OpenAI(
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY"),
)

first_input = "Python is a programming language"
second_input = "Pizza is nice"
third_input = "SQL is a query language"

first_response = client.embeddings.create(
  model=os.getenv("EMBEDDING_MODEL"),
  input=first_input
)
first_embedding = first_response.data[0].embedding
print(type(first_embedding))
print(len(first_embedding))

second_response = client.embeddings.create(
  model=os.getenv("EMBEDDING_MODEL"),
  input=second_input
)
second_embedding = second_response.data[0].embedding
print(type(second_embedding))
print(len(second_embedding))

third_response = client.embeddings.create(
  model=os.getenv("EMBEDDING_MODEL"),
  input=third_input
)
third_embedding = third_response.data[0].embedding
print(type(third_embedding))
print(len(third_embedding))

print(f"The cosine similarity score for the 1st and 2nd input is {cosine_similarity(first_embedding, second_embedding)}")
print(f"The cosine similarity score for the 1st and 2nd input is {cosine_similarity(first_embedding, third_embedding)}")