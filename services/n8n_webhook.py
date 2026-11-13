import httpx
from config import config
from database.models import Lead

async def send_lead_to_n8n(lead: Lead):
    if not config.n8n_webhook_url:
        return

    payload = {
        "lead_id": lead.id,
        "telegram_id": lead.telegram_id,
        "username": f"@{lead.username}" if lead.username else "Без юзернейма",
        "phone": lead.phone,
        "language": lead.language,
        "intent": "Покупка" if lead.intent == "buy" else "Продажа",
        "property_type": lead.property_type,
        "districts": ", ".join(lead.districts),
        "min_price_eur": lead.min_price_eur,
        "max_price_eur": lead.max_price_eur,
        "price_formatted": f"€{lead.min_price_eur:,} - €{lead.max_price_eur:,}",
        "raw_query": lead.raw_query or "Заполнено через кнопки",
        "created_at": lead.created_at.strftime("%Y-%m-%d %H:%M")
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(config.n8n_webhook_url, json=payload)
            response.raise_for_status()
    except Exception as e:
        print(f"Ошибка отправки вебхука в n8n: {e}")