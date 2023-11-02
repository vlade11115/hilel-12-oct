# CurrencyAggregator

# How to run:

1. Step one, install dependencies:

```
 pip install -r requirements.txt
```

2. Apply migration:

```
python manage.py migrate
```

3. Run broker:

```
docker run -d -p 5672:5672 rabbitmq
```

4. Run celery beat:

```
celery -A hilel12 beat 
```

5. Run worker:

```
celery -A hilel12 worker -l INFO

or on Windows:
1. pip install eventlet
2. celery -A hilel12 worker -l INFO -P eventlet
```

6. Run server:
```
python manage.py runserver  
or 
python3 manage.py runserver  
```
