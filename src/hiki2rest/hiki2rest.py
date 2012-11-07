# -*- coding: utf-8 -*-
import urllib2
import os
import re
import glob
import json
from io import StringIO


# get title from filename
def decode_title(title):
    return unicode(urllib2.unquote(title),
                   'euc-jp').encode('utf-8').replace('"', '\\"')


def replace_string(text, key_repl):
    for pair in key_repl.items():
        text = text.replace(pair[0], pair[1])
    return text


def replace_time(text):
    pat_timeat = re.compile('Time.at\((\d+)\)')
    match_timeat_list = pat_timeat.findall(text)
    for timestamp in match_timeat_list:
        text = pat_timeat.sub(timestamp, text)
    return text


def replace_keyword(text):
    pat = re.compile('((\\\\\d\d\d)+)')

    text_converted = ''
    for line in text.split('\n'):
        match = pat.search(line)
        repl_str = ''
        if match:
            for i in match.group(0).split('\\')[1:]:
                repl_str += str(chr(int('0' + str(i), 8)))
            repl_str_encoded = unicode(repl_str, 'euc-jp').encode('utf-8')
            text_converted += pat.sub(repl_str_encoded, line) + '\n'
        else:
            text_converted += line + '\n'

    return text_converted

""" get body txt
with open('text/vi%A4%F2%BC%C2%B9%D4%A4%C7%A4%AD%A4%CA%A4%A4') as f:
    body_text = unicode(f.read(), 'euc-jp').encode('utf-8')
"""

key_repl = {
    ':count => ': '"count": ',
    ':editor => ': '"editor": ',
    ':freeze => ': '"freeze": ',
    ':keyword => ': '"keywords": ',
    ':last_modified => ': '"last_modified": ',
    ':references => ': '"references": ',
    ':title => ': '"title": ',
    ' => ': ': '
}

os.chdir('data')
with open('info.db') as f:
    meta_text = f.read()

os.chdir('text')
title_decoded_title_pair = {i: decode_title(i) for i in glob.glob('*')}

tmp1 = replace_keyword(meta_text)
tmp2 = replace_string(tmp1, key_repl)
tmp3 = replace_time(tmp2)
tmp4 = unicode(tmp3, 'utf-8').encode('utf-8')
#tmp5 = json.JSONEncoder(object).encode(tmp4)
tmp5 = json.JSONEncoder(object).encode(tmp4)
tmp6 = tmp5.decode('utf-8')
io = StringIO(tmp6)
print json.load(io).encode('utf-8')
