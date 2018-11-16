from blog_poster import jinja_env
from collections import namedtuple

Tag = namedtuple('Tag', 'char index open_state void')
# Filter chars
FORMAT_CHARS = set(['_', '`', '>', '*'])

HTML_TAGS = {'_': {'open': '<span style="font-style: italic;">', 'close': '</span>'},
             '>': {'open': '<blockquote>', 'close': '</blockquote>'},
             '**': {'open': '<b>', 'close': '</b>'},
             '`': {'open': '<code style="font-family: \'Consolas\', \
                        \'Menlo\', \'Deja Vu Sans Mono\', \
                        \'Bitstream Vera Sans Mono\', monospace !important; \
                        font-size: 15px;">', 'close': '</code>'},
             '```': {'open': '<pre style="font-family: \'Consolas\', \
                        \'Menlo\', \'Deja Vu Sans Mono\', \
                        \'Bitstream Vera Sans Mono\', monospace !important; \
                        font-size: 15px;"><code>', 'close': '</code></pre>'}}


class BlogFilter():

    def __init__(self, text_string):

        self.tags = []

        self.tag_states = {'_': False,
                           '`': False,
                           '>': False,
                           '**': False,
                           '```': False}

        self.star_count, self.tick_count = 0, 0

        self.text_string = text_string

        self.text_list = list(text_string)

        self.filter(self.text_list)

        self.html_text = self.insert_tags()

    def filter(self, text_list):

        for index, char in enumerate(text_list):

            if char in FORMAT_CHARS:

                if char == '*':

                    self.star_count += 1

                    if self.star_count == 2:

                        self.make_bold_tag(index)

                    self.tick_count = 0

                elif char == '`':

                    self.tick_count += 1

                    if self.tick_count == 1 and text_list[index+1] != '`':

                        self.make_tag(char, index)

                    elif self.tick_count == 3:

                        self.make_code_block_tag(index)

                    self.star_count = 0

                else:

                    self.make_tag(char, index)

        return self.tags

    def make_bold_tag(self, index):

        self.tag_states['**'] = not self.tag_states['**']
        tag = Tag('**', index-1, self.tag_states['**'], self.tag_states['```'])
        self.tags.append(tag)
        self.star_count = 0

    def make_code_block_tag(self, index):

        self.tag_states['```'] = not self.tag_states['```']
        tag = Tag('```', index-2, self.tag_states['```'], False)
        self.tags.append(tag)
        self.tick_count = 0

    def make_tag(self, char, index):

        self.tag_states[char] = not self.tag_states[char]
        tag = Tag(char, index, self.tag_states[char], self.tag_states['```'])
        self.tags.append(tag)
        self.star_count, self.tick_count = 0, 0

    def insert_tags(self):

        html_text = ''

        _shift = 0

        for tag in self.tags:

            if tag.void is False:

                if tag.open_state is True:
                    tag = HTML_TAGS[tag.char]['open']
                else:
                    tag = HTML_TAGS[tag.char]['close']

                html_text += self.text_string[:tag.index] + tag

        if tag.void is False:

            if tag.char == '**':
                _shift = 2
            elif tag.char == '```':
                _shift = 3

        html_text += self.text_string[tag.index+_shift:]

        return html_text

    return ''.join(split)
    '''
    textarea, code, pre {
	font-family: 'Consolas', 'Menlo', 'Deja Vu Sans Mono', 'Bitstream Vera Sans Mono', monospace !important;
	font-size: 15px;
    }
    '''

    # if text surrounded by `text`, make a code text

    # if text surrounded by ```text``` make a code block

    # if text surrounded by > text > make a quote block

    # if text surrounded by _text_ make italic

    # if text surrounded by **text** make bold

    # if text surrounded by [text](link), make link
