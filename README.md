# Bestie by Warm Backend

This project serves backend part of Bestie. Bestie is a health issues assessment tool that utilize conversational AI. Bestie revolutionizes how we do health issues assessment, traditionally by doing self-assessment check list into light conversation with AI chatbot. The conversation data then compiled into concise statements that integrates seamlessly into other features. This project is a submission for [Garuda Hacks 4.0 hackathon](https://garuda-hacks.devpost.com/).

## Requirements

1. [Python3](https://www.python.org/downloads/)

## Libraries Used

1. [OpenAI](https://platform.openai.com/docs/api-reference?lang=python)

## Local Development

1. Setup virtualenv

```bash
python -m pip install virtualenv
python -m venv venv
```

2. Activate virtualenv

```bash
source venv/bin/activate
```

or in Windows

```powershell
venv\Scripts\activate.bat
```

2. Install libraries

```bash
python -m pip install -r requirements.txt
```

3. Start interactive session

```bash
python lambda_function.py
```

## Deployment

Deployed as a serverless service to AWS Lambda via AWS Console

### Requirements

1. [AWS account](https://aws.amazon.com/resources/create-account/)
