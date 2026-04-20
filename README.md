# n8n + Python

n8n instance with a Python 3.13 spam/ham classifier running alongside it.

## Stack

- **n8n** — workflow automation
- **Python 3.13** — spam classifier using logistic regression (SMS Spam Collection dataset)

## Run locally

```bash
uv venv
uv pip install -r source/requirements.txt
python source/spam_classifier.py "your message here"
```

## Deploy (CapRover)

```bash
tar -czf app.tar.gz --exclude='.venv' --exclude='source/spam_model.pkl' --exclude='source/SMSSpamCollection' .
```

Upload the tar via CapRover dashboard. Add a persistent directory mapped to `/root/.n8n`.
