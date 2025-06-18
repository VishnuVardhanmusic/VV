from src.review_engine import runReview

def main():
    # 🛠 Configuration
    inputCodePath = "test_cases/sample.c"
    guidelinePath = "guidelines/c_guidelines.json"
    outputPath = "output/code_review.json"

    # 🔐 LiteLLM Proxy Credentials
    proxy_url = "http://localhost:8000/v1/chat/completions"
    model_name = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    api_key = "your-liteLLM-key"  # Replace with your real LiteLLM API key

    # 🚀 Run the code review
    runReview(
        inputCodePath=inputCodePath,
        guidelinePath=guidelinePath,
        outputPath=outputPath,
        proxy_url=proxy_url,
        model_name=model_name,
        api_key=api_key
    )

if __name__ == "__main__":
    main()
