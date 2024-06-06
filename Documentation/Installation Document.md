

## Installation and Setup Documentation for Tuning Project


### Steps to follow 
#### 1. Clone the RocksDB Repository
Start by cloning the official RocksDB repository from GitHub. This repository contains the necessary source files to build RocksDB.

```bash
git clone https://github.com/facebook/rocksdb
```
<!-- 
#### 2. Install flags 
Install gflags. First, try: sudo apt-get install libgflags-dev If this doesn't work and you're using Ubuntu, here's a nice tutorial: (http://askubuntu.com/questions/312173/installing-gflags-12-04)
Install snappy. This is usually as easy as: sudo apt-get install libsnappy-dev.
Install zlib. Try: sudo apt-get install zlib1g-dev.
Install bzip2: sudo apt-get install libbz2-dev.
Install lz4: sudo apt-get install liblz4-dev.
Install zstandard: sudo apt-get install libzstd-dev

[ for Linux for other OS check this guide https://github.com/facebook/rocksdb/blob/main/INSTALL.md ] -->

#### 2. Build the Static Library and db_bench
Following the instruction in INSTALL.md compile the static library and db_bench. The `static_lib` target builds the static library necessary for linking with other applications, and `db_bench` is a benchmarking tool that comes with RocksDB.

```bash
cd rocksdb
make static_lib
make db_bench
```

#### 3. Verify if db_bench is running 

Use the command 
```bash 
./db_bench --compression_type=none
```

#### 3. Setup Python Bindings with Pybind11
To interact with RocksDB directly from Python, you need to set up Python bindings. This involves creating a C++ extension that Python can interact with.

##### i. Clone the tuning repository:
Clone a separate repository where the Python binding code (using Pybind11) is maintained. Adjust the paths as needed.

```bash
git clone https://github.com/indra-deepika/Auto_Tuning
cd Auto_tuning
```

##### ii. Modify `setup.py`:
Edit the `setup.py` file to configure the Python extension module. Ensure that the paths to the RocksDB includes and library files are correctly specified. Adjust the paths based on your local setup.

```python
from setuptools import setup, Extension
import pybind11

ext_modules = [
   Extension(
       "rocksdb_module",
       ["rocksdb_module.cpp"],
       libraries=["rocksdb"],
       include_dirs=["/mnt/c/Users/edeep/Final_Rocksdb/rocksdb/include"],
       library_dirs=["/mnt/c/Users/edeep/Final_Rocksdb/rocksdb"],
   ),
]

setup(
    name="RocksDB Python Bindings",
    ext_modules=ext_modules,
)
```
##### iii. Modify db_path in rocksdb_module.cpp 

```const std::string rocksdb_path = "/mnt/c/Users/edeep/Final_Rocksdb/rocksdb";```
Ensure it points to the directory where db_bench is present.

#### 4. Build the Python Extension
Compile the Python extension using the setup script. This step builds the extension in place, linking it against the RocksDB static library.

```bash
python3 setup.py build_ext --inplace
```

#### 5. Set the Library Path
Ensure the dynamic linker can find the RocksDB library by setting the `LD_LIBRARY_PATH`.

```bash
export LD_LIBRARY_PATH=/mnt/c/Users/edeep/Final_Rocksdb/rocksdb/:$LD_LIBRARY_PATH
```


#### 5. To run the code 
1. Set the workload that you want to run, target knob set, target metric to optimise in settings.py
2. Run the code use 
```bash
python3 pipeline.py
```
