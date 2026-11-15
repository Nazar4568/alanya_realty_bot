# Alanya Real Estate Lead-Gen Telegram Bot

An asynchronous Telegram bot designed to collect and qualify real estate leads for the Alanya (Turkey) property market. 

The bot supports two input modes: natural language parsing via the Gemini API (extracting structured entities from free-form text) and a step-by-step interactive button flow using `aiogram` FSM. Validated leads are stored in PostgreSQL and forwarded via webhook to a self-hosted `n8n` instance for Google Sheets synchronization and manager notifications.

## Features & Implementation

* **Hybrid Lead Qualification (`handlers/dialog.py`, `states.py`):**
  * **AI Mode:** Users can describe their request in a single message (e.g., *"Looking to buy a villa in Mahmutlar or Oba for 80k-120k EUR"*). The bot extracts available fields and only prompts the user with inline buttons for missing parameters (`route_next_missing_field`).
  * **Manual Mode:** If the user prefers buttons—or if the LLM API is unavailable—the bot falls back to a standard step-by-step questionnaire (Intent $\rightarrow$ Property Type $\rightarrow$ Multi-select Districts $\rightarrow$ Budget Range $\rightarrow$ Contact Info).
* **Structured LLM Parsing (`services/llm_parser.py`):**
  * Uses the `google-genai` SDK (`client.aio`) with Pydantic schema enforcement (`LeadExtraction`) to guarantee typed JSON outputs (`intent`, `property_type`, `districts`, `min_price_eur`, `max_price_eur`).
  * Includes a fallback loop across multiple models (`gemini-3.1-flash-lite`, `gemini-2.5-flash`) with error handling so API failures never crash the dialog.
* **Multi-language Support (`locales.py`):**
  * Full UI localization for Russian (`ru`), Ukrainian (`uk`), and English (`en`).
* **Database Layer (`database/models.py`, `database/engine.py`):**
  * Asynchronous PostgreSQL integration using SQLAlchemy 2.0 (`AsyncSession`, `asyncpg`).
  * Automatically creates tables on startup and stores normalized lead records alongside raw user queries.
* **Webhook Automation (`services/n8n_webhook.py`):**
  * Sends saved lead payloads asynchronously via `httpx` to an `n8n` webhook endpoint, which appends rows to Google Sheets and sends formatted alerts to a Telegram channel/chat.
<img width="526" height="505" alt="Screenshot 2026-11-15 at 19 17 54" src="https://github.com/user-attachments/assets/bd2f771f-ab66-4e22-a334-5e9bc11be7c7" />
## Tech Stack

* **Language:** Python 3.11+
* **Bot Framework:** `aiogram` 3.x
* **Database:** PostgreSQL 16, SQLAlchemy 2.0 (async), `asyncpg`
* **LLM & Validation:** Google Gemini API (`google-genai`), Pydantic v2
* **HTTP Client:** `httpx`
* **Automation & Infrastructure:** `n8n`, Docker, Docker Compose

## Project Structure

```text
alanya_realty_bot/
├── database/
│   ├── engine.py          # Async SQLAlchemy engine, session maker, DB save logic
│   └── models.py          # Declarative ORM models for leads
├── handlers/
│   └── dialog.py          # FSM handlers, inline keyboards, missing-field router
├── services/
│   ├── llm_parser.py      # Async Gemini API client with Pydantic output schema
│   └── n8n_webhook.py     # Async HTTP client for pushing leads to n8n
├── config.py              # Environment configuration via pydantic-settings
├── locales.py             # Localization dictionaries (RU / UK / EN) & district list
├── states.py              # FSM states definition (LeadForm)
├── main.py                # Entry point, database initialization, polling startup
├── Dockerfile             # Python container build instructions
├── docker-compose.yml     # Multi-container stack (bot, postgres, n8n)
├── requirements.txt       # Python dependencies
└── .env.example           # Template for required environment variables
```
How to Run & Test
1. Prerequisites
Docker and Docker Compose installed (or Python 3.11+ and a local PostgreSQL instance).

A Telegram Bot Token from @BotFather.

A Gemini API Key from Google AI Studio.

2. Environment Setup
Clone the repository and create a .env file based on .env.example:
Bash```
git clone [https://github.com/Nazar4568/alanya_realty_bot.git](https://github.com/Nazar4568/alanya_realty_bot.git)
cd alanya_realty_bot
cp .env.example .env```

Fill in your .env file:
Code snippet```
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
N8N_WEBHOOK_URL=http://n8n:5678/webhook/alanya-lead```
(Note: Use http://n8n:5678/... when running inside Docker Compose, or http://localhost:5678/... if running the Python script directly on your host machine).
3. Run with Docker Compose (Recommended)
Build and start the entire stack (postgres, n8n, and bot):
bash```
docker compose up -d --build```

Check the bot logs to verify it started polling:
bash```
docker compose logs -f bot```
4. Configure n8n (Optional)
If you want to test the webhook integration with Google Sheets and Telegram notifications:

Open http://localhost:5678 in your browser.

Create an n8n workflow starting with a Webhook node (POST, path: alanya-lead).

Connect it to a Google Sheets node (Append Row) and/or a Telegram node (Send Message), then click Publish.

5. Testing the Bot Scenarios
Open your bot in Telegram and send /start:

Test Full AI Extraction:

Select a language and click Buy.

Send a text message: "I want to buy villa in muhmutlar for 100k-120k"

The bot will parse all parameters at once and immediately show the summary card asking for your phone number.

Test Partial AI Extraction (Hybrid Flow):

Start over (/start), choose Buy, and send: "Looking for an apartment in Center" (no budget specified).

The bot will extract property_type="apartment" and districts=["Center"], skip those questions, and only prompt you with buttons to select your budget range.

Test Manual Button Flow:

Start over (/start), choose Buy, and click the Fill step-by-step (no AI) button to complete the questionnaire using only inline keyboards.
