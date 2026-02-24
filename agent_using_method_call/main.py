from agent import run_agent

inputs = ["What is 9+12", "Read file sample.txt, Search Python programming"]
while True:
    user = input("User: ")
    print("Final:", run_agent(user))
