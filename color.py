__author__ = 'duzhengjie'


def in_black(s):
    return highlight('') + "%s[30;2m%s%s[0m" % (chr(27), s, chr(27))


def in_red(s):
    return highlight('') + "%s[31;2m%s%s[0m" % (chr(27), s, chr(27))


def in_green(s):
    return highlight('') + "%s[32;2m%s%s[0m" % (chr(27), s, chr(27))


def in_yellow(s):
    return highlight('') + "%s[33;2m%s%s[0m" % (chr(27), s, chr(27))


def in_blue(s):
    return highlight('') + "%s[34;2m%s%s[0m" % (chr(27), s, chr(27))


def in_purple(s):
    return highlight('') + "%s[35;2m%s%s[0m" % (chr(27), s, chr(27))


def in_white(s):
    return highlight('') + "%s[37;2m%s%s[0m" % (chr(27), s, chr(27))


def highlight(s):
    return "%s[30;2m%s%s[1m" % (chr(27), s, chr(27))





