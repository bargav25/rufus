from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    description="A tool for intelligent web data extraction using Playwright and the OpenAI API.",
    author="Bargav",
    author_email="jbargav025@gmail.com",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "openai",
    ],
    entry_points={
        'console_scripts': [
            'rufus=rufus.client:main',  # If you add a main() function for CLI usage
        ],
    },
)