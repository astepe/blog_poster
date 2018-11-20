from selenium import webdriver
from blog_poster.blog_filter import blog_filter
from blog_poster import jinja_env
from urllib.parse import quote


class PreviewWindow():
    """
    for html previewing upon typing into text editor
    """

    def __init__(self, raw_text='enter text to see preview!'):

        self.window = webdriver.Firefox()
        self.raw_text = raw_text

        self.update_preview(raw_text)

    def update_preview(self, raw_text):

        y_offset = self.window.execute_script('return window.pageYOffset')

        self.raw_text = raw_text
        html = blog_filter(raw_text)

        template = jinja_env.get_template('blog_post.html')

        self.window.get("data:text/html;charset=utf-8," +
                        quote(template.render(text=html)))

        js_script = f'window.scrollTo(0, {y_offset})'

        self.window.execute_script(js_script)

        return html
