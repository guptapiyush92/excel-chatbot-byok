"""
Multi-Provider LLM Client
Supports Anthropic Claude, Google Gemini, and OpenAI GPT
"""

from typing import Optional, Dict, Any, List
import os
from enum import Enum


class LLMProvider(Enum):
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OPENAI = "openai"


class MultiProviderLLM:
    """Unified interface for multiple LLM providers."""

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize LLM client for specified provider.

        Args:
            provider: One of 'anthropic', 'gemini', 'openai'
            api_key: API key for the provider
            model: Model name (optional, uses defaults)
            base_url: Custom base URL (for proxies/corporate endpoints)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.base_url = base_url

        # Set default models
        self.model = model or self._get_default_model()

        # Initialize the appropriate client
        self.client = self._initialize_client()

    def _get_default_model(self) -> str:
        """Get default model for the provider."""
        defaults = {
            "anthropic": "claude-sonnet-4-20250514",
            "gemini": "gemini-2.0-flash-exp",
            "openai": "gpt-4o"
        }
        return defaults.get(self.provider, "claude-sonnet-4-20250514")

    def _initialize_client(self):
        """Initialize the provider-specific client."""
        if self.provider == "anthropic":
            from anthropic import Anthropic
            if self.base_url:
                return Anthropic(api_key=self.api_key, base_url=self.base_url)
            return Anthropic(api_key=self.api_key)

        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            return genai.GenerativeModel(self.model)

        elif self.provider == "openai":
            from openai import OpenAI
            if self.base_url:
                return OpenAI(api_key=self.api_key, base_url=self.base_url)
            return OpenAI(api_key=self.api_key)

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        if self.provider == "anthropic":
            return self._generate_anthropic(messages, max_tokens, temperature, **kwargs)
        elif self.provider == "gemini":
            return self._generate_gemini(messages, max_tokens, temperature, **kwargs)
        elif self.provider == "openai":
            return self._generate_openai(messages, max_tokens, temperature, **kwargs)

    def _generate_anthropic(self, messages, max_tokens, temperature, **kwargs) -> str:
        """Generate using Anthropic Claude."""
        # Extract system message if present
        system_message = None
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        # Make API call
        kwargs_filtered = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": user_messages
        }

        if system_message:
            kwargs_filtered["system"] = system_message

        response = self.client.messages.create(**kwargs_filtered)
        return response.content[0].text

    def _generate_gemini(self, messages, max_tokens, temperature, **kwargs) -> str:
        """Generate using Google Gemini."""
        # Combine messages into a prompt
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")

        prompt = "\n".join(prompt_parts)

        # Generate response
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        response = self.client.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text

    def _generate_openai(self, messages, max_tokens, temperature, **kwargs) -> str:
        """Generate using OpenAI GPT."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    @staticmethod
    def get_available_providers() -> Dict[str, Dict[str, Any]]:
        """Get information about available providers."""
        return {
            "anthropic": {
                "name": "Anthropic Claude",
                "models": [
                    "claude-sonnet-4-20250514",
                    "claude-opus-4-20250514",
                    "claude-3-5-sonnet-20241022",
                    "claude-3-5-haiku-20241022"
                ],
                "default": "claude-sonnet-4-20250514",
                "api_key_url": "https://console.anthropic.com/",
                "supports_base_url": True
            },
            "gemini": {
                "name": "Google Gemini",
                "models": [
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash"
                ],
                "default": "gemini-2.0-flash-exp",
                "api_key_url": "https://aistudio.google.com/apikey",
                "supports_base_url": False
            },
            "openai": {
                "name": "OpenAI GPT",
                "models": [
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo"
                ],
                "default": "gpt-4o",
                "api_key_url": "https://platform.openai.com/api-keys",
                "supports_base_url": True
            }
        }


def create_llm_client(
    provider: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None
) -> MultiProviderLLM:
    """
    Factory function to create LLM client.

    Args:
        provider: Provider name ('anthropic', 'gemini', 'openai')
        api_key: API key (if None, tries to get from environment)
        model: Model name (if None, uses default)
        base_url: Custom base URL (optional)

    Returns:
        MultiProviderLLM instance
    """
    # Try to get API key from environment if not provided
    if not api_key:
        env_vars = {
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        api_key = os.getenv(env_vars.get(provider.lower()))

    if not api_key:
        raise ValueError(f"API key for {provider} not provided and not found in environment")

    return MultiProviderLLM(provider, api_key, model, base_url)
