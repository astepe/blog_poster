from collections import namedtuple
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

TAG = namedtuple('Tag', 'tag_type index open')

FORMAT_CHARS = {'_': 'italic', '`': 'code', '>': 'quote', '*': 'bold'}

HTML_TAGS = {'italic': {True: '<span style="font-style: italic;">', False: '</span>'},
             'quote': {True: '<blockquote>', False: '</blockquote>'},
             'bold': {True: '<b>', False: '</b>'},
             'code': {True: '<code>', False: '</code>'},
             'code_block': {'open': '<pre><code>', 'close': '</code></pre>'}
             }


class FilterStates():
    """
    for tracking states during text filtering
    """

    def __init__(self, string):

        self.tags = []

        self.tag_states = {'italic': False,
                           'code': False,
                           'quote': False,
                           'bold': False,
                           'code_block': False}

        self.star_count, self.tick_count = 0, 0

        self.text = string

        self.text_list = list(string)

    def __repr__(self):

        return self.tags, self.text


def blog_filter(raw_text):

    states = FilterStates(raw_text)

    for index, char in enumerate(states.text_list):

        if char in FORMAT_CHARS:
            tag_type = FORMAT_CHARS[char]
            count_char(tag_type, index, states)
        else:
            states.star_count, states.tick_count = 0, 0

    if states.tags:
        return insert_tags(states)
    else:
        return raw_text


def count_char(tag_type, index, states):

    within_code_block = states.tag_states['code_block']
    within_code_inline = states.tag_states['code']
    within_code = within_code_block or within_code_inline

    if tag_type == 'bold':

        states.star_count += 1
        states.tick_count = 0

        if states.star_count == 2 and not within_code:
                make_tag(tag_type, index-1, states)

    elif tag_type == 'code':

        states.tick_count += 1
        states.star_count = 0

        if states.tick_count == 1 and states.text_list[index+1] != '`':
            if not within_code_block:
                make_tag(tag_type, index, states)

        elif states.tick_count == 3:
            make_tag('code_block', index-2, states)

    elif not within_code:

        make_tag(tag_type, index, states)


def make_tag(tag_type, index, states):

    states.tag_states[tag_type] = not states.tag_states[tag_type]

    tag = TAG(tag_type, index, states.tag_states[tag_type])
    states.tags.append(tag)

    states.star_count, states.tick_count = 0, 0


def insert_tags(states):

    raw_text = states.text

    html_text = ''

    previous_tag_index = 0

    for idx, tag in enumerate(states.tags):

        if tag.tag_type == 'code_block':

            if not tag.open:

                highlight_start = states.tags[idx-1].index


                html_text += raw_text[previous_tag_index:highlight_start] + \
                             highlight(raw_text[highlight_start+3:tag.index],
                                       PythonLexer(),
                                       HtmlFormatter()
                                       )
                previous_tag_index = tag.index + 3

        else:

            html_tag = HTML_TAGS[tag.tag_type][tag.open]

            html_text += raw_text[previous_tag_index:tag.index] + html_tag

            if tag.tag_type == 'bold':
                index_offset = 2
            else:
                index_offset = 1

            previous_tag_index = tag.index + index_offset

    html_text += raw_text[previous_tag_index:]

    return html_text
