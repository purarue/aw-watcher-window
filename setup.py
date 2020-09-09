import io
from setuptools import setup, find_packages

requirements = ["logzero", "python-xlib"]

# Use the README.md content for the long description:
with io.open('README.md', encoding='utf-8') as fo:
    long_description = fo.read()

setup(
    name='window_watcher',
    version="0.2.0",
    url='https://github.com/seanbreckenridge/aw-watcher-window',
    author="Erik Bjäreholt <erik@bjareho.lt>, Sean Breckenridge <seanbrecke@gmail.com>",
    description=('''a fork of aw-watcher-window to log window events to a file'''),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(include=['window_watcher']),
    install_requires=requirements,
    keywords='xlib data',
    entry_points={"console_scripts": ["window_watcher = window_watcher.__main__:main"]},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
