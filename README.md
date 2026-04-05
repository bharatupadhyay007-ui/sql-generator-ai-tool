# 🛢️ Bharat Upadhyay's SQL Generator AI Tool

A web application that converts plain English questions into SQL queries using a locally running LLM (LLaMA 3.2).

No cloud. No API costs. Runs 100% on your machine.

---

## 💡 What it does

Type a question in plain English and get production ready SQL instantly.

**Example:**
- Input: `show me top 5 customers by revenue`
- Output: `SELECT customer_name, SUM(revenue) AS total_revenue FROM customers GROUP BY customer_name ORDER BY total_revenue DESC LIMIT 5;`

---

## ✨ Features

- Natural language to SQL conversion
- Query history saved locally
- Export SQL as .sql file
- Response time tracker
- Clean minimal UI
- 100% local and private — no data leaves your machine

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web server and API routes |
| LLaMA 3.2 | AI model for SQL generation |
| Ollama | Local LLM server |
| JavaScript | Frontend interactivity |
| HTML/CSS | UI and styling |

---

## 🚀 How to Run

**Step 1 — Install Ollama and pull the model**
```bash
brew install ollama
ollama pull llama3.2
```

**Step 2 — Start Ollama server**
```bash
ollama serve
```

**Step 3 — Clone the repo and set up environment**
```bash
git clone https://github.com/bharatupadhyay007-ui/sql-generator-ai-tool.git
cd sql-generator-ai-tool
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

**Step 4 — Run the app**
```bash
python3 app.py
```

**Step 5 — Open in browser**
