from setuptools import setup, find_packages

setup(
    name="pharmacy-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'flask>=2.3.3',
        'werkzeug>=2.3.7',
        'flask-sqlalchemy>=3.1.1',
        'flask-wtf>=1.1.1',
        'flask-login>=0.6.2',
    ],
    python_requires='>=3.11',
) 