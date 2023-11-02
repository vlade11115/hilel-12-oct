Installation:
```angular2html
pip install -r requirements.txt
```

Create database:
```angular2html
pyton manage.py migrate
```
Run broker:
```angular2html
docker run -d -p 5672:5672 rabbitmq
```
Run celery beat:
```angular2html
celery -A hilel12 beat
```

Run worker process:

Linux, macOS
```angular2html
celery -A hilel12 worker -l INFO
```

Windows
```angular2html
celery -A hilel12 worker -l INFO -P eventlet
```



Run server:
```angular2html
python manage.py runserver
```
