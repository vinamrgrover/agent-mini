import os
import json
import uuid
import boto3
from datetime import datetime
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool

load_dotenv()

S3_LOG_BUCKET = os.environ.get("S3_LOG_BUCKET")
S3_LOG_PREFIX = os.environ.get("S3_LOG_PREFIX", "logs/")

s3_client = boto3.client("s3")


# Custom function to handle Yahoo Finance News with error handling
def get_yahoo_finance_news(ticker):
    try:
        yahoo_tool = YahooFinanceNewsTool()
        result = yahoo_tool.run(ticker)
        if "Error" in result or "no news found" in result.lower():
            return f"No recent news found for {ticker}."
        return result
    except Exception as e:
        return f"Error retrieving news for {ticker}: {str(e)}"


yahoo_news_tool = Tool(
    name="yahoo_finance_news",
    description="""
    Use this tool to find the latest news about companies by their stock ticker symbol.
    Examples of valid tickers: AAPL (Apple), MSFT (Microsoft), NVDA (Nvidia), AMZN (Amazon), GOOGL (Google), etc.
    The input should be a valid stock ticker symbol only.
    """,
    func=get_yahoo_finance_news,
)

tools = [yahoo_news_tool]

system_message_content = """
You are a helpful assistant with access to a Yahoo Finance News tool.
This tool ONLY works with stock ticker symbols (not company names).

Common ticker symbols you should know:
-  AAPL for Apple
-  MSFT for Microsoft
-  NVDA for Nvidia
-  AMZN for Amazon
-  GOOGL for Google
-  META for Meta (Facebook)
-  TSLA for Tesla

When asked about company news, you must:
1. Immediately identify the correct ticker symbol for each company mentioned (do not ask the user)
2. Call the yahoo_finance_news tool with the ticker symbol (e.g., "AAPL" for Apple)
3. If asked about multiple companies, make separate calls for each company's ticker
4. Summarize the news results you find

EXAMPLES:
User: "What's the latest news about Microsoft?"
You should use the yahoo_finance_news tool with "MSFT" as input

User: "Tell me news about Apple and Google"
You should make two separate tool calls:
-  First call with "AAPL" to get Apple news
-  Second call with "GOOGL" to get Google news

IMPORTANT: Do not ask the user for ticker symbols. Use your knowledge to convert company names to tickers.
"""

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    max_output_tokens=1024,
    model_kwargs={"system": system_message_content},
)

agent = create_react_agent(gemini_model, tools)

input_message = {
    "role": "user",
    "content": "What are the latest news stories about Apple and Microsoft",
}

print("Running Gemini agent with improved Yahoo Finance News tool...\n")

# Collect logs
invocation_log = {
    "timestamp": datetime.utcnow().isoformat(),
    "input_message": input_message,
    "steps": [],
    "response": None,
}

for step in agent.stream(
    {"messages": [input_message]},
    stream_mode="values",
):
    # Save each step's message in the log
    msg = step["messages"][-1]
    invocation_log["steps"].append({"role": "human", "content": msg.content})
    msg.pretty_print()
    invocation_log["response"] = (
        msg.content
    )  # Last one will be the final response
