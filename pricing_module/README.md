# Pricing Module 🚕 (Django)

A Django application for calculating ride prices based on distance, time, and waiting time. It supports dynamic pricing configurations that can be managed through an admin panel.


## Features

- Distance + Time + Waiting based price
- Dynamic day-wise pricing config
- Admin Panel to manage configs
- API to calculate final ride price

## Virtual environment is recommended.
 ### Setup:
 - python -m venv venv
 - source venv/bin/activate (Linux/Mac)

## Run

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
