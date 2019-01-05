from setuptools import setup

setup(
    name='snapshotalyzer',
    version='0.1',
    author="Hananto Prabowo",
    author_email="hanantoprabowo@yahoo.de",
    description="SnapshotAlyzer is a tool to manage AWS EC2 snapshots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/hanantoprabowo/snapshotalyzer",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)