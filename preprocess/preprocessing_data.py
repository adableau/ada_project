# -*- coding:utf-8 -*-
# 词干化、去停用词处理

import os
import re
from string import maketrans
from string import punctuation
from string import digits
from __builtin__ import file

# 修改了第一行与第二行的保存的地方
localpath_EditionDate = '/home/baiqingchun/00_data/20_output_data'
# 分词后的localpath_EditionDate
wordseg_localpath_EditionDate = '/home/baiqingchun/00_data/20_output_data_finish'

deleteList = ['SECTION:', 'LENGTH:', 'Final Edition:', 'To the Editor:', 'BYLINE:', 'Late Edition', 'SOURCE:']


# dirpath
def WriteToLocal(dirpath):
    files = os.listdir(dirpath)
    for folderName in files:  ##第一层文件夹tain
        rootpath = os.path.join(dirpath, folderName)
        secondFolders = os.listdir(rootpath)
        for secondFolder in secondFolders:
            fullpath = os.path.join(rootpath, secondFolder)
            txtFiles = os.listdir(fullpath)
            # 合并第二个文件夹下所有,第二层作为文件名
            save_path = wordseg_localpath_EditionDate + '/' + folderName
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            save_path = save_path + '/' + secondFolder + '.txt'
            file_write = open(save_path, 'w')
            # 每一个文件为一行
            print "-------------------------"
            print save_path
            for txtName in txtFiles:  # 第二个文件夹
                fullpaths = os.path.join(fullpath, txtName)
                print fullpaths
                str = ReadTextFile(secondFolder, fullpaths)  # 对文本分句、分词

                file_write.write(str + "\n")
            file_write.close()


def ReadTextFile(secondFolder, path):
    file = open(path)
    content = file.read().strip()
    content = secondFolder + "," + content
    content = content.replace("\n", "").replace("\r", "").strip()
    strinfo = re.compile(r"\\")
    content = strinfo.sub('', content)

    strinfo = re.compile('  ')
    content = strinfo.sub(' ', content)
    file.close()
    return content


if __name__ == '__main__':
    WriteToLocal(localpath_EditionDate)
