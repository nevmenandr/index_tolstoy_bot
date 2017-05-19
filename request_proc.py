#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 19.05.2017 10:20:21 MSK

import re
import urllib.request
from urllib.parse import quote

def pars_page(page):
    persons = re.findall('<td><a href="/person/(.+?)/">(.+?)</a>', page)
    keymap = {}
    for person in persons:
        keymap[person[1]] = person[0]
    return keymap
    

def query_to_app(term):
    try:
        response = urllib.request.urlopen('http://index.tolstoy.ru/search/?query={0}'.format(quote(term)))
        the_page = response.read().decode('utf-8')
        response.close()
        return pars_page(the_page)
    except:
        return 'No result'
    

def search_term(term):
    if re.search('[a-zA-Zа-яА-Я]', term):
        return query_to_app(term)
    else:
        return None

def main():
    print(search_term('Афанасий'))
    return 0

if __name__ == '__main__':
    main()

