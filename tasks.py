# tasks.py
from invoke import task

DIR_IN_GHUSER_COMPONENTS = "./GH/PyGH/components"
DIR_OUT_GHUER_COMPONENTS = "./build/gh"

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

@task
def ghcomponentize(c):
    path_ghcomponentizer = "./invokes/ghcomponentize/ghcomponentizer.py"
    c.run(f"python {path_ghcomponentizer} \
        --ghio ./invokes/ghcomponentize/ghio \
        {DIR_IN_GHUSER_COMPONENTS} \
        {DIR_OUT_GHUER_COMPONENTS}")