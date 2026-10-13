# Environment Setup

How this lab is set up on Windows + WSL Ubuntu, and how the Python env (venv)
turns on by itself.

## Folder structure

```
docker-kube handson/                 ← project root (lives on the Windows C: drive)
├── .venv/                           ← Python env for WINDOWS (PowerShell)  · not in Git
├── .venv-wsl/                       ← Python env for UBUNTU (WSL)          · not in Git
├── .githooks/                       ← checks that stop commits/pushes to main
├── .github/                         ← pull request template
├── docs/                            ← Git cheatsheet + workflow notes
├── Day2-dockerize-app/              ← Day 2: Flask app + Dockerfile
├── Day3-multistage/                 ← Day 3: multi-stage Dockerfile
├── requirements.txt                 ← Python packages both venvs install
├── .gitignore                       ← things Git must NOT save (venvs, caches…)
├── README.md
└── SETUP.md                         ← this file
```

Outside the project (in Ubuntu's home folder, `~`):

```
~/.bashrc                            ← Ubuntu's startup settings (holds the auto-venv rule)
~/.bashrc.bak-auto-venv              ← backup from before the change
~/.local/bin/kind                    ← kind tool (runs Kubernetes inside Docker)
```

## The big picture

```
┌──────────────── Windows 11 ─────────────────┐
│          (VS Code opens both terminals)     │
│                                             │
│  PowerShell terminal     Ubuntu terminal    │
│          │                     │            │
│          ▼                     ▼            │
│     uses .venv/        uses .venv-wsl/      │
│   (turned on by the    (turned on by the    │
│   VS Code Python ext)   ~/.bashrc rule)     │
│          │                     │            │
│          └──────────┬──────────┘            │
│                     ▼                       │
│      project files on the C: drive          │
│      (Ubuntu sees C: as /mnt/c/)            │
│                     │                       │
│                     ▼                       │
│     Docker Desktop (one shared engine)      │
│     └── kind clusters (seen from both)      │
└─────────────────────────────────────────────┘
```

**Why two venvs?** A venv holds programs built for one operating system.
Windows' `.venv` has `.exe` files that Ubuntu can't run, so each side gets its own.

## How the auto-venv works (Ubuntu)

Each time you open an Ubuntu terminal, `~/.bashrc` runs this check:

```
Terminal opens in some folder
        │
        ▼
Does this folder have .venv/bin/activate  or  .venv-wsl/bin/activate ?
        │                         │
       yes                        no
        │                         ▼
        │                 Go up one folder and check again
        │                 (stop at the top "/" folder)
        ▼                         │
Turn that venv on                 ▼
→ prompt shows (docker-kube)   Nothing found → do nothing (venv stays off)
```

- **Only where needed.** It does nothing in folders without a venv.
- **Works for any project.** Make a venv inside a project folder, and it turns on there automatically.
- **Skips Windows venvs.** A Windows-made `.venv` has no `bin/activate` file, so it's ignored.
- **Works in subfolders.** Open a terminal in `Day3-multistage/` and it still finds the project's venv one level up.

**`lab` shortcut:** type `lab` from anywhere in Ubuntu to jump to this project,
turn the venv on, and show the Git branch.

## Quick reference

| I want to… | Do this |
|---|---|
| Check the venv is on | Line starts with `(docker-kube)`, or run `echo $VIRTUAL_ENV` |
| Turn the venv off | `deactivate` |
| Go to the project from anywhere (Ubuntu) | `lab` |
| Set up a venv for a new Ubuntu-only project | `python3 -m venv .venv` inside the project folder |
| Set up a venv in a project that already has a Windows `.venv` | `python3 -m venv .venv-wsl` |
| Install packages into the venv | `pip install -r requirements.txt` (with the venv on) |
| Undo the `.bashrc` change | `cp ~/.bashrc.bak-auto-venv ~/.bashrc` |
| `kubectl` in Ubuntu can't see a cluster made on Windows | `kind export kubeconfig --name <cluster>` |
