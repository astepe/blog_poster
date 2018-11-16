from jinja2 import Environment, PackageLoader
from blog_poster.blog_filter import blog_filter

jinja_env = Environment(loader=PackageLoader('blog_poster.templates', 'templates'),
                        autoescape=False)

jinja_env.filters['blog_filter'] = blog_filter
