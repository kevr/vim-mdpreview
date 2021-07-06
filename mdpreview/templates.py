import jinja2

# ../templates/
path = "/usr/share/mdpreview/templates"

env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))


def render_template(path: str, **context):
    template_ = env.get_template(path)
    return template_.render(**context)
