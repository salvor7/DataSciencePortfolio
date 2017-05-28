import setuptools

setuptools.setup(
    name="MarkovChainBibleBot",
    version="0.1.0",
    url="https://github.com/salvor7/MarkovChainBibleBot",

    author="Andrew AH Brown",
    author_email="andrew.ah.brown@gmail.com",

    description="An absurdist bible quote generating bot, released on twitter.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
