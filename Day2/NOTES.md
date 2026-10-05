# Day 2: Containerizing a Flask To-Do App

## What I built

A minimal Flask to-do app (`app.py`), packaged as a Docker image and pushed to Docker Hub as
`hrishikesh26/docker-kube-practice:v1`.

## Dockerfile

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

- `RUN` runs a command at **build** time (installing dependencies).
- `CMD` runs a command when the **container starts** (launching the app).
- Both take a full command, not just a file name.
- Copy `requirements.txt` first so the slow `pip install` layer stays cached when only code changes.
- `EXPOSE` is documentation only. It does not change the port the app listens on.

## Commands

```powershell
docker build -t hrishikesh26/docker-kube-practice:v1 .   # build + name:tag
docker run -dp 3000:5000 hrishikesh26/docker-kube-practice:v1   # -p laptop:container
docker ps          # running containers
docker ps -a       # all containers, including stopped
docker stop <id>   # stop
docker rm <id>     # delete a container
docker rmi <image> # delete an image
docker tag <old> <new>   # add another name to an image
docker login
docker push hrishikesh26/docker-kube-practice:v1
```

Image name format: `<dockerhub-user>/<repo>:<tag>`. Use version tags (`v1`, `v2`) instead of only `latest`.

## Problems I hit and fixes

| Problem | Cause | Fix |
| --- | --- | --- |
| `localhost:3000` showed nothing | Ran `-p 3000:3000`, but the app listens on 5000 inside the container | `-p 3000:5000` (right side = the app's real port) |
| `An image does not exist locally with the tag` on push | Built as `day2-todo`, pushed a different name | Build with the full name `user/repo:tag`, or `docker tag` it |
| Build still used the old Dockerfile | File wasn't saved | Save (Ctrl+S) before `docker build` |
| `unable to remove repository reference ... (must force)` | A **stopped** container still used the image | `docker ps -a`, `docker rm <id>`, then `docker rmi` |
| Typo in image name (`kunbe`) | n/a | Rebuild with the correct name; delete the old repo on Docker Hub |
| `command not found` in WSL | Ubuntu uses `python3`; pip/venv not installed; Windows `.venv` doesn't work in Linux | `sudo apt install python3-venv python3-pip`, create a separate Linux venv |
