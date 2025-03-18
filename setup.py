from setuptools import find_packages, setup

setup(
    name="data_pipeline",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pyspark>=3.3.0",
        "delta-spark>=2.0.0",
        "pydantic>=2.0.0",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=1.0",
            "duckdb>=0.8.0",
        ],
    },
)