# Day 3: kind Multi-Node Cluster

## What we built

A local Kubernetes cluster with **1 control plane + 2 workers**, running on Docker Desktop.
Each node is just a Docker container. The setup lives in `kind-multinode.yaml`.

```bash
kind create cluster --config Day3-multistage/kind-multinode.yaml   # create
kubectl get nodes                                                   # check (all Ready)
kind delete cluster --name kind-cluster-practice                    # delete
```

- **Cluster name:** `kind-cluster-practice`
- **kubectl context:** `kind-kind-cluster-practice` (kind adds `kind-` in front)
- **Workers show ROLES `<none>`:** normal. That column only reads labels. Optional:
  `kubectl label node <name> node-role.kubernetes.io/worker=`

## Setup fixes we needed first

| Problem | Fix |
|---|---|
| WSL used old **cgroup v1**, so Kubernetes v1.37 refused to start | `C:\Users\hrish\.wslconfig` → `[wsl2]` `kernelCommandLine = cgroup_no_v1=all`, then `wsl --shutdown` |
| **Two Docker engines** (one in Ubuntu, one in Docker Desktop), so things "disappeared" | Removed Ubuntu's Docker, turned on Docker Desktop → Settings → Resources → **WSL integration → Ubuntu** |

## The memory problem

The first 3-node create **failed**: the API server never answered, so kubeadm gave up after ~60s.

**Why:** the PC has 7.4 GB RAM, Docker gets ~3.6 GB of it, and only ~1.2 GB was free.
Starting 3 nodes at once was too slow, and the setup timed out. Retrying later worked.

**How to avoid it:**

1. **Free RAM before creating.** Close browser tabs and heavy apps. Aim for 3+ GB free (Task Manager → Memory).
2. **Stop the cluster when not practicing** (kind has no `stop`, so stop the containers):
   ```bash
   docker stop  $(docker ps -q  --filter "label=io.x-k8s.kind.cluster=kind-cluster-practice")
   docker start $(docker ps -aq --filter "label=io.x-k8s.kind.cluster=kind-cluster-practice")
   ```
3. **Use fewer nodes.** 1 control plane + 1 worker is enough to learn scheduling.
4. **Run one cluster at a time.** Delete old ones (`kind get clusters` to list them).
5. **Don't raise WSL memory** on a 7.4 GB PC. It would starve Windows itself.
