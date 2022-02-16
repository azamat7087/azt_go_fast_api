# encoding: utf-8
# module unicodedata
import unicodedata

import transliterate
import re


def has_cyr(s):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(s.lower()) != set()


def slugify(value, allow_unicode=False):

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def gen_slug(s):
    if has_cyr(s):
        s = transliterate.translit(s, reversed=True)
    new_slug = slugify(s, allow_unicode=True)

    return new_slug
