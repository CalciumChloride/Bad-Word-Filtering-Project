# -*- coding: utf-8 -*-


import config, phonological


matching = []


with open('matching.txt', 'r', encoding='utf-8') as _f:
    _lines = _f.readlines()
    for _line in _lines:
        if _line[0] == '%':
            continue
        a = _line.strip().split()
        a[0] = a[0].replace('#', config._jongsung_seperator)
        a[1] = a[1].replace('#', config._jongsung_seperator)
        a[0] = a[0].replace('-', config._jongsung_empty)
        a[1] = a[1].replace('-', config._jongsung_empty)
        matching.append(a)
    


# 표준 발음법에 따른 변환 결과를 반환
def pronounce(sentence):
    thime = phonological.str_to_thime(sentence)
    for m in matching:
        if thime != thime.replace(m[0], m[1]):
            print(f'[{phonological.thime_to_str(thime)}] >',
                  f'[{phonological.thime_to_str(thime.replace(m[0], m[1]))}]')
        thime = thime.replace(m[0], m[1])
    converted = phonological.thime_to_str(thime)
    return converted
    
    
if __name__ == '__main__':
    anan = input('입력하세요: ')
    print(pronounce(anan))
    