# Gemini Agent with Finance Tools

This repository contains examples of using Google's Gemini API with LangGraph and LangChain to create AI agents for financial data analysis.

## Scripts Overview

### 1. Basic Agent (agent.py)
- Uses OpenAI's GPT-4 Mini
- Implements Yahoo Finance News tool
- Simple question-answering about companies

### 2. Gemini Basic Agent (agent_gemini.py)
- Replaces OpenAI with Google's Gemini API
- Implements Yahoo Finance News tool
- Similar functionality to the basic agent

### 3. Enhanced Gemini Agent (agent_gemini_enhanced.py)
- Uses Google's Gemini API
- Implements both Yahoo Finance News and custom Stock Info tools
- Provides more detailed financial analysis
- Handles errors gracefully

### 4. Simplified Gemini Agent (agent_gemini_simple.py)
- Streamlined version that only uses the Yahoo Finance News tool
- More reliable for basic financial news queries

### 5. Final Gemini Agent (agent_gemini_final.py)
- Improved version with custom tool wrapper and clear system prompts
- Uses a tool with a more intuitive name (get_company_news)
- Includes examples in the system prompt to guide the model
- Reliable for retrieving news about specific companies

### 6. Company Comparison Agent (agent_gemini_compare.py)
- Specialized for comparing news between different companies
- Uses ticker symbols to retrieve relevant information

## Setup

1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install langchain-community langgraph langchain-google-genai google-generativeai yfinance python-dotenv`
4. Add your API keys to a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key_here
   GOOGLE_API_KEY=your_gemini_key_here
   ```

## Usage

Run any of the scripts using Python, for example:

```bash
python agent_gemini_final.py
```

## Notes

- The Yahoo Finance News API may occasionally have connection issues
- Gemini API has rate limits that might require adjusting the model (Flash vs Pro)
- For more advanced financial analysis, additional tools would be needed
- When designing agents, make sure the system prompt and tool descriptions are clear and include examples 