# tasks.py
from invoke import task

@task
def yakerize(c):
    path_yakerize : str = "./invokes/yakerize.py"
    c.run(f"python {path_yakerize}")

#access a repository secret