# -*- coding: utf-8 -*-

'''
2021.07.28 다운로드 후 변형
https://github.com/neotune/python-korean-handler
깃허브코드 복붙가능한가요?? 일단 복붙했는데 문제시 수정
'''

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


# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

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


class Character():
    ''' Super class '''
    def __init__(self):
        self.char = ' '
        self.hangul = -1
        
        
    def __eq__(self, other):
        if issubclass(type(other), Character):
            return self.char == other.char
        elif type(other) == str:
            return self.char == other
        else:
            return False
        
        
    def isHangul(self):
        return self.hangul
    
    def isjongEmpty(self):
        return False
    
    def cho(self):
        return self.char
    
    def jung(self):
        return self.char
    
    def jong(self):
        return self.char


class NoneHangulChar(Character):
    def __init__(self, char):
        self.char = char
        self.hangul = 0
        

class HangulSyllable(Character):
    def __init__(self, char):
        self.char = char
        self.p = seperate(self.char)
        self.hangul = 0
        
    
    def seperate(self, keyword):
        char_code = ord(keyword) - BASE_CODE
        d = {}
        
        char1 = int(char_code / CHOSUNG)
        d['cho'] = CHOSUNG_LIST[char1]
        
        char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
        d['jung'] = JUNGSUNG_LIST[char2]
        
        char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
        if char3==0:
            d['jong'] = '#'
        else:
            d['jong'] = JONGSUNG_LIST[char3]
                    
        return d

    
    def isjongEmpty(self):
        return self.p['jong'] == '#'
    
    def cho(self):
        return self.p['cho']
    
    def jung(self):
        return self.p['jung']
    
    def jong(self):
        return self.p['jong']
    
    def setCho(self, t):
        self.p['cho'] = t
    
    def setJung(self, t):
        self.p['jung'] = t
    
    def setJong(self, t):
        self.p['jong'] = t
        
    def setJongEmpty(self):
        self.p['jong'] = '#'
    


def seperate(test_keyword):
    split_keyword_list = list(test_keyword)

    result = list()
    for keyword in split_keyword_list:
        if isHangulSyllable(keyword):
            result.append(HangulSyllable(keyword))
        else:
            result.append(NoneHangulChar(keyword))
            
    return result


def join(keyword_list):
    pass
    

if __name__ == '__main__':
    print(seperate('일단 앉아봐!'))
