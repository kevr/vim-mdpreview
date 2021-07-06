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

share = os.path.join(home, ".local", "share", "mdpreview")
if os.path.isdir(share):
    shutil.rmtree(share)
os.makedirs(share)

templates = os.path.join(share, "templates")
shutil.copytree("templates", templates)

static = os.path.join(share, "static")
shutil.copytree("static", static)

systemd_path = os.path.join(home, ".config", "systemd", "user")
if not os.path.exists(systemd_path):
    os.makedirs(systemd_path)

service = os.path.join(systemd_path, "mdpreviewd.service")
if os.path.exists(service):
    os.remove(service)
shutil.copyfile("systemd/mdpreviewd.service", service)

# Reload user services.
os.system("systemctl --user daemon-reload")
