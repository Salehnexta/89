"""Test script for DeepSeek API connectivity."""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Test DeepSeek API directly
try:
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        temperature=0.7
    )
    
    # Test a simple query
    response = llm.invoke("Hello, can you tell me about Paris in June?")
    print("\nDeepSeek API test successful! Response:")
    print(response.content)
    
except Exception as e:
    print(f"\nDeepSeek API test failed: {str(e)}")
    print("Please check your API key and network connection.")
