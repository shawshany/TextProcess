#!/usr/bin/python3
# -*-coding:utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

#Reference:**********************************************
# @Time     : 2019-09-30 12:34
# @Author   : 病虎
# @E-mail   : victor.xsyang@gmail.com
# @File     : TextProcess.py
# @User     : ora
# @Software: PyCharm
# @Description: 
#Reference:**********************************************
from TextProcess.langconv import *
import re
from TextProcess import emoji



"""
### 基础正则过滤
1. emotion表情：u'\[[:a-zA-Z\u4e00-\u9fa5]{1,10}\]' 现推荐：emoji.demojize()方法
2. 过滤超链接tag，href
3. 过滤http地址
4. 把长数字都换成一个特殊字符NUM
5. 过滤括号：【xxxxx】/（xxxxxxx）/ [xxxx] 【.*】|（.*）|\[.*\]
6. 过滤非中文字符，连续标点和空格
7. 过滤连续空格

text_regex_preprocessing(text, "OnlinePipe")
"""
class TextProcess():
    def evaluate(self, rawContent, pattern):
        """

        :param rawContent: 待处理的文本
        :param pattern: 正则匹配的模式
        """
        if None in (rawContent, pattern):
            return None
        text = rawContent
        switcher = {
            "Emotion": self.replace_emotion,
            "TagHref": self.remove_ahref,
            "Http": self.remove_http,
            "LongNumber": self.replace_long_num,
            "Brackets": self.replace_brackets,
            "NoChinese": self.remove_not_che,
            "ExtraSpace": self.clean_extra_spaces,
            "ControlCharacter": self.replace_control_character,
            "ChiEngNum": self.keep_chi_eng_num,
            "ChiEng": self.keep_chi_eng,
            "Chi": self.remove_not_che,
            "OnlinePipe": self.preprocessing_all_online,
            "OnlinePipeStrictMore": self.preprocessing_all_online_strict_more,
            "OnlinePipeStrictMost": self.preprocessing_all_online_strict_most,
            "HotlinePipe": self.preprocessing_all_hotline,
        }
        func = switcher.get(pattern, lambda: "nothing")
        return self.clean_extra_spaces(func(text))

    def Tra2Sim(self, text, flag):
        """
        繁体简体互换
        :param text:原始文本
        :param flag:'zh-hant':简体到繁体 ; 'zh-hans':繁体到简体
        """
        # 转换繁体到简体
        if flag=='zh-hans':
            return Converter('zh-hans').convert(text)
        # 转换简体到繁体
        if flag == 'zh-hant':
            return Converter('zh-hant').convert(text)

    def strLower(self, eng_text):
        '''
        英文大写转小写
        :param engtext:
        :return:
        '''
        return eng_text.lower()

    def strQ2B(self, ustring):
        '''
        全角转半角
        :param ustring:
        :return:
        '''
        ss = ""
        for s in ustring:
            rstring = ""
            for uchar in s:
                inside_code = ord(uchar)
                if inside_code == 12288:  # 全角空格直接转换
                    inside_code = 32
                elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                    inside_code -= 65248
                rstring += chr(inside_code)
            ss += rstring
        return ss

    def preprocessing_all_online(self, text):
        t1 = self.strLower(text)
        t1 = self.Tra2Sim(t1, 'zh-hans')
        t1 = self.strQ2B(t1)
        t1 = self.replace_emotion(t1, "")
        t2 = self.remove_ahref(t1, "")
        t3 = self.remove_http(t2, "")
        t4 = self.replace_long_num(t3, "LONG_NUM")
        t5 = self.replace_brackets(t4, "")
        t6 = self.keep_chi_eng_num(t5, "")
        t7 = self.replace_control_character(t6, "")
        return t7

    def preprocessing_all_online_strict_most(self, text):
        t1 = self.strLower(text)
        t1 = self.Tra2Sim(t1, 'zh-hans')
        t1 = self.strQ2B(t1)
        t1 = self.replace_emotion(t1, "")
        t2 = self.remove_ahref(t1, "")
        t3 = self.remove_http(t2, "")
        t4 = self.replace_long_num(t3, "")
        t5 = self.replace_brackets(t4, "")
        t6 = self.remove_not_che(t5)
        t7 = self.replace_control_character(t6, "")
        return t7

    def preprocessing_all_online_strict_more(self, text):
        t1 = self.strLower(text)
        t1 = self.Tra2Sim(t1, 'zh-hans')
        t1 = self.strQ2B(t1)
        t1 = self.replace_emotion(t1, "")
        t2 = self.remove_ahref(t1, "")
        t3 = self.remove_http(t2, "")
        t4 = self.replace_long_num(t3, "")
        t5 = self.replace_brackets(t4, "")
        t6 = self.keep_chi_eng(t5, "")
        t7 = self.replace_control_character(t6, "")
        return t7


    def preprocessing_all_hotline(self, text):
        t1 = self.replace_emotion(text, " ")
        t2 = self.remove_ahref(t1, " ")
        t3 = self.remove_http(t2, " ")
        t4 = self.replace_long_num(t3, " ")
        t5 = self.replace_brackets(t4, " ")
        t6 = self.remove_not_che(t5)
        return t6

    def replace_control_character(self, text, sub_str=""):
        """
        去除控制字符
        :param text: 待处理的文本
        :param sub_str: 用于替换的子串
        """
        re_str = u'[\t\r\n\v\f]'
        return self.replace_pattern(re_str, sub_str, text)

    def keep_chi_eng_num(self, text, sub_str=""):
        """
        保留中文、英文及数字
        :param text:
        :param sub_str:
        """
        res_str = u'[^a-zA-Z0-9\u4e00-\u9fa5]'
        return self.replace_pattern(res_str, sub_str, text)

    def keep_chi_eng(self, text, sub_str=""):
        """
        保留中文、英文
        :param text:
        :param sub_str:
        """
        res_str = u'[^a-zA-Z\u4e00-\u9fa5]'
        return self.replace_pattern(res_str, sub_str, text)

    def filter_emoji(self, desstr, restr=''):
        # 过滤表情
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

    def replace_emotion(self, text, sub_str=""):
        # re_str = '[\U00010000-\U0010ffff]'

        # re_str = u'\[[:a-zA-Z\u4e00-\u9fa5]{1,10}\]'
        return self.filter_emoji(text, sub_str)

    def convert_emotion(self, text):
        return emoji.demojize(text)

    def remove_ahref(self, text, sub_str=""):
        re_str = u'<[^>]*>'
        return self.replace_pattern(re_str, sub_str, text)

    def remove_http(self, text, sub_str=""):
        re_str = u'https?://[a-zA-Z0-9\.\?/&\=\:\;\-\_]*'
        return self.replace_pattern(re_str, sub_str, text)

    def replace_long_num(self, text, sub_str=""):
        re_str = u'\d{5,}'
        return self.replace_pattern(re_str, sub_str, text)

    def replace_brackets(self, text, sub_str=""):
        re_str = u'【.*】|（.*）|\[.*\]|「.*」|{.*}'
        return self.replace_pattern(re_str, sub_str, text)

    def remove_not_che(self, text):
        text = self.replace_pattern(u'[^\u4e00-\u9fa5 ]', "", text)
        return text

    def remove_not_che_and_comma(self, text):
        text = self.replace_pattern(u'[^\u4e00-\u9fa5，。？！ ]', " ", text)
        text = self.replace_pattern(u'。{2,}|，{2,}|^，|^。|^？|^！', "", text.strip())
        return text

    def remove_commas(self, text):
        text = self.replace_pattern(u'。{2,}|，{2,}|,{2,}|？{2,}|！{2,}| {2,}', "", text.strip())
        return text

    def clean_extra_spaces(self, text):
        text = self.replace_pattern(u' {2,}', "", text.strip())
        return text

    def replace_pattern(self, re_str, sub_str, text):
        regex_pattern = re.compile(re_str)
        return regex_pattern.sub(sub_str, text)
