import os
import json
import uuid
from datetime import datetime
import boto3
from agent_gemini_final import agent
from dotenv import load_dotenv

load_dotenv()

S3_LOG_BUCKET = os.environ.get("S3_LOG_BUCKET")
S3_LOG_PREFIX = os.environ.get("S3_LOG_PREFIX", "logs/")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key"),
)


def save_log_to_s3(log_obj):
    """Save the log as a JSON file to S3."""
    log_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    key = f"{S3_LOG_PREFIX}{timestamp}_{log_id}.json"
    s3_client.put_object(
        Bucket=S3_LOG_BUCKET,
        Key=key,
        Body=json.dumps(log_obj, indent=2),
        ContentType="application/json",
    )
    # Optional: return key or print for debug
    print(f"Invocation log saved to s3://{S3_LOG_BUCKET}/{key}")


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    companies = body.get("companies", [])
    if not companies:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No companies provided."}),
            "headers": {"Content-Type": "application/json"},
        }

    # Prepare agent input
    company_str = " and ".join(companies)
    input_message = {
        "role": "user",
        "content": f"What are the latest news stories about {company_str}",
    }

    # Collect logs
    invocation_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "input_message": input_message,
        "companies": companies,
        "steps": [],
        "response": None,
        "request_id": context.aws_request_id if context else None,
    }

    # Run the agent and collect output
    news_summaries = []
    for step in agent.stream(
        {"messages": [input_message]}, stream_mode="values"
    ):
        msg = step["messages"][-1]
        news_summaries.append(msg.content)
        invocation_log["steps"].append(
            {"role": "human", "content": msg.content}
        )
        invocation_log["response"] = (
            msg.content
        )  # Last one is the final response

    # Save the invocation log to S3
    try:
        save_log_to_s3(invocation_log)
    except Exception as e:
        # Optionally log this somewhere else or add to response
        print(f"Failed to save log to S3: {e}")

    # Return the response
    return {
        "statusCode": 200,
        "body": json.dumps({"companies": companies, "news": news_summaries}),
        "headers": {"Content-Type": "application/json"},
    }
