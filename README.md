# Django Project Setup Guide

## 1. Clone the repo

```bash
git clone https://github.com/Togev/dungeon-finder.git
cd dungeon-finder
```

## 2. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure environment variables

- Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

- Edit `.env` to add your credentials and a secret key.

### Generating a Django SECRET_KEY

You can generate a new secret key by running:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output into your `.env` file.

## 4. Run migrations

```bash
python manage.py migrate
```

## 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

## 6. Run the development server

```bash
python manage.py runserver
```