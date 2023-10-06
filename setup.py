#License Header

from setuptools import setup

setup(
    name='lco',
    version='0.0.1',
    py_modules=['lco'],
    install_requires=[
        "click>=8.0",
        "PyYAML>=5.1",
        "looker-sdk>=23.0.0",
        "pandas>2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'lco = lco:cli',
        ],
    },
)