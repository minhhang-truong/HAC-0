import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import torch

_src_path = os.path.dirname(os.path.abspath(__file__))

# Xác định kiến trúc GPU để biên dịch chính xác
if torch.cuda.is_available():
    device_prop = torch.cuda.get_device_properties(0)
    major = device_prop.major
    minor = device_prop.minor
    arch_flag = f'-gencode=arch=compute_{major}{minor},code=sm_{major}{minor}'
else:
    arch_flag = ''

nvcc_flags = [
    '-O3', '-std=c++14',
    '-U__CUDA_NO_HALF_OPERATORS__', '-U__CUDA_NO_HALF_CONVERSIONS__', '-U__CUDA_NO_HALF2_OPERATORS__',
]

if arch_flag:
    nvcc_flags.append(arch_flag)

if os.name == "posix":
    c_flags = ['-O3', '-std=c++14']
elif os.name == "nt":
    c_flags = ['/O2', '/std:c++17']
    # Giữ nguyên phần tìm cl.exe nếu bạn dùng Windows, 
    # nhưng trên Kaggle (Linux) đoạn này sẽ bị bỏ qua.

setup(
    name='gridencoder',
    ext_modules=[
        CUDAExtension(
            name='_gridencoder',
            sources=[os.path.join(_src_path, 'src', f) for f in [
                'gridencoder.cu',
                'bindings.cpp',
            ]],
            extra_compile_args={
                'cxx': c_flags,
                'nvcc': nvcc_flags,
            }
        ),
    ],
    cmdclass={
        'build_ext': BuildExtension,
    }
)