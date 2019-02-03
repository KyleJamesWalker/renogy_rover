from setuptools import setup, find_packages

readme = open('README.rst').read()

requirements = {
    "package": [
        "expiringdict",
        "pymodbus",
        "yamlsettings",
    ],
    "test": [
        "pytest",
        "pytest-mock",
        "pytest-pudb",
    ],
    "setup": [
        "pytest-runner",
    ],
}

requirements.update(all=sorted(set().union(*requirements.values())))

setup(
    name='renogy_rover',
    version='0.0.1',
    description='MODBUS Driver for the Renogy Rover 20A/40A Charge Controller',
    long_description=readme,
    author='Kyle James Walker',
    author_email='KyleJamesWalker@gmail.com',
    url='https://github.com/KyleJamesWalker/renogy_rover',
    packages=find_packages(),
    package_dir={'renogy_rover': 'renogy_rover'},
    include_package_data=True,
    install_requires=requirements['package'],
    extras_require=requirements,
    setup_requires=requirements['setup'],
    license='MIT',
    entry_points={
        "console_scripts": [
            "renogy = renogy_rover.__main__:main",
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=requirements['test'],
)
