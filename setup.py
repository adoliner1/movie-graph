from setuptools import setup, find_packages

setup(
    name="movie-graph",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'neo4j==5.14.1',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
    ],
)