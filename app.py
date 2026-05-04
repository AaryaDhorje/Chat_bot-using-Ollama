from agent.react_agent import build_agent
from utils.printer import print_banner, print_response


def run_chat():
    agent_executor = build_agent()
    print_banner()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        print("🤖 Thinking...", end="", flush=True)

        try:
            response = agent_executor.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })

            print_response(response)

        except Exception as e:
            print(f"\nError: {e}")
            print("Make sure Ollama is running: ollama serve")


if __name__ == "__main__":
    run_chat()