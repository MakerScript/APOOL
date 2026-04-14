# Yandex Alice Skill — "Buy an Elephant"

A Python Flask backend for a Yandex Alice (voice assistant) skill.

## Project Structure

- `main.py` — Main application. Implements the "Купи слона" (Buy an Elephant) skill at the `/post` endpoint.
- `sjhshhs.py` — Experimental skill with Yandex NLU entity recognition (names and cities).
- `requirements.txt` — Python dependencies (Flask, gunicorn).

## Running

The app runs on port 5000 via Flask in development:

```
python main.py
```

## Deployment

Uses gunicorn for production:

```
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```

## How It Works

The `/post` endpoint receives POST requests from Yandex Alice dialog API (JSON format) and responds with dialog responses. The skill repeatedly tells users to "buy an elephant" until they agree.
