
## State-Space Explorer Demo

This talk includes a demo of State-Space Explorer. Therefore clone the repository recursively. In order to build the demo application, run

```
git submodule update --init --recursive
mkdir build
cd build
cmake ../ -DLLVM_BUILD_DIR=<llvm_build_dir> -DBUILD_DEMOS
make
```

## Generating the Images

The fonts required for the slides are imported in ```talk.css```.
The Graphviz trees require the ```Ubuntu Mono``` font to be installed.
It can be downloaded [here](https://http://font.ubuntu.com/).
The trees can then be generated using:

```
python3 ./scripts/generate_trees.py [-- / --force-explore / --force-generate]
```
