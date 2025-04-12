import os
import requests

from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


@tool
def get_weather(latitude: float, longitude: float) -> str:
    """指定された緯度・経度から天気を取得します。"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m"
    response = requests.get(url)
    data = response.json()

    temp = data["current"]["temperature_2m"]
    wind_speed = data["current"]["wind_speed_10m"]
    return f"Temperature: {temp}°C, Wind Speed: {wind_speed} m/s"


def main():
    # 使用するツール
    tools = [get_weather]

    # プロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    # モデル定義
    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-1106", temperature=0)
    # エージェント定義
    agent = create_openai_tools_agent(model, tools, prompt)
    # エージェントに、ツールを渡して実行
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # プロンプトを渡して、エージェントが実行
    response = agent_executor.invoke({"input": "東京の天気を教えてください。"})
    return response


if __name__ == "__main__":
    response = main()

    print(response["input"])
    print(response["output"])
