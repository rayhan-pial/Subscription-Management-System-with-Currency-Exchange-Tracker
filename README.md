# Subscription Management System with Currency Exchange Tracker

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/rayhan-pial/Subscription-Management-System-with-Currency-Exchange-Tracker.git
cd Subscription-Management-System-with-Currency-Exchange-Tracker

### 2. Create and Configure .env File

Create a .env file in the root directory of your project following the structure of the existing env-file.

Fill in the required values:

CELERY_BROKER_URL=your_broker_url
CELERY_RESULT_BACKEND=your_result_backend

### 3. Install Dependencies

pip install -r requirements.txt

## Run the Project

Terminal 1: Run Django Server

            - python manage.py runserver

Terminal 2: Start Celery Worker

            On Windows - celery -A subscription_project worker -l info --pool=solo
            On Linux - celery -A subscription_project worker -l info

Terminal 3: Start Celery Beat Scheduler

            - celery -A subscription_project beat --loglevel=info

Terminal 4: Start Manual Exchange Rate Fetch Task

            - python manage.py exchange_task

## API

### Get Token (POST) url - http://127.0.0.1:8000/api/token/

Response- { "access": "new_access_token"}

### Get Token (POST) url -http://127.0.0.1:8000/api/token/refresh/

Body - { "refresh": "refresh_token"}

Response- { "access": "new_access_token"}

### Get All Subscriptions (GET) url - http://127.0.0.1:8000/api/subscriptions/

return user's all subscriptions

### Subscribe a Plan (POST) url - http://127.0.0.1:8000/api/subscribe/

Body - { "plan_id": 1}

create a subscription for the user

### Cancel a Subscription (POST) url - http://127.0.0.1:8000/api/cancel/

Body - { "subscription_id": 1}

Cancel the given subscription

### Get Exchange Rate (GET) url - http://127.0.0.1:8000/api/exchange-rate/

Param - { "base_currency": "USD", "target_currency": "BDT"}

return currency exchange rate between them
