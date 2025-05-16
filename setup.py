# setup.py
from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="adversarial-bot",
    version="0.1.0",
    description="A project to simulate conversations between customers and chatbots.",
    author="juanm4morales",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=load_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "simulate-conversation=adv_customer.main:main",
        ],
    },
)