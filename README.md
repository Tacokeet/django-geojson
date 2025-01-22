# Geovector Infrastructure

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation & Testing

1. Build the Docker containers:
```bash
docker-compose build
```

2. [A] Run the tests:
```bash
docker-compose run --entrypoint /app/entrypoint-test.sh web
```

2. [B] Run test if you have container already running:
```bash
docker exec -it ai-infrasolutions-web-1 python manage.py test
```

### Running the website

1. Run Django with Postgis database
 ```bash
docker-compose up
```

### Populate database with features
1. Run the feature population script:
```bash
docker exec -it ai-infrasolutions-web-1 python post_features.py
```
*Note: The container name 'ai-infrasolutions-web-1' may differ if multiple containers were built*


### Acquire JWT
1. Get JWT tokens with username and password:
```bash
curl -X POST http://localhost:8000/token/ \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin"}'
```

2. Request will return both access and refresh tokens:
```json
{
    "refresh": "your.refresh.token",
    "access": "your.access.token"
}
```

3. Use access token in subsequent requests:
```bash
curl http://localhost:8000/features/ \
    -H "Authorization: Bearer your.access.token"
```


### Endpoints
The API exposes the following endpoints:

- `/token/` - Receive refresh and access JWT 
    - `POST`: Post your credentials (username/password) to receive tokens

- `/token/refresh/` - Refresh JWT 
    - `POST`: Post with your refresh token to receive new access token

- `/features/` - Get and create features
    - `GET`: Returns features 
    - `POST`: Create new feature with name and geometry

- `/features/?in_bbox=<min Lon>,<min Lat>,<max Lon>,<max Lat>` - Get features inside bounding box
    - `GET`: Returns features inside bounding box

- `/features/<id>/` - Manage specific features
    - `GET`: Returns specific feature details
    - `PUT`: Update feature
    - `DELETE`: Remove feature
