# -*- coding:utf-8 -*-
# 词干化、去停用词处理

import os
import re

# 修改了第一行与第二行的保存的地方
localpath_EditionDate = '/home/baiqingchun/00_data/20_output_data_finish'
# 分词后的localpath_EditionDate
wordseg_localpath_EditionDate = '/home/baiqingchun/00_data/data_done'


# dirpath
def WriteToLocal(dirpath):
    files = os.listdir(dirpath)
    for folderName in files:  ##第一层文件夹tain
        rootpath = os.path.join(dirpath, folderName)
        secondFolders = os.listdir(rootpath)
        save_path = wordseg_localpath_EditionDate + '/' + folderName + '.txt'
        file_write = open(save_path, 'w')
        for secondFolder in secondFolders:
            fullpath = os.path.join(rootpath, secondFolder)
            print fullpath
            str_content = ReadTextFile(fullpath)  # 拼接数据
            file_write.write(str_content + "\n")
        file_write.close()


def ReadTextFile(path):
    file = open(path)
    content = file.read().strip()
    strinfo = re.compile(r"\\")
    content = strinfo.sub('', content)

    strinfo = re.compile('  ')
    content = strinfo.sub(' ', content)
    file.close()
    return content


if __name__ == '__main__':
    WriteToLocal(localpath_EditionDate)
