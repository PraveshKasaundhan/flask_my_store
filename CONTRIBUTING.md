# CONTRIBUTING

## How to run docker container file locally
```
CMD ["flask","run","--host","0.0.0.0"]
docker run -dp 5005:5000 -w /app -v "%cd%:/app" myimage
```

## How to run docker container with gunicorn file locally
```
CMD ["gunicorn","--bind","0.0.0.0:80","app:create_app()"]
docker run -dp 5005:5000 -w /app -v "%cd%:/app" myimage sh -c "flask run --host 0.0.0.0"
```

## How to run redis in docker in local
```
docker run -w /app myimage sh -c "rq worker -u <redis_url> emails"
```