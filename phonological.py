# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:42:11 2021

@author: KYH

https://github.com/neotune/python-korean-handler
https://github.com/JDongian/python-jamo/blob/master/jamo/jamo.py
참고함

"""

import re
import config

"""
    초성 중성 종성 분리 하기
	유니코드 한글은 0xAC00 으로부터
	초성 19개, 중성21개, 종성28개로 이루어지고
	이들을 조합한 11,172개의 문자를 갖는다.

	한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
	(0xAC00은 'ㄱ'의 코드값)

	따라서 다음과 같은 계산 식이 구해진다.
	유니코드 한글 문자 코드 값이 X일 때,

	초성 = ((X - 0xAC00) / 28) / 21
	중성 = ((X - 0xAC00) / 28) % 21
	종성 = (X - 0xAC00) % 28

	이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
	이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.

	초성문자코드 = 초성 + 0x1100 //('ㄱ')
	중성문자코드 = 중성 + 0x1161 // ('ㅏ')
	종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
"""


'''
아래와 같은 인코딩 방식을 thime 이라고 하겠음 (맘대로 지음)
모든 글자마다 앞에 _CHAR_SEPERATOR (Ş)
한글은 초성, 중성, 종성이 나뉘어
종성 앞에 _JONGSUNG_SEPERATOR (Ŧ)
가 들어감
한글이 아닌 문자는 그대로 들어감
'''



_HANGUL_OFFSET = 44032

_JONGSUNG_SEPERATOR = config._jongsung_seperator
_JONGSUNG_EMPTY = config._jongsung_empty



# 초성 리스트. 00 ~ 18
_CHOSUNG_LIST = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')

# 중성 리스트. 00 ~ 20
_JUNGSUNG_LIST = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
_JONGSUNG_LIST = [_JONGSUNG_EMPTY] + list('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')


def isHangulSyllable(letter):
    if type(letter) == str and len(letter) == 1:
        return re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', letter) is not None
    else:
        raise Exception(f'Error: isHangulSyllable({letter}) : 인자는 한 글자 문자열이어야 함')

def isJa(p):
    return p in _CHOSUNG_LIST


def _hgchar_seperate(keyword):
    if type(keyword) == str and len(keyword) == 1 and isHangulSyllable(keyword):
        char_code = ord(keyword) - _HANGUL_OFFSET
        
        char1 = char_code // 588
        lead = _CHOSUNG_LIST[char1]
        
        char2 = (char_code - (588 * char1)) // 28
        vowel = _JUNGSUNG_LIST[char2]
        
        char3 = int((char_code - (588 * char1) - (28 * char2)))
        tail = _JONGSUNG_EMPTY
        if char3:
            tail = _JONGSUNG_LIST[char3]
        
        return lead + vowel + _JONGSUNG_SEPERATOR + tail
    else:
        raise Exception(f'Error: _hgchar_seperate({keyword}) : 인자는 한글 한 글자여야 함')


def _hgchar_join(lead, vowel, tail=_JONGSUNG_EMPTY):
    try:
        lead = _CHOSUNG_LIST.index(lead)
        vowel = _JUNGSUNG_LIST.index(vowel)
        tail = _JONGSUNG_LIST.index(tail)
        return chr((((lead * 21) + vowel) * 28 + tail) + _HANGUL_OFFSET)
    except ValueError as e:
        print(e)
        print(f'_hgchar_join({lead}, {vowel}, {tail}) : 인자는 한글 초성, 중성, 종성 하나씩이어야 함')
    



def str_to_thime(string):
    if type(string) != str:
        raise Exception(f'str_to_thime({string}) : 인자는 문자열이어야 함')
        return
    
    split_keyword_list = list(string)

    result = ''
    for keyword in split_keyword_list:
        if isHangulSyllable(keyword):
            result += _hgchar_seperate(keyword)
        else:
            result += keyword
            
    return result



def thime_to_str(thime):
    result = ''
    i = 0
    while i < len(thime):
        if isJa(thime[i]):
            char = thime[i:i+4]
            try:
                result += _hgchar_join(char[0], char[1], char[3])
            except:
                print(f'thime_to_str 잘못된 문자열 | {char}')
            i += 4
            
        else:
            result += thime[i]
            i += 1
            
    return result
    


if __name__ == '__main__':
    string = '휴!!잘 된다~~'
    print('\n원래:')
    print(string)
    print('\n')
    
    thime = str_to_thime(string)
    print('\nTHIME:')
    print(thime)
    print('\n')
    
    won = thime_to_str(thime)
    print('\n되돌림:')
    print(won)
    print('같은가?', won == string)
    print('\n')

