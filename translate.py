import sys

from bs4 import BeautifulSoup as BS
from yandex_translate import YandexTranslate, YandexTranslateException
from json import load, dump
key = open('/home/dan/.yandex/key').read()
translate = YandexTranslate(key)

def do_translate(fname):
    TM = load(open('dic.json'))
    xml = BS(open(fname).read(), features='xml')
    for mxCell in xml('mxCell'):
        try:
            _in = mxCell['value']
            try:
                _out = TM['_in']
            except KeyError:
                _out = translate.translate(_in, 'ru-en')['text'][0]
                TM.update({_in:_out})
            mxCell['value'] = _out
        except KeyError:
            pass
        except YandexTranslateException:
            pass
    dump(TM, open('dic.json','w'), ensure_ascii = 0, indent = 2)
    return xml.prettify()
    
if __name__ == '__main__':
    try:
        translated = do_translate(sys.argv[1])
        open("%s.tr" % sys.argv[1],'w').write(translated)
    except IndexError:
        print('!!!')

