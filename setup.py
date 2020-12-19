import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recommendation_app",
    version="0.0.1",
    author="Steffem Klempau",
    author_email="steffen.klempau@yahoo.de",
    description="Recommendation system with REST endpoint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steffenkk/recommendation-app",
    package_dir={"recommendation_app": "src"},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "prep = src.prepare:process",
        ]
    },
    python_requires=">=3.6",
)
