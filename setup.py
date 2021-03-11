import setuptools

setuptools.setup(
    name="bytesize-discord-bot",
    version="0.0.1",
    author="Connor Avery",
    author_email="",
    description="A lambda which houses a discord bot",
    long_description="A lambda which houses a discord bot",
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["handler=bot_handler:lambda_handler"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
