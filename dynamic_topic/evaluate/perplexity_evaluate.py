# -*- coding: UTF-8-*-
import numpy
import math
import string
import matplotlib.pyplot as plt
import re


# perplexity=exp^{ - (∑log(p(w))) / (N) }

# 其中，P(W)是指的测试集中出现的每一个词的概率，具体到LDA的模型中就是P(w)=∑z p(z|d)*p(w|z)
# 【z,d分别指训练过的主题和测试集的各篇文档】。
# 分母的N是测试集中出现的所有词，或者说是测试集的总长度，不排重。

# 因而python程序代码块需要包括几个方面：

# 1.对训练的模型，将Topic-word分布文档转换成字典，方便查询概率，即计算perplexity的分子
# 2.统计测试集长度，即计算perplexity的分母
# 3.计算困惑度
# 4.对于不同的Topic数量的模型，计算的困惑度，画折线图。
#

# 对模型训练出来的词转换成一个词为KEY,概率为值的字典。
def dictionary_found(wordlist):
    result_word_dictionary = {}
    for i in xrange(2, len(wordlist), 3):
        if i > 0:
            if result_word_dictionary.has_key(wordlist[i]) == True:
                word_probability = result_word_dictionary.get(wordlist[i])
                word_probability = float(word_probability) + float(wordlist[i - 2])
                result_word_dictionary.update({wordlist[i]: word_probability})
            else:
                result_word_dictionary.update({wordlist[i]: wordlist[i - 2]})

    return result_word_dictionary


# 对于测试集的每一个词，在字典中查找其概率。
def look_into_dic(dictionary, testset):
    '''Calculates the TF-list for perplexity'''
    frequency = []
    letter_list = []
    a = 0.0
    for letter in testset.split():
        if letter not in letter_list:
            letter_list.append(letter)
            letter_frequency = (dictionary.get(letter))
            frequency.append(letter_frequency)
        else:
            pass
    for each in frequency:
        if each != None:
            a += float(each)
        else:
            pass
    return a


# 测试集的词数统计
def f_testset_word_count(testset):
    '''reture the sum of words in testset which is the denominator of the formula of Perplexity'''
    testset_clean = testset.split()
    # return (len(testset_clean) - testset.count("\n"))
    return (len(testset_clean))


def f_perplexity(word_frequency, word_count):  # 计算困惑度
    '''Search the probability of each word in dictionary
    Calculates the perplexity of the LDA model for every parameter T'''
    duishu = math.log(word_frequency)
    kuohaoli = duishu / (word_count * 5)
    print kuohaoli
    perplexity = math.exp(-kuohaoli)
    return perplexity


# 做主题数与困惑度的折线图
def graph_draw(topic, perplexity):
    x = topic
    y = perplexity
    print "----------------"
    print x
    print y
    plt.plot(x, y, color="red", linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()


def perplexity_main(all_word_path, model_topic_path, k):
    topic = []
    perplexity_list = []
    testset, testset_word_count = get_word_count_N(all_word_path)
    for i in xrange(len(k)):
        topic.append(k[i])
        # 分别计算k=5,10,15的困惑度
        trace = model_topic_path + str(k[i]) + ".txt"
        f = open(trace, 'r')
        text = f.readlines()
        word_list = []
        for line in text:
            if "topic" not in line.lower():
                line_clean = line.split()
                word_list.extend(line_clean)
            else:
                pass
        word_dictionary = dictionary_found(word_list)
        frequency = look_into_dic(word_dictionary, testset)
        perplexity = f_perplexity(frequency, testset_word_count)
        print perplexity
        perplexity_list.append(perplexity)
    print topic
    print perplexity_list
    graph_draw(topic, perplexity_list)


# 統計總數N
def get_word_count_N(all_word_path):
    f1 = open(all_word_path, 'r')
    testset = f1.read()
    testset_word_count = f_testset_word_count(testset)  # call the function to count the sum-words in testset
    return testset, testset_word_count


if __name__ == "__main__":
    """
    all_word_path: all word lists
    model_topic_path:topic word1 0.2636 word2 0.369
    """
    all_word_path = "E://vocab.nips.txt"
    model_topic_path = "E://out.itr100topics"
    k = [128, 256]
    perplexity_main(all_word_path, model_topic_path, k)
