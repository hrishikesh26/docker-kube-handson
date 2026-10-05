# Docker & Kubernetes Hands-on

My practice lab for Docker and Kubernetes, organized by day.

## Layout

```
Day1/          # one folder per practice session
docs/          # workflow + git cheatsheet
.githooks/     # local guards (block commits/pushes to main)
.github/       # PR template
```

## Setup

```powershell
git config core.hooksPath .githooks     # enable local guards (once per clone)
python -m venv .venv                    # if .venv doesn't exist yet
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Git workflow

`main` is protected: every change goes **branch → PR → squash merge**.

```powershell
git switch main; git pull
git switch -c feat/day2-k8s-pods
# ...work, commit...
git push -u origin HEAD
gh pr create --fill
gh pr merge --squash --delete-branch
```

- Full workflow and conventions: [docs/WORKFLOW.md](docs/WORKFLOW.md)
- Commands, diagrams, troubleshooting: [docs/GIT_CHEATSHEET.md](docs/GIT_CHEATSHEET.md)
