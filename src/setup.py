from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

os.environ["CC"] = "g++"

sources = ["point_cloud_renderer.pyx", "cpp/point_cloud_renderer.cpp", 
                                       "cpp/camera.cpp", 
                                       "cpp/glad.c", 
                                       "cpp/GLShader.cpp"]

ext_modules=[
    Extension("point_cloud_renderer",
              sources=sources,
              include_dirs=['../inc/'],
              libraries=["m"],
              language="c++",
              extra_compile_args=["-std=c++14", "-lGl"]
    )
]

setup(
  name = "PointCloudRenderer",
  ext_modules = cythonize(ext_modules)
)
