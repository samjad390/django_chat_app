# Django Chat App

This is a simple chat application built with Django and Channels that allows users to join a chat room and exchange messages in real-time.

## Prerequisites

To run this project, you will need the following installed on your system:

- Python
- Django
- Channels
- Redis Server
- DRF
- PostgreSQL

## Getting Started

1. Clone the repository to your local machine
2. Open your terminal and navigate to the project directory
3. Create a virtual environment and activate it:
```
python3 -m venv env
source env/bin/activate
```
4. Install the project dependencies:
```
pip install -r requirements.txt
```
5. Start the Redis server:
```
redis-server
```
6. Create postgresql database named ```chat_app```.
7. Run the Django migrations command:
```
python manage.py migrate
```
8. Run the Django development server:
```
python manage.py runserver
```
9. Open your browser and go to http://localhost:8000 to view the application

## Running Tests

To run the automated tests for this system, run the following command in your terminal:
```
python manage.py test
```

## Deployment

To deploy this application to a live server, you will need to configure your web server and database settings. 

