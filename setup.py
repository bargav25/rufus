from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    author="Bargav",
    author_email="jbargav025@gmail.com",
    description="A tool for intelligent web data extraction using Playwright and the OpenAI API.",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "openai",
    ],
)