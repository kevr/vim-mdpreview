import os
import shutil

from setuptools import setup

setup(name="mdpreview",
      version="1.0.0",
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
