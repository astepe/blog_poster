
def blog_filter(raw_text):

    count = raw_text.count('_')
    if count % 2 == 1:
        count -= 1

    split = raw_text.split('_', maxsplit=count)

    for i in range(1, len(split), 2):
        split[i] = '<span style="font-style: italic;">' + split[i] + '</span>'

    return ''.join(split)



    # if text surrounded by `text`, make a code text

    # if text surrounded by '''text''' make a code block

    # if text surrounded by > text > make a quote block

    # if text surrounded by _text_ make italic

    # if text surrounded by **text** make bold

    # if text surrounded by [text](link), make link
