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

share = "/usr/share/mdpreview"
os.system(f"mkdir -p {share}")
templates = os.path.join(share, "templates")
if os.path.isdir(templates):
    shutil.rmtree(templates)
shutil.copytree("templates", templates)

static = os.path.join(share, "static")
if os.path.isdir(static):
    shutil.rmtree(static)
shutil.copytree("static", static)

service = "/etc/systemd/system/mdpreviewd.service"
if os.path.exists(service):
    os.remove(service)
shutil.copyfile("systemd/mdpreviewd.service", service)
