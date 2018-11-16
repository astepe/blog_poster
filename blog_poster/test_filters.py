from blog_poster.blog_filter import *

TEST_TEXT = 'hello _everyone_ how **are** >you> `today` ```this is`_** an >example> of a code block```'


def test_blog_filter(string=TEST_TEXT):

    html = blog_filter(string)
    assert html == 'hello <span style="font-style: italic;">everyone</span> how <b>are</b> <blockquote>you</blockquote> <code>today</code> <pre><code>this is`_** an >example> of a code block</code></pre>'


def test_make_tag():

    states = FilterStates(TEST_TEXT)
    make_tag(states, '_', 5, states.tag_states['```'])
    make_tag(states, '**', 8, states.tag_states['```'])
    states.tag_states['```'] = True
    make_tag(states, '**', 13, states.tag_states['```'])
    assert states.tags == [('_', 5, True, False),
                           ('**', 8, True, False),
                           ('**', 13, False, True), ]


class TestInsertTags:

    def test_insert_italics(self):

        states = FilterStates('#_hi_#')
        states.tags = [TAG('_', 1, True, False), TAG('_', 4, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<span style="font-style: italic;">hi</span>#'

    def test_insert_bold(self):

        states = FilterStates('#**hi**#')
        states.tags = [TAG('**', 1, True, False), TAG('**', 5, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<b>hi</b>#'

    def test_insert_code_block(self):

        states = FilterStates('#```hi```#')
        states.tags = [TAG('```', 1, True, False), TAG('```', 6, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<pre><code>hi</code></pre>#'

    def test_insert_code_text(self):

        states = FilterStates('#`hi`#')
        states.tags = [TAG('`', 1, True, False), TAG('`', 4, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<code>hi</code>#'

    def test_quote_block(self):

        states = FilterStates('#>hi>#')
        states.tags = [TAG('>', 1, True, False), TAG('>', 4, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<blockquote>hi</blockquote>#'

    def test_void_action(self):

        states = FilterStates('#```>hello,> world```#')
        states.tags = [TAG('```', 1, True, False), TAG('>', 4, True, True), TAG('>', 11, False, True), TAG('```', 18, False, False)]
        string = ''.join(states.string_list)
        html = insert_tags(states, string)
        assert html == '#<pre><code>>hello,> world</code></pre>#'

class TestInspectChar:

    def test_italics(self):

        states = FilterStates(TEST_TEXT)
        inspect_char(states, '_', 1)
        assert states.tags == [('_', 1, True, False)]

    def test_bold(self):

        states = FilterStates(TEST_TEXT)
        inspect_char(states, '*', 1)
        inspect_char(states, '*', 2)
        assert states.tags == [('**', 1, True, False)]

    def test_code_block(self):

        states = FilterStates('```TEST_TEXT```')
        inspect_char(states, '`', 0)
        inspect_char(states, '`', 1)
        inspect_char(states, '`', 2)
        assert states.tags == [('```', 0, True, False)]

    def test_code_text(self):

        states = FilterStates(TEST_TEXT)
        inspect_char(states, '`', 1)
        assert states.tags == [('`', 1, True, False)]

    def test_quote_block(self):

        states = FilterStates(TEST_TEXT)
        inspect_char(states, '>', 1)
        assert states.tags == [('>', 1, True, False)]

    def test_void_action(self):

        states = FilterStates('```TEST_TEXT>TEST_TEXT>```')
        inspect_char(states, '`', 1)
        inspect_char(states, '`', 2)
        inspect_char(states, '`', 3)
        states.tags = []
        inspect_char(states, '>', 12)
        # assert that the void value has been changed
        assert states.tags == [('>', 12, True, True)]
