from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    """
    This function will return the list of requirements.
    """
    requirements_lst: List[str] = []

    try:
        with open("requirements.txt", "r") as file:
            # Read lines from requirements.txt
            lines = file.readlines()

            # Process each line
            for line in lines:
                requirement = line.strip()

                # Ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    requirements_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirements_lst


setup(
    name="Networksecurity",
    version="0.0.1",
    author="ujjwal  ",
    author_email="ujjawal5105@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
