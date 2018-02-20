from setuptools import setup
import os

# allow setup.py to be run from any path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

README = "Provides tonetutor user management models."

setup(
    name="tonetutor_usermgmt",
    version="0.0.4",
    author="Jivan Amara",
    author_email="Development@JivanAmara.net",
    packages=['usermgmt', 'usermgmt.migrations'],
    include_package_data=True,
    package_data={
        'usermgmt': ['templates/usermgmt/user_profile.html'],
    },
    description=README,
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
    ],
)
