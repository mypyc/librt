import os
import shutil
import subprocess
import tempfile

from pathlib import Path

REPO = "https://github.com/python/mypy"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        mypy_dir = os.path.join(tmp_dir, "mypy")
        subprocess.run(["git", "clone", REPO, mypy_dir, "--depth=1"], check=True)
        shutil.rmtree("lib-rt", ignore_errors=True)
        shutil.copytree(os.path.join(mypy_dir, "mypyc", "lib-rt"), "lib-rt", dirs_exist_ok=True)
        shutil.rmtree("librt", ignore_errors=True)
        shutil.copytree(
            os.path.join(mypy_dir, "mypy", "typeshed", "stubs", "librt", "librt"),
            "librt",
            dirs_exist_ok=True,
        )
        Path("librt/py.typed").touch()


if __name__ == "__main__":
    main()
