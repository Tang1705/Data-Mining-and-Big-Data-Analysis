import random
import numpy as np

class Association_rules:
    def __init__(self,minSupport=0.2,minConfidence=0.5):
        '''
        minSuport:最小支持度
        minConfidence:最小置信度
        dataset:数据集
        count:存放frequent itemsets 以及 support
        associationRules:满足minConfidence的关联规则
        num:元素数量
        threshold = num*minSupport：由num和minSupport算出的阈值
        '''
        self.minSupport = minSupport
        self.minConfidence = minConfidence
        self.dataset = None
        self.count = None
        self.associationRules = None
        self.num = 0
        self.threshold = 0
 
    #计算frequent itemset
    def countItem(self,upDict,elength):
        currentDict = {}
        element = list(upDict.keys())
        for i in range(len(element)-1):
            for j in range(i+1,len(element)):
                tmp = set(list(element[i]))
                tmp.update(list(element[j]))
                if len(tmp) > elength:
                    continue
                if tmp in list(set(item) for item in currentDict.keys()):
                    continue
                for item in self.dataset:
                    if tmp.issubset(set(item)):
                        if tmp in list(set(item) for item in currentDict.keys()):
                            currentDict[tuple(tmp)] += 1
                        else:
                            currentDict[tuple(tmp)] = 1
        for item in list(currentDict.keys()):
            if currentDict[item] < self.threshold:
                del currentDict[item]
        if len(list(currentDict.keys())) < 1:
            return None
        else:
            return currentDict
 
    #生成frequent itemsets
    def fit(self,dataset):
        self.dataset = dataset
        count = []
        count.append({})
        for item in self.dataset:
            for i in range(len(item)):
                if item[i] in list(count[0].keys()):
                    count[0][item[i]] += 1
                else:
                    count[0][item[i]] = 1
                    self.num += 1
 
        self.threshold = self.num * self.minSupport
 
        for item in list(count[0].keys()):
            if count[0][item] < self.threshold:
                del count[0][item]
                
        i = 0
        while(True):
            if len(count[i]) < 2:
                break
            else:
                tmp = self.countItem(count[i],i+2)
                if tmp == None:
                    break
                else:
                    count.append(tmp)
                i += 1
 
        self.count = count
 
    #打印并返回frequent itemsets
    def frequentItemsets(self):
        #print('threshold:',self.threshold)
        for item in self.count:
            print(item)
            print()
        return self.count
 
    #二进制法求每个itemset的所有子集
    def subsets(self,itemset):
        N = len(itemset)
        subsets = []
        for i in range(1,2**N-1):
            tmp = []
            for j in range(N):
                if (i >> j) % 2 == 1:
                    tmp.append(itemset[j])
            subsets.append(tmp)
        return subsets
 
    #计算置信度。set = (X),set2 = (X^Y)
    def countConfidence(self,set1,set2):
        len1 = len(set1)
        len2 = len(set2)
        #去除元素位置干扰。例如：set2 = ('a','b'),而self.count中存储为('b','a')
        if not tuple(set2) in self.count[len2-1].keys():
            set2[0],set[1] = set2[1],set2[0]
        #写代码的时候出现的疏忽，当元素只有一个时count中存储格式是str，而元素多于一个时格式是tuple
        if len1 == 1:
            return self.count[len2-1][tuple(set2)] / self.count[len1-1][set1[0]]
        else:
            if not tuple(set1) in self.count[len1-1].keys():
                set1[0],set1[1] = set1[1],set1[0]
            return self.count[len2-1][tuple(set2)] / self.count[len1-1][tuple(set1)] 
 
    def associationRule(self):
        associationRules = []
        for i in range(1,len(self.count)):
            for itemset in list(self.count[i].keys()):
                #用字典存每个itemset的关联规则
                tmp = {}
                #print(itemset)
                subset = self.subsets(itemset)
                #print(subset)
                for i in range(len(subset)-1):
                    for j in range(i+1,len(subset)):
                        #判断subset[i]与subset[j]完整组成一个itemset，而且没有相同的元素
                        if len(subset[i]) + len(subset[j]) == len(itemset) and len(set(subset[i]) & set(subset[j])) == 0:
                            confidence = self.countConfidence(subset[i],itemset)
                            #print(subset[i],' > ',subset[j],' ',confidence)
                            if confidence > self.minConfidence:
                                #生成相应键值对
                                tmpstr = str(subset[i]) + ' > ' + str(subset[j])
                                tmp[tmpstr] = confidence
                            #将subset[i]与subset[j]反过来生成另外一个规则
                            confidence = self.countConfidence(subset[j],itemset)
                            #print(subset[j],' > ',subset[i],' ',confidence)
                            if confidence > self.minConfidence:
                                tmpstr = str(subset[j]) + ' > ' + str(subset[i])
                                tmp[tmpstr] = confidence
                if tmp.keys():
                    associationRules.append(tmp)
        for item in associationRules:
            print(item)
        return associationRules


def set_data(num):
    dataset = []
    for i in range(num):
        number = random.randint(1,5)
        dataset.append(list(set(chr(ord('a')+random.randint(1,10)) for i in range(number))))
    return dataset

if __name__ == '__main__':
    num = 10
    dataset = set_data(num)
    for item in dataset:
        print(item)
    ar = Association_rules()
    ar.fit(dataset)
    freItemsets = ar.frequentItemsets()
    associationRules = ar.associationRule()
