
#classify the data using libSVM
http://www.cnblogs.com/Finley/p/5329417.html


dataformat :

#[label]   [Index1]:[value1]  [index2]:[value2]  [index3]:[value3]
# [label]:类别（通常是整数）[index n]: 有顺序的索引 [value n]

the dataset stored in "data" directory
svm_train的参数：

-s SVM的类型(svm_type)

    0 -- C-SVC(默认)

    使用惩罚因子(Cost)的处理噪声的多分类器

    1 -- nu-SVC(多分类器)

    按照错误样本比例处理噪声的多分类器

    2 -- one-class SVM

    一类支持向量机，可参见"SVDD"的相关内容

    3 -- epsilon-SVR(回归)

    epsilon支持向量回归

    4 -- nu-SVR(回归)

-t 核函数类型(kernel_type)

    0 -- linear(线性核):

    u'*v

    1 -- polynomial(多项式核):

    (gamma*u'*v + coef0)^degree

    2 -- radial basis function(RBF,径向基核/高斯核):

    exp(-gamma*|u-v|^2)

    3 -- sigmoid(S型核):

    tanh(gamma*u'*v + coef0)

    4 -- precomputed kernel(预计算核)：

核矩阵存储在training_set_file中

        下面是调整SVM或核函数中参数的选项：

        -d 调整核函数的degree参数，默认为3

        -g 调整核函数的gamma参数，默认为1/num_features

        -r 调整核函数的coef0参数，默认为0

        -c 调整C-SVC, epsilon-SVR 和 nu-SVR中的Cost参数，默认为1

        -n 调整nu-SVC, one-class SVM 和 nu-SVR中的错误率nu参数，默认为0.5

        -p 调整epsilon-SVR的loss function中的epsilon参数，默认0.1

        -m 调整内缓冲区大小,以MB为单位，默认100

        -e 调整终止判据，默认0.001

        -wi调整C-SVC中第i个特征的Cost参数

调整算法功能的选项：

-b 是否估算正确概率,取值0 - 1，默认为0

-h 是否使用收缩启发式算法(shrinking heuristics),取值0 - 1，默认为0

-v 交叉校验

-q 静默模式

run the codes:

    python new.py