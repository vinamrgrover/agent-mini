# Agent Mini - Small Finance Agent

A mini AI-Agent that uses the Langchain Y-Finance module to fetch the latest news for company tickers. Deployed on AWS Lambda as a container, with an API Gateway for easy access.

## Architecture Diagram

![Untitled Diagram drawio-10](https://github.com/user-attachments/assets/0db24298-da0c-4118-90a4-8e01ac2041df)


## Features

- Fetches latest company news using stock ticker symbols (e.g., AAPL, MSFT)
- Powered by Langchain and Google Gemini
- Serverless, scalable, and easy to deploy on AWS

## Getting Started

### 1. Building the Docker Image

```bash
docker build -t agent_mini:latest .
```

### 2. Pushing to ECR

First, create an ECR repository (if you haven't already):

```bash
aws ecr create-repository --repository-name agent-mini
```

Authenticate Docker to your registry:

```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com
```

Tag and push the image:

```bash
docker tag agent_mini:latest <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/agent-mini:latest
docker push <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/agent-mini:latest
```

### 3. Creating the Lambda Function

Create a new Lambda function using the container image:

```bash
aws lambda create-function \
  --function-name agent-mini-fn \
  --package-type Image \
  --code ImageUri=<aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/agent-mini:latest \
  --role arn:aws:iam::<aws_account_id>:role/<your-lambda-execution-role>
```

**Note:** Make sure your Lambda execution role has permissions for S3 (for logging) and any other AWS resources you use.

### 4. Configuring API Gateway

1. **Create an HTTP API** (recommended for simplicity):
   - Go to the API Gateway Console
   - Create a new HTTP API
   - Add an integration: choose your Lambda function (`agent-mini-fn`)
   - Add a route (e.g., `POST /news`)
   - Deploy the API

2. **Test your endpoint:**

```bash
curl -X POST "<invoke-url>/news" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["Apple", "Microsoft"]}'
```

### 5. (Optional) Setting Rate Limiting

You can configure rate limiting using API Gateway Usage Plans and API Keys, or attach AWS WAF for IP-based rate limiting.

## Environment Variables

Set the following environment variables (in Lambda or `.env`):

| Variable | Description |
|----------|-------------|
| `S3_LOG_BUCKET` | S3 bucket for storing invocation logs |
| `S3_LOG_PREFIX` | (Optional) Prefix for log files |
| `GOOGLE_API_KEY` | (If using Google Gemini) API key |
| `aws_access_key_id` | Your AWS Access Key ID
| `aws_secret_access_key` | Your AWS Secret Access Key | 
| ... | Any other required variables |

## Example Usage

### Request

```http
POST /news
Content-Type: application/json

{
  "companies": ["Apple", "Microsoft"]
}
```

### Response

```json
{
  "companies": ["Apple", "Microsoft"],
  "news": [
    "Apple: ...",
    "Microsoft: ..."
  ]
}
```

## Development & Local Testing

You can run and test the container locally using Docker:

```bash
docker run -p 9000:8080 agent_mini:latest
```

Invoke the Lambda locally:

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"body": "{\"companies\": [\"Apple\", \"Microsoft\"]}"}'
```
