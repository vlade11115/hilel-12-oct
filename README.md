1. Install dependencies
```
pip install -r requirements.txt
```
2. Migrate models
```
python manage.py migrate
```
3. Run broker RabbitMQ
```
docker run -d -p 5672:5672 rabbitmq
```
4. Run worker
Mac & Linux
```
celery -A hilel12 worker -l INFO
```
Windows
```
celery -A hilel12 worker -l INFO --pool=solo
```
5. Run celery beat
```
celery -A hilel12 beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
6. Run Django web-server
```
python manage.py runserver
```