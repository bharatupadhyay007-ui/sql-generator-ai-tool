import requests

def generate_sql(user_question):
    prompt = f"""You are an expert SQL developer.
Convert the following natural language request into a clean SQL query.
Return ONLY the SQL query, nothing else. No explanation, no markdown, just raw SQL.

Request: {user_question}
SQL:"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# Main loop - keeps running until you type exit
while True:
    user_input = input("\nAsk in plain English (or type 'exit' to quit): ")
    
    if user_input.lower() == "exit":
        print("Bye!")
        break
    
    print("\nGenerated SQL:")
    print("-" * 40)
    print(generate_sql(user_input))
    print("-" * 40)
