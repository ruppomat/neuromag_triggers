from setuptools import setup, find_packages

setup(
    name="neuromag_triggers",
    version="0.1.0",
    description="Detect digital triggers from raw Neuromag STI channels with rising edge and refractory logic.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mne",
        "numpy",
        "pandas"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)