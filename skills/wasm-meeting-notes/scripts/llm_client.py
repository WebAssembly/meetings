import os
import sys
import json
import urllib.request
import urllib.error

def get_llm_config():
    """
    Resolves the LLM provider, API key, base URL, and model from environment variables.
    Supports OpenAI-compatible APIs (OpenAI, Ollama, Groq, OpenRouter, DeepSeek, LocalAI, vLLM),
    Google Gemini, and Anthropic Claude.
    """
    provider = os.environ.get("LLM_PROVIDER", "").strip().lower()

    api_key = (
        os.environ.get("LLM_API_KEY") or
        os.environ.get("OPENAI_API_KEY") or
        os.environ.get("GEMINI_API_KEY") or
        os.environ.get("ANTHROPIC_API_KEY")
    )

    base_url = (
        os.environ.get("LLM_BASE_URL") or
        os.environ.get("OPENAI_BASE_URL") or
        os.environ.get("ANTHROPIC_BASE_URL") or
        os.environ.get("GEMINI_BASE_URL")
    )

    model = (
        os.environ.get("LLM_MODEL") or
        os.environ.get("OPENAI_MODEL") or
        os.environ.get("GEMINI_MODEL") or
        os.environ.get("ANTHROPIC_MODEL")
    )

    if not provider:
        if os.environ.get("ANTHROPIC_API_KEY") or (api_key and api_key.startswith("sk-ant")):
            provider = "anthropic"
        elif os.environ.get("GEMINI_API_KEY") or (api_key and api_key.startswith("AIza")):
            provider = "gemini"
        elif os.environ.get("OPENAI_API_KEY") or base_url or (api_key and api_key.startswith("sk-")):
            provider = "openai"
        else:
            provider = "openai"

    if not api_key and not base_url:
        print("Error: No LLM API key or base URL configured.", file=sys.stderr)
        print("Please set one of the following environment variables:", file=sys.stderr)
        print("  - LLM_API_KEY (and optional LLM_BASE_URL, LLM_MODEL)", file=sys.stderr)
        print("  - OPENAI_API_KEY (and optional OPENAI_BASE_URL, OPENAI_MODEL)", file=sys.stderr)
        print("  - GEMINI_API_KEY (and optional GEMINI_MODEL)", file=sys.stderr)
        print("  - ANTHROPIC_API_KEY (and optional ANTHROPIC_MODEL)", file=sys.stderr)
        sys.exit(1)

    return {
        "provider": provider,
        "api_key": api_key,
        "base_url": base_url,
        "model": model
    }

def call_llm(system_instruction, user_prompt, response_json=False, temperature=0.1):
    """
    Sends a prompt to the configured LLM provider and returns the response string.
    """
    config = get_llm_config()
    provider = config["provider"]
    api_key = config["api_key"]
    base_url = config["base_url"]
    model = config["model"]

    if provider == "gemini":
        model = model or "gemini-flash-latest"
        url = (base_url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/") + f"/models/{model}:generateContent?key={api_key}"
        data = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": temperature
            }
        }
        if response_json:
            data["generationConfig"]["response_mime_type"] = "application/json"

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                candidates = res.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
                return ""
        except urllib.error.HTTPError as e:
            print(f"Gemini API HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
            raise
        except urllib.error.URLError as e:
            print(f"Gemini API URL Error: {e.reason}", file=sys.stderr)
            raise

    elif provider == "anthropic":
        model = model or "claude-3-5-haiku-20241022"
        url = (base_url or "https://api.anthropic.com/v1").rstrip("/") + "/messages"
        data = {
            "model": model,
            "system": system_instruction,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": temperature,
            "max_tokens": 4096
        }
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                content = res.get("content", [])
                if content and "text" in content[0]:
                    return content[0]["text"].strip()
                return ""
        except urllib.error.HTTPError as e:
            print(f"Anthropic API HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
            raise
        except urllib.error.URLError as e:
            print(f"Anthropic API URL Error: {e.reason}", file=sys.stderr)
            raise

    else:  # OpenAI / OpenAI-compatible
        model = model or "gpt-4o-mini"
        url = (base_url or "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        if response_json:
            data["response_format"] = {"type": "json_object"}

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                choices = res.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
                return ""
        except urllib.error.HTTPError as e:
            print(f"OpenAI-compatible API HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
            raise
        except urllib.error.URLError as e:
            print(f"OpenAI-compatible API URL Error: {e.reason}", file=sys.stderr)
            raise
