from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="sk-45acf866dcdb4ac29a985ea59030b69e",
    base_url="https://api.deepseek.com/v1",
    temperature=0.2
)

response = llm.invoke([
    HumanMessage(content="Explain LangChain in one sentence")
])

print(response.content)
