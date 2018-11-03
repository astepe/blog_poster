from selenium import webdriver
from blog_poster.filters import blog_filter
from blog_poster import jinja_env
from html import unescape
import os


class PreviewWindow():

    def __init__(self, raw_text='enter text to see preview!'):

        self.window = webdriver.Firefox()
        self.raw_text = raw_text
        self.update_preview(self.raw_text)

    def update_preview(self, raw_text):

        self.raw_text = raw_text

        html_text = blog_filter(raw_text)

        template = jinja_env.get_template('blog_post.html')

        self.window.get("data:text/html;charset=utf-8," + unescape(template.render(test=html_text)))
