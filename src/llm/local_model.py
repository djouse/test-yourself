from llama_cpp import Llama
from typing import Dict, Any

class LocalLlama:
    def __init__(self, model_path: str, n_ctx: int = 2048):
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
    def generate(self, prompt: str, max_tokens=512, temperature=0.1) -> str:
        out: Dict[str, Any] = self.llm.create_completion(prompt=prompt, max_tokens=max_tokens, temperature=temperature, stream=False)  # type: ignore
        return out["choices"][0]["text"]


llm = LocalLlama("path/to/qwen3-1_7b-q4_k_m.gguf")
response = llm.generate("Hello, how are you?")