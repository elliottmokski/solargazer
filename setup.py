from setuptools import setup, find_packages

setup(
    name='solargazer',
    version='0.2',
    packages=find_packages(),
    python_requires='>=3.6',
    author='Elliott Mokski',
    author_email='elliottpmokski@gmail.com',
    description='A simple wrapper for linearmodels to generate clean panel regression tables in LaTeX.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/elliottmokski/solargazer',
    install_requires=[
        'pandas>=1.0.0',
        'linearmodels>=5.0',
    ],
)