from setuptools import setup
from setuptools.command.test import test as TestCommand

import sortedcontainers


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        exit(errno)


with open('README.rst') as reader:
    readme = reader.read()

args = dict(
    name=sortedcontainers.__title__,
    version=sortedcontainers.__version__,
    description='Sorted Containers -- Sorted List, Sorted Dict, Sorted Set',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://www.grantjenks.com/docs/sortedcontainers/',
    license='Apache 2.0',
    packages=['sortedcontainers'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

try:
    from Cython.Build import cythonize
except ImportError:
    pass
else:
    from setuptools import Extension
    ext_modules = [
        Extension('sortedcontainers._sortedlist', ['sortedcontainers/sortedlist.py']),
        Extension('sortedcontainers._sorteddict', ['sortedcontainers/sorteddict.py']),
        Extension('sortedcontainers._sortedset', ['sortedcontainers/sortedset.py']),
    ]
    args.update(ext_modules=cythonize(ext_modules))

setup(**args)
