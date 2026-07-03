import re


def bold_texts(html):
    return re.findall(r"<b>(.*?)</b>", html)


def quoted(text):
    return re.findall(r'"(.*?)"', text)


def dollar_amounts(text):
    return [int(s) for s in re.findall(r"(?<=\$)\d+", text)]


def split_camel(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
