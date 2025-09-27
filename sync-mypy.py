import os
import shutil
import subprocess
import tempfile

REPO = "https://github.com/python/mypy"

def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        mypy_dir = os.path.join(tmp_dir, "mypy")    
        subprocess.run(["git", "clone", REPO, mypy_dir, "--depth=1"], check=True)
        shutil.copytree(os.path.join(mypy_dir, "mypyc", "lib-rt"), "lib-rt", dirs_exist_ok=True)


if __name__ == "__main__":
    main()
