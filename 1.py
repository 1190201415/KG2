# -*-coding = utf-8 -*-
# @Time : 2024/3/23 14:53
# @Author :skq
# @File : 1.py.py
# @Software: PyCharm
import xml.etree.ElementTree as ET
class attachment(object):
    def __init__(self, K=False, T=False, Z=False, E=False, Q=False, P=False):
        self.T = T
        self.Z = Z
        self.Q = Q
        self.K = K
        self.E = E
        self.P = P

    def tostring(self):
        str1= ''
        attri = vars(self)
        for a, v in attri.items():
            print(type(a))
            if v:
                str1 = str1+'1'
            else:
                str1 = str1 + '0'
            print(v)
        return str1
a = attachment()
a.tostring()