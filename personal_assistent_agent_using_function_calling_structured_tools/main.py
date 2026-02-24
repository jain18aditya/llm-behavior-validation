from assistant import run_assistant

while True:
    user = input("User: ")
    output = run_assistant(user)
    print("Assistant:", output)

"""
Summarize this email: Please send the report by tomorrow.

Extract order details:{Order ID: 123,Amount: $50,Status: Shipped}

Plan my day for preparing a presentation
"""