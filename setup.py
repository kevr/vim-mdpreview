import re
from subprocess import PIPE, Popen

from setuptools import setup

VERSION = "0.4.7"


def git_version():
    proc = Popen(["git", "describe", "--long"], stdout=PIPE)
    out, err = proc.communicate()
    out = out.decode()
    if proc.returncode != 0:
        return VERSION
    match = re.match(r'^(\d+\.\d+[-.]\d+)(?:.*)?', out)
    return match.group(1).replace("-", ".")


setup(name="mdpreview",
      version=git_version(),
      description="VIM Markdown Preview HTTP server",
      author="Kevin Morris",
      author_email="kevr@0cost.org",
      url="https://www.github.com/kevr/mdpreview",
      packages=['mdpreview'],
      scripts=['bin/mdpreviewd'],
      install_requires=[
          "typing-extensions==3.*,>=3.6.0"
      ])
