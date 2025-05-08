from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "mistralai/Mistral-13B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

def generate_response(context: str, query: str) -> str:
    prompt = f"""
[INST] <<SYS>>
You are a helpful e-commerce assistant.
<</SYS>>
Context: {context}
User: {query}
Answer: [/INST]"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Answer:")[-1].strip()