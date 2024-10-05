#! python3

"""
    This script collects all the files needed to create the yak package.
"""

from invoke import run
import os
import sys
import shutil


def main() -> None:
    # create a build folder in the yaker directory
    path_yakerdir : str = "./yaker"
    path_builddir : str = "./yaker/build"

    # if not empty, delete the build folder
    # delete the entire folder
    if os.path.exists(path_builddir):
        shutil.rmtree(path_builddir)
    os.makedirs(path_builddir, exist_ok=False)

    #####################################################################
    # Rhino rhp
    #####################################################################
    # path_rhldir : str = "dotnet restore ./CsRhino/ScriptSync.csproj"
    res = run("dotnet restore ./CsRhino/ScriptSync.csproj", hide=False, warn=True)
    res = run("dotnet build ./CsRhino/ScriptSync.csproj --configuration Release --no-restore", hide=False, warn=True)

    # copy each file contained in ./CsRhino/bin/Release/net48/ to the yaker build folder
    path_rhldir : str = "./CsRhino/bin/Release/net48/"
    for file in os.listdir(path_rhldir):
        shutil.copy(os.path.join(path_rhldir, file), path_builddir)

    #####################################################################
    # Py Components
    #####################################################################
    # the cpy_componentizer script
    componentizercpy_path : str = r"./invokes/ghcomponentize/ghcomponentizer.py"
    # where the components are stored
    components_dir : str = r"./GH/PyGH/components"
    # the ghio folder 
    ghio_dir : str = os.path.join(path_yakerdir, "ghio")
    print(ghio_dir)

    res = run(f"python {componentizercpy_path} --ghio {ghio_dir} {components_dir} {path_builddir}", hide=False, warn=True)

    #####################################################################
    # Manifest, logo, misc folder (readme, license, etc)
    #####################################################################

    # copy the manifest file
    shutil.copy("./manifest.yml", path_builddir)

    # copy the logo file
    shutil.copy("./logo.png", path_builddir)

    # create a misc folder in the yaker directory
    path_miscdir : str = os.path.join(path_builddir, "misc")
    os.makedirs(path_miscdir, exist_ok=False)

    # # copy the readme file
    shutil.copy("./README.md", path_miscdir)

    # # copy the license file
    shutil.copy("./LICENSE.md", path_miscdir)

    #####################################################################
    # Yakerize
    #####################################################################
    yak_exe_path : str = os.path.join(path_yakerdir, "exec", "Yak.exe")
    #get the absolute path of the exe
    yak_exe_path = os.path.abspath(yak_exe_path)
    print(yak_exe_path)

    path_current : str = os.getcwd()
    os.chdir(path_builddir)
    res = run(f"cd", hide=False, warn=True)
    res = run(f"{yak_exe_path} build", hide=False, warn=True, echo=True)
    if res.failed:
        print(f"Yakerize failed: {res.stderr}")
        sys.exit(1)
    else:
        print("Yakerize successful.")
    os.chdir(path_current)


if __name__ == "__main__":
    main()