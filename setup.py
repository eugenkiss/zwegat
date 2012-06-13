from distutils.core import setup

setup(
    name='zwegat',
    version='0.2',
    author='Eugen Kiss',
    author_email='eugen@eugenkiss.com',
    packages=[],
    scripts=['zwegat.py'],
    install_requires=[
        'pyparsing >= 1.5.6'
    ],
    entry_points = {
        'console_scripts': [
            'zwegat = zwegat:main',
        ],
    }
)
