# CONTRIBUTING

## How to run docker file locally
```
docker -dp 5005:5000 -w /app -v "%cd%:/app" image_name sh -c "flask run"
```
