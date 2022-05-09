import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pyocutil",
    version="0.0.1",
    packages=[
        'pyocutil',
    ],
    # from here all is optional
    description="utilities for openshift",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'oc',
        'openshift',
    ],
    url="https://veltzer.github.io/pyocutil",
    download_url="https://github.com/veltzer/pyocutil",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'pytconf',
        'pylogconf',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
        'pyocutil=pyocutil.main:main',
    ]},
    python_requires=">=3.10",
)
