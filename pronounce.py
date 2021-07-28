# -*- coding: utf-8 -*-


import phonological


JONGMATCHING = {'ㄱ':'ㄱ', 'ㄲ':'ㄱ', 'ㅋ':'ㄱ', 'ㄳ': 'ㄱ',
                      'ㄷ': 'ㄷ', 'ㄸ': 'ㄷ', 'ㅌ': 'ㄷ', 'ㅅ': 'ㄷ', 'ㅆ': 'ㄷ', 'ㅈ': 'ㄷ', 'ㅊ': 'ㄷ',
                      'ㅍ': 'ㅂ',
                      'ㄵ': 'ㄴ',
                      'ㄼ': 'ㄹ', 'ㄽ': 'ㄹ', 'ㄾ': 'ㄹ',
                      'ㅄ': 'ㅂ',
                      'ㄺ': 'ㄱ',
                      'ㄻ': 'ㅁ',
                      'ㄿ': 'ㅂ'}



# 표준 발음법에 따른 변환 결과를 반환
def pronounce(sentence):
    seperated = phonological.seperate(sentence)
    
    # 4장 받침의 발음
    
    for i in len(seperated):
        syl = seperated[i]
        nextsyl = seperated[i+1]
        if i+1 < len(seperated):
            nextsyl = phonological.Character('-')

        if not syl.isjongEmpty():
            p = syl.jong()
            syl.setJong(JONGMATCHING[p])
            
            if p == 'ㄼ':
                # ‘밟-’은 자음 앞에서 [밥]으로 발음
                if syl == '밟':
                    if phonological.isJa(nextsyl.cho()):
                        syl.setJong('ㅂ')
                # ‘넓-’은 넓죽하다, 넓둥글다만 [넙]으로 발음
                elif syl == '넓':
                    if nextsyl == '죽' or nextsyl == '둥':
                        syl.setJong('ㅂ')
                    
            elif p == 'ㄺ':
                '''용언의 어간인''' # ‘ㄺ’은 ‘ㄱ’ 앞에서 [ㄹ]로 발음한다. ex) 맑고[말꼬]
                if nextsyl.cho() == 'ㄱ':
                    syl.setJong('ㄹ')
            
            # 제12항  받침 ‘ㅎ’의 발음
            elif p in 'ㅎㄶㅀ':
                if nextsyl.cho() in 'ㄱㄷㅈ':
                    syl.setJongEmpty()
                    nextsyl.setCho('ㅋㅌㅊ'['ㄱㄷㅈ'.index(nextsyl.cho())])
                elif nextsyl.cho() == 'ㅎ':
                    '''작성중'''
                    pass
                    
                    
                    