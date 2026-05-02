# ReplyGenius-AI
# ReplyGenius AI 📩🤖

ReplyGenius AI is an intelligent email assistant that reads emails, generates context-aware replies, and allows user approval before sending responses.

---

## 🚀 Features

* 📩 Reads emails using IMAP (Gmail)
* 🤖 Generates smart replies (AI + rule-based system)
* 👤 Human-in-the-loop approval before sending
* 📤 Sends replies using SMTP
* 🛡️ Safe fallback system to avoid incorrect responses

---

## 🧠 How It Works

1. Reads unread emails from inbox
2. Analyzes email content
3. Generates a reply using:

   * Rule-based logic (for common cases)
   * Local AI model fallback (Ollama)
4. Shows suggested reply
5. User can:

   * Send
   * Edit
   * Skip

---

## 🛠️ Tech Stack

* Python
* IMAP & SMTP (Email handling)
* Ollama (Local LLM - optional)
* Rule-based NLP logic

---

## ⚙️ Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Appy0413/ReplyGenius-AI.git
cd ReplyGenius-AI
```

2. Install dependencies

```bash
pip install ollama
```

3. Create a `.env` file in the project root`

```python
EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
```

4. Run the app

```bash
python app.py
```

---

## 🎯 Future Improvements

* Email categorization (priority, spam, etc.)
* Multi-reply suggestions (like Gmail Smart Reply)
* Web interface (React)
* Integration with advanced LLM APIs

---

## 💡 Key Learning

This project demonstrates a hybrid AI approach where deterministic logic ensures reliability and AI is used selectively for flexible responses.

---

## 📌 Author

Aprajita Singh
Aspiring AI Engineer
