def print_banner():
    print("🌐 Smart AI Agent Online (Type 'quit' to exit)")
    print("-" * 60)


def print_response(response):
    for m in response["messages"]:
        if getattr(m, "type", "") == "tool":
            print(f"\n🔎 Tool used: {m.name}")

    for m in reversed(response["messages"]):
        if getattr(m, "type", "") == "ai":
            print(f"\r🤖 Agent: {m.content}")
            return