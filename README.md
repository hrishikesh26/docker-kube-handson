# Docker & Kubernetes Hands-on

My practice lab for Docker and Kubernetes, organized by day.

## Layout

```
Day1/   # one folder per practice session
...
```

## Setup

```powershell
# Activate the Python virtual environment (PowerShell)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Git workflow

1. `git switch main && git pull`
2. `git switch -c dayN/<topic>`: one branch per topic
3. Commit small, focused changes
4. `git push -u origin dayN/<topic>` and open a Pull Request
5. Review the diff, merge on GitHub, then delete the branch
