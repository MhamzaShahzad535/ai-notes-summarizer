import csv
import os
from datetime import datetime, timezone
from pathlib import Path

from google import genai


MODEL_NAME = "gemini-3.5-flash-lite"
LOG_FILE = Path("llm_usage.csv")

# Paid-tier equivalent prices per 1 million tokens.
# Your current free-tier requests may actually cost $0.
INPUT_PRICE_PER_MILLION = 0.30
OUTPUT_PRICE_PER_MILLION = 2.50


def log_usage(prompt_tokens, output_tokens, thinking_tokens, total_tokens):
    estimated_cost = (
        (prompt_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
        + ((output_tokens + thinking_tokens) / 1_000_000)
        * OUTPUT_PRICE_PER_MILLION
    )

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "model",
                "prompt_tokens",
                "output_tokens",
                "thinking_tokens",
                "total_tokens",
                "estimated_paid_cost_usd",
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            MODEL_NAME,
            prompt_tokens,
            output_tokens,
            thinking_tokens,
            total_tokens,
            f"{estimated_cost:.8f}",
        ])


def summarize_note(content: str) -> str:
    # Input validation
    content = content.strip()

    if not content:
        raise ValueError("Note content cannot be empty")

    if len(content) > 10000:
        raise ValueError("Note content is too long")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Summarize the following note in 2-3 short sentences.
Keep only the most important information.

NOTE:
{content}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    # Output validation
    if not response.text:
        raise ValueError("Gemini returned an empty response")

    summary = response.text.strip()

    if len(summary) < 10:
        raise ValueError("Gemini returned an invalid summary")

    # Token usage / cost logging
    usage = response.usage_metadata

    if usage:
        prompt_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        thinking_tokens = usage.thoughts_token_count or 0
        total_tokens = usage.total_token_count or 0

        log_usage(
            prompt_tokens,
            output_tokens,
            thinking_tokens,
            total_tokens,
        )

    return summary