import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rc-server-sdk",
    version="3.1.3",
    author="zhanglei1",
    author_email="zhanglei1@rongcloud.cn",
    description="rongcloud python server sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rongcloud/server-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
