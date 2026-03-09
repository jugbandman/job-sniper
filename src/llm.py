"""LLM Abstraction - supports local models (Ollama, LM Studio) and cloud APIs.

Usage:
    from src.llm import get_llm
    llm = get_llm()  # Auto-detects available backend
    response = llm.complete("Summarize this job posting: ...")

Backends (checked in order):
    1. Ollama (localhost:11434) - if running
    2. LM Studio (localhost:1234) - if running
    3. Any OpenAI-compatible server (LOCAL_LLM_URL env var)
    4. Anthropic Claude API (ANTHROPIC_API_KEY env var) - cloud fallback

Config: Set in _config/llm-config.yaml or environment variables.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from pathlib import Path


class LLMBackend:
    """Base class for LLM backends."""

    def __init__(self, name: str, base_url: str, model: str = ""):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.model = model

    def complete(self, prompt: str, system: str = "", max_tokens: int = 2000) -> str:
        raise NotImplementedError

    def is_available(self) -> bool:
        raise NotImplementedError


class OllamaBackend(LLMBackend):
    """Ollama local LLM (localhost:11434)."""

    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        super().__init__("ollama", base_url, model)

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read())
                models = [m.get("name", "") for m in data.get("models", [])]
                return len(models) > 0
        except (urllib.error.URLError, OSError):
            return False

    def list_models(self):
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                return [m.get("name", "") for m in data.get("models", [])]
        except (urllib.error.URLError, OSError):
            return []

    def complete(self, prompt: str, system: str = "", max_tokens: int = 2000) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        if system:
            payload["system"] = system

        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")


class OpenAICompatibleBackend(LLMBackend):
    """Any OpenAI-compatible API (LM Studio, vLLM, llama.cpp server, etc.)."""

    def __init__(self, base_url: str = "http://localhost:1234/v1",
                 model: str = "local-model", api_key: str = "not-needed"):
        super().__init__("openai-compatible", base_url, model)
        self.api_key = api_key

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError):
            return False

    def complete(self, prompt: str, system: str = "", max_tokens: int = 2000) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]


class AnthropicBackend(LLMBackend):
    """Claude API (cloud fallback)."""

    def __init__(self, model: str = "claude-haiku-4-5-20251001",
                 api_key: str = ""):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        super().__init__("anthropic", "https://api.anthropic.com", model)

    def is_available(self) -> bool:
        return bool(self.api_key)

    def complete(self, prompt: str, system: str = "", max_tokens: int = 2000) -> str:
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]


def load_llm_config(config_dir: str = "_config") -> Dict[str, Any]:
    """Load LLM config from yaml if it exists."""
    config_path = Path(config_dir) / "llm-config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def get_llm(config_dir: str = "_config", prefer: Optional[str] = None) -> LLMBackend:
    """Auto-detect and return the best available LLM backend.

    Args:
        config_dir: Path to config directory
        prefer: Force a specific backend ("ollama", "lmstudio", "anthropic")

    Returns:
        An LLMBackend instance ready to use.

    Raises:
        RuntimeError if no backend is available.
    """
    config = load_llm_config(config_dir)

    # Build backends to try
    backends = []

    if prefer == "ollama" or not prefer:
        ollama_model = config.get("ollama_model", os.environ.get("OLLAMA_MODEL", "llama3.2"))
        ollama_url = config.get("ollama_url", os.environ.get("OLLAMA_URL", "http://localhost:11434"))
        backends.append(OllamaBackend(model=ollama_model, base_url=ollama_url))

    if prefer == "lmstudio" or not prefer:
        lm_url = config.get("lmstudio_url", os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1"))
        lm_model = config.get("lmstudio_model", os.environ.get("LMSTUDIO_MODEL", "local-model"))
        backends.append(OpenAICompatibleBackend(base_url=lm_url, model=lm_model))

    # Custom OpenAI-compatible endpoint
    local_url = config.get("local_llm_url", os.environ.get("LOCAL_LLM_URL", ""))
    if local_url:
        local_model = config.get("local_llm_model", os.environ.get("LOCAL_LLM_MODEL", "local-model"))
        local_key = config.get("local_llm_key", os.environ.get("LOCAL_LLM_KEY", "not-needed"))
        backends.append(OpenAICompatibleBackend(base_url=local_url, model=local_model, api_key=local_key))

    if prefer == "anthropic" or not prefer:
        anthropic_model = config.get("anthropic_model", "claude-haiku-4-5-20251001")
        backends.append(AnthropicBackend(model=anthropic_model))

    # Try each in order
    for backend in backends:
        if backend.is_available():
            return backend

    raise RuntimeError(
        "No LLM backend available. Install Ollama (brew install ollama), "
        "run LM Studio, or set ANTHROPIC_API_KEY for cloud fallback."
    )
