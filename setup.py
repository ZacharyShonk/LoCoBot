from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pykobuki",
        ["pykobuki.cpp"],
        include_dirs=[
            pybind11.get_include(),
            "/home/locobot/Documents/kobuki/install/include",
            "/home/locobot/Documents/kobuki/install/include/eigen3"
        ],
        library_dirs=["/home/locobot/Documents/kobuki/install/lib"],
        libraries=["kobuki_core"],  # Use "kobuki_core" since the file is libkobuki_core.so
        extra_compile_args=["-std=c++14"],
        language="c++"
    )
]

setup(
    name="pykobuki",
    version="0.1",
    author="Your Name",
    description="Python wrapper for the Kobuki robot using libkobuki",
    ext_modules=ext_modules,
)
