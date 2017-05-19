#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 19.05.2017 11:49:35 MSK

import json
import re
import urllib.request

def person_get_mentions(num):
    if re.search('[^0-9]', num):
        return None
    mentions_url = 'http://index.tolstoy.ru/person/mentions/'
    response = urllib.request.urlopen(mentions_url + num)
    jsonstring = response.read().decode('utf-8')
    response.close()
    data = json.loads(jsonstring)
    mentions = data['mentions']
    return mentions
    

def main():
    mentions = person_get_mentions('103')
    
    return 0

if __name__ == '__main__':
    main()

