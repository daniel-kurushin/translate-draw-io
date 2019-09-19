import sys
import re

from yandex_translate import YandexTranslate, YandexTranslateException
from json import load, dump
from lingv import wrap, join
key = open('/home/dan/.yandex/key').read()
translate = YandexTranslate(key)

pattern = re.compile('"(.*?)"', flags=re.MULTILINE | re.DOTALL)
digit = re.compile('\d+', flags=re.MULTILINE | re.DOTALL)

def do_translate(dot):
    TM = load(open('dic.json'))
    updated = 0
    for _in in map( lambda x : x.group().replace('"','') ,re.finditer(pattern, dot)):
        _in_joined = join(_in.split())
        print(_in_joined)
        if re.match(digit, _in_joined):
            _out = _in
        else:
            try:
                _out = TM[_in_joined]
            except KeyError:
                _out = translate.translate(_in, 'ru-en')['text'][0]
                TM.update({_in_joined:_out})
                updated = 1
            except YandexTranslateException:
                pass
        yield _in, _out
    if updated:
        dump(TM, open('dic.json','w'), ensure_ascii = 0, indent = 2)
    
if __name__ == '__main__':
    try:
        dot = open(sys.argv[1]).read()
        for _from, _to in do_translate(dot):
            print(_from, _to)
            dot = dot.replace('"%s"' % _from, '"%s"' % _to)
        
        open("%s.tr" % sys.argv[1],'w').write(dot)
    except IndexError:
        print('!!!')

