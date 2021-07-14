import os
import re
import shutil
from subprocess import PIPE, Popen

from setuptools import setup


def git_version():
    proc = Popen(["git", "describe"], stdout=PIPE)
    out, err = proc.communicate()
    out = out.decode()
    match = re.match(r'^(\d+\.\d+-\d+)(?:.*)?', out)
    return match.group(1).replace("-", ".")


setup(name="mdpreview",
      version=git_version(),
      description="VIM Markdown Preview HTTP server",
      author="Kevin Morris",
      author_email="kevr@0cost.org",
      url="https://www.github.com/kevr/mdpreview",
      packages=['mdpreview'],
      scripts=['bin/mdpreviewd'])

home = os.environ.get("HOME")

systemd_path = os.path.join(home, ".config", "systemd", "user")
if not os.path.exists(systemd_path):
    os.makedirs(systemd_path)

service = os.path.join(systemd_path, "mdpreviewd.service")
if os.path.exists(service):
    os.remove(service)
shutil.copyfile("systemd/mdpreviewd.service", service)
