from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).parent.absolute()

with open(here / 'README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hubmap-pipeline-release-mgmt',
    version='0.2',
    description='Management scripts for releasing HuBMAP computational pipelines',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/hubmapconsortium/pipeline-release-mgmt',
    author='Matt Ruffalo',
    author_email='mruffalo@cs.cmu.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='docker automation',
    packages=find_packages(),
    install_requires=[
        'multi-docker-build>=0.3',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'tag_release_pipeline=hubmap_pipeline_release_mgmt.tag_release_pipeline:main',
        ],
    },
)
