# Day 3: Multi-Stage Docker Build

## The big idea

Think of baking a cake.

- **Kitchen** (stage 1): flour bags, bowls, mixer, mess everywhere.
- **Plate** (stage 2): just the cake.

You don't hand someone the whole kitchen, only the plate. A multi-stage build does
the same: build in one image, then copy **only the finished stuff** into a clean, small image.

## The Dockerfile, line by line

### Stage 1: the kitchen (`builder`)

```dockerfile
FROM python:3.11-alpine AS builder
```

Start from a small Python image. `AS builder` gives this stage a **name** so we can grab things from it later.

- `python` = image name, `3.11-alpine` = tag (Python 3.11 on Alpine, a tiny Linux).
- `:` separates the **name** from the **tag** (`name:tag`).

```dockerfile
WORKDIR /app
```

"Go into the `/app` folder." Creates it if missing. All later commands run here.

- `/` at the start = the **root** (top) of the container's file system, like `C:\` on Windows.
- `/app` = a folder called `app` right under the root.

```dockerfile
RUN python -m venv /venv
```

Make a **virtual environment** (a box that holds all Python packages) at `/venv`.
One box = easy to carry to the next stage.

- `RUN` = run this command **while building** the image.
- `-m venv` = "run Python's built-in `venv` module".

```dockerfile
ENV PATH="/venv/bin:$PATH"
```

"When I say `python` or `pip`, use the ones inside the box." So `pip install` puts packages in `/venv`.

- `ENV` = set an environment variable (a setting the container remembers).
- `PATH` = the list of folders Linux searches when you type a command.
- `$PATH` = "the old value of PATH". `$` means "read this variable".
- `:` here = separator between folders in the list.
- So this means: "look in `/venv/bin` **first**, then everywhere else".

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Copy the shopping list, then install Flask into the box.

- `COPY <from laptop> <to container>`.
- `.` = "the current folder" (here `/app`, because of `WORKDIR`).
- `-r requirements.txt` = "read the package list from this file".
- `--no-cache-dir` = don't keep downloaded leftovers. Smaller image.

### Stage 2: the plate (runtime)

```dockerfile
FROM python:3.11-alpine
```

A **second `FROM`** = a brand-new, empty image. Nothing from stage 1 comes along unless we ask.

```dockerfile
WORKDIR /app
COPY --from=builder /venv /venv
```

The magic line. "From the `builder` stage, copy only the `/venv` box." Everything else in stage 1 is thrown away.

- `--from=builder` = copy from the stage named `builder`, **not** from your laptop.
- `/venv /venv` = source path, then destination path.

```dockerfile
ENV PATH="/venv/bin:$PATH"
COPY app.py .
```

Use the box again (ENV does **not** carry over between stages), and copy in our app code.
Only `app.py`, not the whole folder.

```dockerfile
RUN adduser -D appuser
USER appuser
```

Make a normal user and switch to it. Running as `root` is like giving a guest the master key. Don't.

- `root` = the all-powerful admin user in Linux.
- `-D` = "don't set a password" (Alpine's `adduser` option). The user can't log in, it just runs the app.

```dockerfile
EXPOSE 5000
CMD ["python", "app.py"]
```

- `EXPOSE` = a note saying "the app uses port 5000" (documentation only).
- `CMD` = what runs when the **container starts** (not at build time).
- `["python", "app.py"]` = "exec form". Each word in its own quotes. Preferred over `CMD python app.py`
  because the app receives stop signals properly (`docker stop` is fast).

## Commands

```powershell
docker build -t todo:multistage .        # build
docker run -dp 3000:5000 todo:multistage # run, open http://localhost:3000
docker images                            # compare sizes with Day 2 image
docker build --target builder -t todo:builder .   # build ONLY stage 1 (for debugging)
```

- `-t` = **tag**: give the image a name (`name:tag`).
- `.` at the end of `docker build` = "use this folder" (the **build context**: files Docker can `COPY`).
- `-d` = **detached**: run in the background, give me my terminal back.
- `-p 3000:5000` = **port**: `laptop:container`. Laptop's 3000 forwards to container's 5000.
- `-dp` = `-d` and `-p` squeezed together.
- `--target builder` = stop after the `builder` stage.
- `#` = comment. Everything after it is ignored.

## Words to know

| Word | Meaning (simple) |
| --- | --- |
| Image | A frozen recipe + ingredients. Doesn't run. |
| Container | A running copy of an image. |
| Stage | One `FROM ...` section of a Dockerfile. |
| Layer | Each instruction (`RUN`, `COPY`, ...) makes a layer. Docker caches them. |
| Build time | When `docker build` runs (`RUN` happens here). |
| Run time | When `docker run` starts the container (`CMD` happens here). |
| Alpine | A super small Linux. Great for small images. |
| venv | A folder that holds a project's Python packages. |

## Tips to remember

- **Two `FROM`s = two stages.** Only the **last** stage becomes your final image.
- **Name your stages** with `AS name`. `--from=name` is easier to read than `--from=0`.
- **`COPY --from=` is the only bridge** between stages. If you didn't copy it, it's gone.
- **`ENV PATH` must be set in both stages.** ENV does not carry over between stages.
- **Copy `requirements.txt` before your code** so Docker caches the slow install step.
- **Small app = small savings.** Multi-stage shines when you need build tools
  (like `gcc`) that the running app doesn't need.
- **Use the same base image in both stages** (here `3.11-alpine`). Packages built on one
  OS may not work on another.
- **Don't run as root.** Add a user and `USER` it.
- **`EXPOSE 5000`, not `EXPOSE 3000:5000`.** The `laptop:container` mapping goes in `docker run -p`.
- **`RUN` = build time, `CMD` = start time.** Remember: "RUN while baking, CMD when serving".
- **Save the file (Ctrl+S) before `docker build`.** Docker builds what's on disk, not what's in your editor.
