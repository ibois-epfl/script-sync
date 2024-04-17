# tasks.py
from invoke import task

@task
def yakerize(c):
    path_yakerize : str = "./invokes/yakerize.py"
    c.run(f"python {path_yakerize}")

@task
def vscerize(c):
    path_vscerize : str = "./invokes/vscerize.py"
    c.run(f"python {path_vscerize}")

@task
def syncv(c):
    path_sync_version : str = "./invokes/syncv.py"
    c.run(f"python {path_sync_version}", hide=False, warn=True)