# services/llm_parser.py
import asyncio
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from config import config

client = genai.Client(api_key=config.gemini_api_key)

class ExtractedLead(BaseModel):
    property_type: Optional[Literal["apartment", "house", "villa"]] = Field(
        default=None,
        description="Property type: 'apartment' (квартира/1+1/2+1), 'house' (дом), or 'villa' (вилла). None if not mentioned."
    )
    districts: Optional[List[str]] = Field(
        default=None,
        description=(
            "List of Alanya districts standardized to English names: "
            "['Mahmutlar', 'Oba', 'Kleopatra', 'Kestel', 'Avsallar', 'Kargicak', 'Tosmur', 'Tepe', 'Bektas']. "
            "Return ['Any'] if user explicitly says any district or doesn't know. Return None if not mentioned at all."
        )
    )
    min_price_eur: Optional[int] = Field(
        default=None,
        description="Minimum budget in EUR as integer (convert '80к'/'80k' to 80000). Set to 0 if only upper limit is given."
    )
    max_price_eur: Optional[int] = Field(
        default=None,
        description="Maximum budget in EUR as integer. If only one approximate number is given, set both min and max to that value."
    )

SYSTEM_PROMPT = """
You are an AI real estate assistant in Alanya, Turkey.
Extract structured parameters from the user's inquiry in Russian, Ukrainian, or English.
Do not guess missing values — leave them as null (None).
"""

CANDIDATE_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]

async def parse_user_query(text: str) -> ExtractedLead:
    for model_name in CANDIDATE_MODELS:
        try:
            print(f"🔄 Пробуем модель: {model_name}...")
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=model_name,
                    contents=text,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=ExtractedLead,
                        temperature=0.0,
                    ),
                ),
                timeout=8.0,
            )
            if response.parsed:
                print(f"🚀 Успешно распознано ({model_name}): {response.parsed}")
                return response.parsed
        except asyncio.TimeoutError:
            print(f"⏱ Таймаут 8 сек на модели {model_name}, переключаемся...")
        except Exception as e:
            print(f"⚠️ Пропуск {model_name}: {e}")

    return ExtractedLead()