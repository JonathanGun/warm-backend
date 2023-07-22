# Warm Backend

// TODO danial

This project is part of Warm Application in [Garuda Hacks 4.0 hackathon](https://garuda-hacks.devpost.com/). Warm is a xxx app that helps people to xxx

Assessment assistant using OpenAI's GPT (generative pre-trained transformer), pre-prompted to assist user understanding what it needs.

## Requirements

1. [Python3](https://www.python.org/downloads/)

## Libraries Used

1. [OpenAI](https://platform.openai.com/docs/api-reference?lang=python)
2. [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)

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

3. Invoke function

```bash
python -c ''
```

## Deployment (TODO)

Deployed to GCP Cloud Function using Terraform

### Requirements

1. [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
2. [GCP account](https://cloud.google.com/free/); you can use free credit, or use [free tier for cloud functions](https://cloud.google.com/free/docs/free-cloud-features#cloud-functions)
3. [gcloud cli](https://cloud.google.com/sdk/gcloud)

### Steps

1. Init terraform

```bash
terraform init
```

2. 

```bash
terraform apply
```

### Clean up Resources

To keep your billing account healthy, you can clean up unused resource after you are finished with the project

```bash
terraform destroy
```
