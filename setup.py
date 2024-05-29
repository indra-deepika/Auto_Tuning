from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11
from settings import rocksdb_path 
ext_modules = [
    Pybind11Extension(
        "rocksdb_module",
        ["rocksdb_module.cpp"],
        libraries=["rocksdb"],  # Link against the RocksDB library
        include_dirs=[
            rocksdb_path + "/include",  # Include path for RocksDB
            pybind11.get_include(),  # Include path for Pybind11
        ],
        library_dirs=[rocksdb_path],  # Directory containing the RocksDB library files
    ),
]

setup(
    name="rocksdb_module",
    version="1.0",
    author="Your Name",
    description="Python bindings for custom RocksDB functionalities",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
