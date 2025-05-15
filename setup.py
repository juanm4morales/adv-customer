from setuptools import setup, find_packages

setup(
    name="adversarial-bot",
    version="0.1.0",
    description="A project to simulate conversations between customers and chatbots.",
    author="juanm4morales",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "requests",
        "python-dotenv",
        "langchain-openai",
        "langgraph",
    ],
    entry_points={
        "console_scripts": [
            "simulate-conversation=adv_customer.main:main",
        ],
    },
)