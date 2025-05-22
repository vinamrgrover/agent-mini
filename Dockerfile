FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task

# Installing g++
RUN yum update -y && \
    yum install -y gcc-c++ && \
    yum clean all

RUN pip install --upgrade pip && pip install uv

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY agent_gemini_final.py .
COPY app.py .
COPY .env .

CMD ["app.lambda_handler"]
