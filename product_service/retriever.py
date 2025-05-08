from vector_store import VectorStore
from data_loader import load_product_data
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load product data
df = load_product_data()
documents = df.apply(lambda row: f"{row['Product Title']} - {row['Description']} Features: {row['Features']}", axis=1).tolist()

# Initialize vector store
vector_store = VectorStore()
vector_store.build_index(documents)

# Load Mistral model
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-13B-Instruct-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-13B-Instruct-v0.1", torch_dtype=torch.float16 if device == "cuda" else torch.float32).to(device)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if device == "cuda" else -1)

def search_products(query: str, top_k: int = 5) -> str:
    retrieved_docs = vector_store.query(query, top_k)
    context = "\n".join(retrieved_docs)

    prompt = f"""<s>[INST] Use the following product information to answer the user's query.
Product Info:
{context}

User Query:
{query}
[/INST]"""
    response = generator(prompt, max_new_tokens=300, do_sample=True)[0]['generated_text']
    return response.split("[/INST]")[-1].strip()
