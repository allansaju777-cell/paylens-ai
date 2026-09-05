from ai_agent import ask_agent


print("================================")
print("          PAYLENS AI")
print("================================")


question = input(
    "\nAsk a question about your business: "
)


answer = ask_agent(
    question
)


print("\n🤖 PAYLENS AI:")

print(answer)