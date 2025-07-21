# Ecommerce Helper

**AI assistant for e-commerce management: Mercado Libre, Tienda Nube, and Ecomm App**

This project provides a modular and lightweight bot for querying and receiving automated answers about sales, stock, and billing. It starts with Telegram (MVP) and is ready to extend to other channels (WhatsApp, Discord, Slack).

---

## 🧱 Features

* **Decoupled adapters** for messaging channels and data sources.
* **Core module (Engine)** that orchestrates: message → intent → query → response.
* **AI provider** using OpenAI GPT-3.5/GPT-4 to interpret and generate responses.
* **Data adapters** for Mercado Libre, Tienda Nube, and Ecomm App.
* **In-memory context** storage, no external database required (ideal for a 5-user MVP).
* **Configuration via `.env`** for tokens and credentials.

---

## 📂 Project Structure

```plaintext
 e-commerce_helper/
 ├── adapters/
 │   ├── channel/
 │   │   └── telegram_adapter.py       # Send and receive messages on Telegram
 │   ├── datasource/
 │   │   ├── meli_adapter.py           # Mercado Libre API queries
 │   │   ├── tienda_nube_adapter.py    # Tienda Nube API queries
 │   │   └── ecomm_adapter.py          # Ecomm App API queries
 │   └── ai_provider.py                # OpenAI API wrapper
 ├── core/
 │   ├── engine.py                     # Orchestrates data flow and AI
 │   └── context_store.py              # In-memory context management
 ├── prompts/
 │   └── system_prompt.txt             # Base prompt for GPT
 ├── main.py                           # Entry point (CLI / webhook)
 ├── requirements.txt                  # Python dependencies
 ├── .env.example                      # Example environment variables
 └── README.md                         # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>.git
cd ecommerce_helper
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # or 'venv\Scripts\activate' on Windows
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your credentials:
# TELEGRAM_TOKEN=
# OPENAI_API_KEY=
# MELI_CLIENT_ID=
# MELI_CLIENT_SECRET=
# TIENDA_NUBE_TOKEN=
# ECOMM_API_URL=
# ECOMM_API_KEY=
```

### 4. Run in CLI mode (for testing)

```bash
python main.py --mode cli
# Then type questions such as:
# "How many sales did I have this week?"
```

### 5. Deploy to AWS Lambda (optional)

1. Package your code: `zip -r deploy.zip .`
2. Use Terraform or AWS CLI to deploy as described in the deployment section.

---

## 🤝 Contributing

1. Create a branch for your feature: `feature/branch-name`
2. Commit and push: `git push origin feature/branch-name`
3. Open a pull request.

---

## 📝 License

This project is licensed under MIT. See the `LICENSE` file for details.
