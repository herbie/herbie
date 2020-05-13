from setuptools import setup

setup(
    name='herbie',
    version='0.1.0',
    packages=['herbie'],
    url='https://github.com/herbie/herbie',
    license='MIT',
    author='',
    author_email='',
    description='Herbie',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    install_requires=["django>=2.2"],
)