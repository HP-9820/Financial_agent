import streamlit as st
from duckduckgo_search import DuckDuckGoSearch
import yfinance as yf
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define WebSearchAgent
class WebSearchAgent:
    def __init__(self):
        self.name = "WebSearch Agent"
        self.role = "Search the web for information"
        self.search_engine = DuckDuckGoSearch()

    def search(self, query):
        try:
            results = self.search_engine.text(query, max_results=5)
            return results
        except Exception as e:
            return f"Error during search: {e}"

# Define FinancialAgent
class FinancialAgent:
    def __init__(self):
        self.name = "Financial AI Agent"
        self.role = "Gather financial data"

    def get_stock_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1mo")
            return data
        except Exception as e:
            return f"Error fetching stock data: {e}"

    def get_company_news(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            return stock.news
        except Exception as e:
            return f"Error fetching news: {e}"

# Streamlit app
st.title("Multi-modal AI Agents")

# Initialize agents
websearch_agent = WebSearchAgent()
financial_agent = FinancialAgent()

# Web Search Section
st.header("Web Search")
query = st.text_input("Enter a search query:")
if st.button("Search Web"):
    results = websearch_agent.search(query)
    if isinstance(results, str):
        st.error(results)
    else:
        for idx, result in enumerate(results):
            st.write(f"{idx+1}. {result['title']}")
            st.write(result['href'])

# Financial Data Section
st.header("Financial Data")
ticker = st.text_input("Enter a stock ticker (e.g., NVDA):")
if st.button("Get Stock Data"):
    stock_data = financial_agent.get_stock_data(ticker)
    if isinstance(stock_data, str):
        st.error(stock_data)
    else:
        st.write(stock_data)

if st.button("Get Company News"):
    news = financial_agent.get_company_news(ticker)
    if isinstance(news, str):
        st.error(news)
    else:
        for item in news:
            st.write(f"- {item['title']}: {item['link']}")
