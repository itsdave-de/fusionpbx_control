from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in fusionpbx_control/__init__.py
from fusionpbx_control import __version__ as version

setup(
	name="fusionpbx_control",
	version=version,
	description="Connect to FusionPBX",
	author="itsdave GmbH",
	author_email="dev@itsdave.de",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
