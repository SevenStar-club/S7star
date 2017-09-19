#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2015 alpha1e0
================================================================
社工密码生成器.
'''


import time
import itertools



class PasswdGenerator(object):
    '''
    Password generator.
    '''
    # 常用密码关键数字
    _numList = ['123456', '123123', '123123123', '112233', '445566', '456456', '789789', '778899', '321321', '520', '1314', '5201314', '1314520', '147369', '147258', '258', '147', '456', '789', '147258369', '111222', '123', '1234', '12345', '1234567', '12345678', '123456789', '987654321', '87654321', '7654321', '654321', '54321', '4321', '321']
    # 常用前缀列表
    _prefixList = ['a','qq','yy','aa','abc','qwer','woaini']
    # 常用密码
    _commonPasswd = ['123456', 'a123456', '123456a', '123456abc', 'abc123456', 'woaini1314', 'qq123456', 'woaini520', 'woaini123', 'woaini521', 'qazwsx', '1qaz2wsx', '1q2w3e4r', '1q2w3e4r5t', '1q2w3e', 'qwertyuiop', 'zxcvbnm']
    # 和partner混合的常用前缀列表
    partnerPrefixList = ['520','5201314','1314','iloveu','iloveyou']
    # 和domian，company组合的前缀列表
    domainPrefixList = ['admin','root','manager','system']


    def __init__(self, fullname="", nickname="", englishname="", partnername="", birthday="", phone="", qq="", \
        company="", domain="", oldpasswd="", keywords="", keynumbers=""):
        '''
        Params:
            Parameters of args:
            fullname:    specified the fullname, format: 'zhang san' 'wang ai guo' 0
            nickname:    specified the nickname 0
            englishname: specified the english name 0
            partnername: specified the partner name
            birthday:    specified the birthday day, format: '2000-1-10' 0
            phone:       specified the phone number 0
            qq:          specified the QQ number 0
            company:     specified the company
            domain:      specified the domain name
            oldpasswd:   specified the oldpassword
            keywords:    specified the keywords, example: 'keyword1 keyword2'
            keynumbers:  specified the keynumbers, example: '123 789' 0
        '''
        
        self.fullname = fullname
        self.nickname = nickname
        self.englishname = englishname
        self.partnername = partnername
        self.birthday = birthday
        self.phone = phone
        self.qq = qq
        self.company = company
        self.domain = domain
        self.oldpasswd = oldpasswd
        self.keywords = keywords
        self.keynumbers = keynumbers

        # 常用数字列表，用户和用户名、昵称、英文名、关键字等混合
        self.innerNumList = []
        # 常用前缀列表，用于和手机号、QQ号混合
        self.innerPrefixList = []

        # 段名列表，由原始全名生成
        self.shortNameList = []
        # 全名列表，由原始全名生成
        self.fullNameList = []
        # 待混合的keyword列表，由于用户名、昵称、英文名、关键字的混合规则一致，因此放到这一个列表内进行混合
        self.mixedKeywordList = []

        self.result = []


    def _genShortNameList(self, fullname=None):
        fullname = fullname if fullname else self.fullname
        if not fullname:
            return []
        else:
            result = []
            func = lambda x:[x, x.title(), x[0].lower(), x[0].upper(), x.upper()]
            #print 'func:',func
            nameSplited = fullname.split()
            if len(nameSplited) == 1:
                result += func(nameSplited[0])
            elif len(nameSplited) == 2:
                shortName = nameSplited[0][0].lower() + nameSplited[1][0].lower()
                result += func(shortName)
            else:
                shortName = nameSplited[0][0].lower() + nameSplited[1][0].lower() + nameSplited[2][0].lower()
                result += func(shortName)
                shortNameRS = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0][0].lower()
                shortNameR = nameSplited[1][0].lower() + nameSplited[2][0].lower() + nameSplited[0]
                result += [shortNameR, shortNameRS, shortNameRS.upper()]

            return result


    def _genFullNameList(self, fullname=None):
        fullname = fullname if fullname else self.fullname
        if not fullname:
            return []
        else:
            result = []
            nameSplited = fullname.split()
            if len(nameSplited) == 1:
                result.append(nameSplited[0])
            elif len(nameSplited) == 2:
                result += ["".join(nameSplited), nameSplited[1]+nameSplited[0]]
            else:
                result += [nameSplited[0]+nameSplited[1]+nameSplited[2], nameSplited[1]+nameSplited[2]+nameSplited[0]]
            
            return result + [x.upper() for x in result]


    def _genInnerNumList(self):
        result = self._numList
        for i in range(0,10):
            result += [str(i)*x for x in range(1,10)]

        endyear = int(time.strftime("%Y"))
        result += [str(x) for x in range(2000, endyear+1)]

        if self.keynumbers:
            result += self.keynumbers.split()
        if self.oldpasswd:
            result.append(self.oldpasswd)

        return result


    def _genDateList(self, date):
        if not date:
            return []
        else:
            result = []
            dateSplited = date.split("-")
            if len(dateSplited) == 1:
                result.append(dateSplited[0])
            elif len(dateSplited) == 2:
                result += [dateSplited[0], dateSplited[0]+dateSplited[1], dateSplited[0][-2:]+dateSplited[1]]
            else:
                result += [dateSplited[0], dateSplited[0]+dateSplited[1], dateSplited[0]+dateSplited[1]+dateSplited[2]]
                result += [dateSplited[0][-2:]+dateSplited[1], dateSplited[0][-2:]+dateSplited[1]+dateSplited[2]]

            return result

    def _mixed(self, listA, listB):
        if not listA and not listB:
            return []
        result = []
        # print 'listA:',listA
        # print 'listB',listB
        for a,b in itertools.product(listA, listB):
            #print a,b
            if len(a+b)>5 and len(a+b)<17:
                result.append(a+b)
                result.append(a+"@"+b)

        return result


    def _preHandlePhase(self):
        self.innerNumList = self._genInnerNumList()
        self.innerPrefixList = self._prefixList + [x.upper() for x in self._prefixList]
        self.shortNameList = self._genShortNameList()
        self.fullNameList = self._genFullNameList()

        self.mixedKeywordList += self.shortNameList
        self.mixedKeywordList += self.fullNameList
        if self.nickname:
            self.mixedKeywordList.append(self.nickname)
        if self.englishname:
            self.mixedKeywordList.append(self.englishname)
        if self.keywords:
            self.mixedKeywordList += self.keywords.split()


    def _mixedPhase(self):
        self.result += self._mixed(self.mixedKeywordList, self.innerNumList)
        self.result += self._mixed(["520"], self.mixedKeywordList)
        if self.phone:
            self.result += self._mixed(self.innerPrefixList+self.mixedKeywordList, [self.phone])
        if self.qq:
            self.result += self._mixed(self.innerPrefixList+self.mixedKeywordList, [self.qq])
        if self.partnername:
            nameList = self._genShortNameList(self.partnername)
            nameList += self._genFullNameList(self.partnername)
            self.result += self._mixed(self.partnerPrefixList, nameList)
        if self.birthday:
            dateList = self._genDateList(self.birthday)
            self.result += self._mixed(self.innerPrefixList+self.mixedKeywordList, dateList)
        if self.domain:
            self.result += self._mixed(self.domainPrefixList, [self.domain])
        if self.company:
            self.result += self._mixed(self.domainPrefixList, [self.company])


    def _lastHandlePhase(self):
        self.result += self._commonPasswd
        self.result += [x+"." for x in self.result]


    def generate(self):
        self._preHandlePhase()
        self._mixedPhase()
        self._lastHandlePhase()

        return self.result


if __name__ == '__main__':
    pwgen = PasswdGenerator(nickname='lj',qq='85997632015lj')
    wordlist = pwgen.generate()
    print wordlist




'''
首字母大写
常用前缀@#$%
常用后缀123, 123456 111 
'''