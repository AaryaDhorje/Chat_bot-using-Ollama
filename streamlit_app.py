import streamlit as st

from agent.react_agent import build_agent
from config import MODEL_NAME, TEMPERATURE


st.set_page_config(
    page_title="Smart AI Agent",
    page_icon="🤖",
    layout="centered",
)


@st.cache_resource(show_spinner="Starting agent…")
def get_agent():
    return build_agent()


with st.sidebar:
    st.title("🤖 Smart AI Agent")
    st.caption("Local LLM via Ollama, with live web search")
    st.divider()

    st.markdown("**Model**")
    st.code(MODEL_NAME, language="text")
    st.markdown(f"**Temperature:** `{TEMPERATURE}`")
    st.markdown("**Tools:** DuckDuckGo Search")
    st.divider()

    if st.button("🗑️  Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Make sure `ollama serve` is running in the background.")


st.title("💬 Chat")
st.caption("Ask anything — the agent will search the web when it needs to.")

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_tools(tools):
    if not tools:
        return
    label = f"🔎 Used {len(tools)} tool call{'s' if len(tools) > 1 else ''}"
    with st.expander(label, expanded=False):
        for t in tools:
            st.markdown(f"**{t['name']}**")
            st.code(t["content"][:1500], language="text")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_tools(msg.get("tools", []))
        st.markdown(msg["content"])


if user_input := st.chat_input("Type your message…"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                agent = get_agent()
                lc_input = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                input_len = len(lc_input)
                response = agent.invoke({"messages": lc_input})

                new_messages = response["messages"][input_len:]

                tools_used = [
                    {"name": m.name, "content": str(m.content)}
                    for m in new_messages
                    if getattr(m, "type", "") == "tool"
                ]

                final_content = ""
                for m in reversed(new_messages):
                    if getattr(m, "type", "") == "ai" and m.content:
                        final_content = m.content
                        break

                render_tools(tools_used)
                st.markdown(final_content or "_(no response)_")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_content,
                    "tools": tools_used,
                })
            except Exception as e:
                st.error(
                    f"**Error:** {e}\n\n"
                    "Make sure Ollama is running (`ollama serve`) and the model is pulled."
                )
