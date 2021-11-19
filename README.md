# BookStoreAPI

## Introduction
A quick example of how to use [Django-Ninja-Extra](https://eadwincode.github.io/django-ninja-extra/), [Ninja-Schema](https://github.com/eadwinCode/ninja-schema) and [NinjaJWT](https://eadwincode.github.io/django-ninja-jwt/)


## Quick Start
For development: 
### Build Docker Image
```bash
bash scripts/docker_build.sh build
```

### Run Docker Image
```bash
bash scripts/docker_build.sh up
```
Run image on background
```bash
bash scripts/docker_build.sh up -d
```
Visit: [http://0.0.0.0:8001/api/docs](http://0.0.0.0:8001/api/docs)

### Stop Docker Image
```bash
bash scripts/docker_build.sh down
```

Preview
<img src="docs/image/bookstore_api.gif">
