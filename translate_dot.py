import sys
import re

#from yandex_translate import YandexTranslate, YandexTranslateException
from json import load, dump
from lingv import wrap, join
#key = open('/home/dan/.yandex/key').read()
#translate = YandexTranslate(key)

p = re.compile('"(.*?)"', flags=re.MULTILINE | re.DOTALL)

def do_translate(dot):
    TM = load(open('dic.json'))
    for _in in map( lambda x : x.group() ,re.finditer(p, dot)):
        _in_joined = _in.replace('\n', ' ').replace('"',' ')
        print(_in_joined)
        try:
            _out = TM[_in_joined]
        except KeyError:
            _out = _in_joined#translate.translate(_in, 'ru-en')['text'][0]
            TM.update({_in_joined:_out})
        except YandexTranslateException:
            pass
        yield _in, wrap(_out)
    dump(TM, open('dic.json','w'), ensure_ascii = 0, indent = 2)
    
if __name__ == '__main__':
    try:
        dot = open(sys.argv[1]).read()
        for _from, _to in do_translate(dot):
            dot = dot.replace('"%s"' % _from, '"%s"' % _to)
        
        open("%s.tr" % sys.argv[1],'w').write(dot)
    except IndexError:
        print('!!!')

