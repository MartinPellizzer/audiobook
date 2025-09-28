
def text_format(text):
    text = text.replace('1:10', 'one to ten')
    text = text.replace('1:5', 'one to five')
    text = text.replace('1:2', 'one to two')
    text = text.replace('1:1', 'one to one')
    text = text.replace('’', "'")
    return text
