import requests

def ask(prompt):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# Experiment 1 - Zero shot
print("=== Zero Shot ===")
print(ask("Write a SQL query to find top 5 customers by revenue."))

# Experiment 2 - Role based
print("\n=== Role Based ===")
print(ask("You are a senior data engineer. Write a SQL query to find top 5 customers by revenue. Use CTEs, not subqueries."))

# Experiment 3 - Few shot
print("\n=== Few Shot ===")
print(ask("""Convert these requests to SQL:
Request: Find all orders from last month
SQL: SELECT * FROM orders WHERE created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')

Request: Find top 5 customers by revenue
SQL:"""))
