from jinja2 import Environment, PackageLoader, select_autoescape

jinja_env = Environment(
loader=PackageLoader('blog_poster.templates', 'templates'),
autoescape=False
)
