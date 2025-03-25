from setuptools import setup, find_packages 
from typing import List

def get_requirements() -> List[str]:
    """
        This function return a list of requirement packages for the project
    """
    requirement_list: List[str] = []
    try: 
        with open('requirements.txt', 'r') as file:
            #Readline 
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e.':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirement.txt not found")
        
    return requirement_list
print(get_requirements())

## Setup metadata 

setup(
    name = 'NetworkSecurity',
    version = '0.0.1',
    author= "Daniel Lai",
    author_email= "danhdanhtuan0308@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)
