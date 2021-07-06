import os

import jinja2

from mdpreview.util import share

templates = os.path.join(share, "templates")

env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates))


def render_template(path: str, **context):
    template = env.get_template(path)
    return template.render(**context)
