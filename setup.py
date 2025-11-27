from setuptools import setup, Extension, find_packages
import meta

setup(
    **vars(meta.setup),
    ext_modules=[
        Extension("fake_ext", sources=[]),
        Extension(
            'jsify.cjsify',
            sources=[
                'source/cjsify/Undefined.c',
                'source/cjsify/Object.c',
                'source/cjsify/Tuple.c',
                'source/cjsify/List.c',
                'source/cjsify/Dict.c',
                'source/cjsify/Iterator.c',
                'source/cjsify/Literals.c',
                'source/cjsify/cjsify.c'
            ],
            include_dirs=['source/cjsify']
        ),
    ],
    packages=find_packages("source"),
    package_dir={"jsify": "source/jsify"},
    package_data={"jsify": ["*.py", '*.pyi']},
    zip_safe=False
)
