from setuptools import setup, find_packages

setup(
    name="demo_maker",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    description="AI-powered application for creating narrated demo videos",
    author="DemoMaker Team",
    install_requires=[
        # Core dependencies will be specified in requirements.txt
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
