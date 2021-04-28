from setuptools import find_packages, setup
setup(
    name='geotiflib',
    version='1.0.9',
    description='GeoTiff Python library utils',
    author='GeoSolutions',
    license='GNU General Public License v3',
    install_requires=['beautifulsoup4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.2', 'pytest-mock==3.5.1', 'mock==2.0.0'],
    test_suite='tests',
    packages=find_packages(),
    include_package_data=True
)
