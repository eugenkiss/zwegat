from distutils.core import setup

setup(
    name='zwegat',
    version='0.1',
    author='Eugen Kiss',
    author_email='eugen@eugenkiss.com',
    packages=[],
    scripts=['zwegat.py'],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': [
            'zwegat = zwegat:main',
        ],
    }
)
