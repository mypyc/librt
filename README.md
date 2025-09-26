# librt: mypyc runtime library

This library contains efficient C implementations of various Python standard
library classes and functions. Mypyc can use these fast implementations when
compiling Python code to native extension modules.

This repository is used to build/publish mypyc runtime library. Development happens
in [mypy repository](https://github.com/python/mypy). Code is then perodically
synced from `mypyc/lib-rt` [subdirectory there](https://github.com/python/mypy/tree/master/mypyc).
Issues should be reported to mypyc [issue tracker](https://github.com/mypyc/mypyc/issues).
