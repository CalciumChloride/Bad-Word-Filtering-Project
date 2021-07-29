# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:42:11 2021

@author: KYH

https://github.com/neotune/python-korean-handler
https://github.com/JDongian/python-jamo/blob/master/jamo/jamo.py
참고함

"""

import re

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
모든 글자마다 앞에 _CHAR_WALL (Ş)
한글은 초성, 중성, 종성이 나뉘어
초성 앞에 _CHOSUNG_START (Ŀ)
중성 앞에 _JUNGSUNG_START (Ŵ)
종성 앞에 _JONGSUNG_START (Ŧ)
가 들어감
한글이 아닌 문자는 그대로 들어감

Ex) '앉' -> 'ŞĿᄋŴᅡŦᆬ'
    '강녕 hh!' -> 'ŞĿㄱŴᅡŦᆫŞĿᄂŴᅧŦᆼŞ ŞhŞhŞ!'
'''



_HANGUL_OFFSET = 44032
_CHOSUNG_OFFSET = 0x10ff
_JUNGSUNG_OFFSET = 0x1160
_JONGSUNG_OFFSET = 0x11a7


_CHAR_WALL = 'Ş'
_CHOSUNG_START = 'Ŀ'
_JUNGSUNG_START = 'Ŵ'
_JONGSUNG_START = 'Ŧ'

_EMPTY = ' '



# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def isHangulSyllable(letter):
    return re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', letter) is not None

def isJa(p):
    return p != 'ㅇ' and p in CHOSUNG_LIST


def _hgchar_seperate(keyword):
    rem = ord(keyword) - _HANGUL_OFFSET
    
    char3 = rem % 28
    if char3:
        tail = chr(char3 + _JONGSUNG_OFFSET)
    else:
        tail = _EMPTY
    
    char2 = 1 + ((rem - char3) % 588) // 28
    vowel = chr(char2 + _JUNGSUNG_OFFSET)
    
    char1 = 1 + rem // 588
    lead = chr(char1 + _CHOSUNG_OFFSET)
    
    return _CHOSUNG_START + lead + _JUNGSUNG_START + vowel + _JONGSUNG_START + tail


def _hgchar_join(lead, vowel, tail):
    lead  = ord(lead)  - _CHOSUNG_OFFSET
    vowel = ord(vowel) - _JUNGSUNG_OFFSET
    if tail == _EMPTY:
        tail = 0
    else:
        tail = ord(tail) - _JONGSUNG_OFFSET
    return chr(tail + (vowel - 1) * 28 + (lead - 1) * 588 + _HANGUL_OFFSET)
    



def str_to_thime(string):
    split_keyword_list = list(string)

    result = ''
    for keyword in split_keyword_list:
        result += _CHAR_WALL
        if isHangulSyllable(keyword):
            result += _hgchar_seperate(keyword)
        else:
            result += keyword
            
    return result


def thime_to_str(thime):
    keyword_list = thime.split(_CHAR_WALL)[1:]       # [0]은 ''
    result = ''
    for char in keyword_list:
        if char[0] == _CHOSUNG_START:
            result += _hgchar_join(char[1], char[3], char[5])
        else:
            result += char
            
    return result
    


if __name__ == '__main__':
    string = '휴!!잘된다~~'
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
    print('\n')

