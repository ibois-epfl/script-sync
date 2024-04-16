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