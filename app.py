from flask import Flask, request, jsonify
import requests
import json
import os
from datetime import datetime
import time

app = Flask(__name__)

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_sql(user_question):
    prompt = f"""You are an expert SQL developer.
Convert the following natural language request into a clean SQL query.
Return ONLY the SQL query, nothing else. No explanation, no markdown, just raw SQL.

Request: {user_question}
SQL:"""

    start = time.time()
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    elapsed = round(time.time() - start, 1)
    return response.json()["response"], elapsed


@app.route("/")
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Bharat Upadhyay's SQL Generator AI Tool</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f5f5f5;
            color: #1a1a1a;
            min-height: 100vh;
            padding: 40px 20px;
        }

        .app {
            max-width: 860px;
            margin: 0 auto;
        }

        .topbar {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 2rem;
            padding-bottom: 1.25rem;
            border-bottom: 0.5px solid #e0e0e0;
        }

        .logo {
            width: 48px;
            height: 48px;
            background: #1D9E75;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .brand {
            font-size: 26px;
            font-weight: 700;
            color: #1a1a1a;
        }

        .brand span {
            color: #1D9E75;
            font-size: 28px;
            font-weight: 800;
        }

        .badge {
            margin-left: auto;
            font-size: 11px;
            background: #e8f7f2;
            color: #1D9E75;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 500;
            border: 0.5px solid #1D9E75;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 1.5rem;
        }

        .stat {
            background: #ffffff;
            border: 0.5px solid #e0e0e0;
            border-radius: 10px;
            padding: 14px 16px;
        }

        .stat-val {
            font-size: 22px;
            font-weight: 500;
            color: #1a1a1a;
        }

        .stat-label {
            font-size: 12px;
            color: #888888;
            margin-top: 2px;
        }

        .input-card {
            background: #ffffff;
            border: 0.5px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }

        .input-label {
            font-size: 11px;
            color: #888888;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        textarea {
            width: 100%;
            background: #f5f5f5;
            border: 0.5px solid #dddddd;
            border-radius: 8px;
            padding: 12px 14px;
            font-size: 14px;
            color: #1a1a1a;
            resize: vertical;
            font-family: inherit;
            min-height: 80px;
            outline: none;
            transition: border-color 0.15s;
        }

        textarea:focus { border-color: #1D9E75; }

        .actions {
            display: flex;
            gap: 10px;
            margin-top: 12px;
        }

        .btn-primary {
            background: #1D9E75;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.15s;
        }

        .btn-primary:hover { background: #189e6e; }
        .btn-primary:disabled { background: #a8dac9; cursor: not-allowed; }

        .btn-secondary {
            background: transparent;
            color: #777777;
            border: 0.5px solid #dddddd;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: border-color 0.15s;
        }

        .btn-secondary:hover { border-color: #aaaaaa; color: #444444; }

        .loading {
            display: none;
            align-items: center;
            gap: 8px;
            padding: 12px 0;
            font-size: 13px;
            color: #888888;
        }

        .spinner {
            width: 14px;
            height: 14px;
            border: 2px solid #e0e0e0;
            border-top-color: #1D9E75;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .result-card {
            background: #ffffff;
            border: 0.5px solid #e0e0e0;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 1rem;
            display: none;
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 16px;
            border-bottom: 0.5px solid #eeeeee;
            background: #fafafa;
        }

        .result-title {
            font-size: 11px;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #1D9E75;
        }

        .export-btn {
            font-size: 12px;
            color: #1D9E75;
            background: #e8f7f2;
            border: 0.5px solid #1D9E75;
            padding: 4px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 500;
        }

        .sql-output {
            padding: 1.25rem;
            font-family: "SF Mono", "Fira Code", monospace;
            font-size: 13px;
            line-height: 1.8;
            color: #333333;
            white-space: pre-wrap;
            background: #fafafa;
        }

        .history-section { margin-top: 2rem; }

        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }

        .section-title {
            font-size: 11px;
            font-weight: 500;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .clear-link {
            font-size: 12px;
            color: #c0392b;
            cursor: pointer;
            background: none;
            border: none;
        }

        .history-item {
            background: #ffffff;
            border: 0.5px solid #eeeeee;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: border-color 0.15s;
        }

        .history-item:hover { border-color: #1D9E75; }

        .h-question { font-size: 13px; color: #666666; margin-bottom: 4px; }
        .h-sql { font-size: 12px; font-family: monospace; color: #333333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .h-time { font-size: 11px; color: #999999; margin-top: 6px; }

        .no-history { font-size: 13px; color: #aaaaaa; text-align: center; padding: 2rem 0; }
    </style>
</head>
<body>
<div class="app">

    <div class="topbar">
        <div class="logo">🛢️</div>
        <div>
            <div class="brand"><span>Bharat Upadhyay's</span> SQL Generator AI Tool</div>
        </div>
        <div class="badge">Powered by LLaMA 3.2</div>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="stat-val" id="stat-count">0</div>
            <div class="stat-label">Queries generated</div>
        </div>
        <div class="stat">
            <div class="stat-val" id="stat-time">—</div>
            <div class="stat-label">Last response time</div>
        </div>
        <div class="stat">
            <div class="stat-val">100%</div>
            <div class="stat-label">Local &amp; private</div>
        </div>
    </div>

    <div class="input-card">
        <div class="input-label">Ask in plain English</div>
        <textarea id="question" placeholder="e.g. show me top 5 customers by revenue"></textarea>
        <div class="actions">
            <button class="btn-primary" id="generateBtn" onclick="generateSQL()">
                ⚡ Generate SQL
            </button>
            <button class="btn-secondary" onclick="clearInput()">Clear</button>
            <button class="btn-secondary" id="exportBtn" onclick="exportSQL()" style="display:none; color:#1D9E75; border-color:#1D9E75;">
                📤 Export .sql
            </button>
        </div>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            Generating SQL...
        </div>
    </div>

    <div class="result-card" id="resultCard">
        <div class="result-header">
            <div class="result-title"><div class="dot"></div> Generated SQL</div>
            <button class="export-btn" onclick="exportSQL()">Export .sql</button>
        </div>
        <div class="sql-output" id="result"></div>
    </div>

    <div class="history-section">
        <div class="section-header">
            <div class="section-title">Query history</div>
            <button class="clear-link" onclick="clearHistory()">Clear all</button>
        </div>
        <div id="history"></div>
    </div>

</div>

<script>
    let currentSQL = "";

    async function generateSQL() {
        const question = document.getElementById("question").value.trim();
        if (!question) return;

        document.getElementById("generateBtn").disabled = true;
        document.getElementById("loading").style.display = "flex";
        document.getElementById("resultCard").style.display = "none";
        document.getElementById("exportBtn").style.display = "none";

        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        currentSQL = data.sql;

        document.getElementById("generateBtn").disabled = false;
        document.getElementById("loading").style.display = "none";
        document.getElementById("resultCard").style.display = "block";
        document.getElementById("result").innerText = currentSQL;
        document.getElementById("exportBtn").style.display = "block";
        document.getElementById("stat-time").innerText = data.elapsed + "s";

        loadHistory();
    }

    function clearInput() {
        document.getElementById("question").value = "";
        document.getElementById("resultCard").style.display = "none";
        document.getElementById("exportBtn").style.display = "none";
    }

    function exportSQL() {
        const blob = new Blob([currentSQL], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "query.sql";
        a.click();
        URL.revokeObjectURL(url);
    }

    async function loadHistory() {
        const response = await fetch("/history");
        const data = await response.json();
        const container = document.getElementById("history");

        document.getElementById("stat-count").innerText = data.history.length;

        if (data.history.length === 0) {
            container.innerHTML = "<div class='no-history'>No queries yet. Ask something above!</div>";
            return;
        }

        container.innerHTML = data.history.slice().reverse().map(item => `
            <div class="history-item" onclick="loadQuery(\`${item.sql.replace(/`/g, "\\`")}\`)">
                <div class="h-question">💬 ${item.question}</div>
                <div class="h-sql">${item.sql}</div>
                <div class="h-time">🕐 ${item.timestamp}</div>
            </div>
        `).join("");
    }

    function loadQuery(sql) {
        currentSQL = sql;
        document.getElementById("result").innerText = sql;
        document.getElementById("resultCard").style.display = "block";
        document.getElementById("exportBtn").style.display = "block";
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    async function clearHistory() {
        await fetch("/clear_history", { method: "POST" });
        loadHistory();
    }

    loadHistory();
</script>
</body>
</html>
'''


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    question = data.get("question", "")
    sql, elapsed = generate_sql(question)

    history = load_history()
    history.append({
        "question": question,
        "sql": sql,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })
    save_history(history)

    return jsonify({"sql": sql, "elapsed": elapsed})


@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({"history": load_history()})


@app.route("/clear_history", methods=["POST"])
def clear_history():
    save_history([])
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)
