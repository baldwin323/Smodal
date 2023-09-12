"""
This script contains several potential solutions for resolving pytest dependencies conflicts.  
Choose the method that suits best your project and comment out the rest.
"""

import os
import subprocess

# 1. Constrain one of the conflicting pytest dependencies to an exact version
def constrain_dependency_version():
    constraint_file = open("requirements.txt", "a")
    constraint_file.write("pytest==exact_version")
    constraint_file.close()

# 2. Upgrade all dependencies to the latest compatible version of pytest
def upgrade_to_latest_compatible_pytest():
    os.system("pip install --upgrade pytest")

# 3. Removing unnecessary pytest dependencies to avoid the version conflict
# Prepare requirements.txt and remove unnecessary packages in it. 

# 4. Installing conflicting dependencies in separate environments using virtualenv.
def install_dependencies_in_separate_envs():
    os.system("virtualenv venv")
    os.system("source venv/bin/activate")
    os.system("pip install -r requirements.txt")
    os.system("deactivate")

# CHECK YOUR CONFLICTS in your specific codebase and determine the optimal fix then uncomment related method and run it.
# constrain_dependency_version()
upgrade_to_latest_compatible_pytest()
# install_dependencies_in_separate_envs()