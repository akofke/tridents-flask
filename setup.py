from setuptools import setup

setup(
    name='tridents',
    packages=['tridents'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
)