
This talk includes a demo of State-Space Explorer. Therefore clone the repository recursively. In order to build the demo application, run

```
git submodule update --init --recursive
mkdir build
cd build
cmake ../ -DLLVM_BUILD_DIR=<llvm_build_dir>
make
```
