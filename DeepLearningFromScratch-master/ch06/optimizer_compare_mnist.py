# coding: utf-8
import os
import sys
sys.path.append(os.pardir)  # 为了导入父目录的文件而进行的设定
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist  # 导入MNIST数据集模块
from common.util import smooth_curve  # 导入平滑曲线的工具函数
from common.multi_layer_net import MultiLayerNet  # 导入多层神经网络类
from common.optimizer import *  # 导入所有优化器类


# 0:读入MNIST数据集
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)  # 加载数据集并归一化
train_size = x_train.shape[0]  # 获取训练数据集中样本数
batch_size = 128  # 设置小批量数据大小
max_iterations = 3000  # 设置最大迭代次数


# 1:进行实验的设置
optimizers = {}  # 创建一个字典用于存储不同优化器实例
optimizers['SGD'] = SGD()  # 存储随机梯度下降优化器实例
optimizers['Momentum'] = Momentum()  # 存储带有动量的随机梯度下降优化器实例
optimizers['AdaGrad'] = AdaGrad()  # 存储AdaGrad优化器实例
optimizers['Adam'] = Adam()  # 存储Adam优化器实例
#optimizers['RMSprop'] = RMSprop()  # 可选的RMSprop优化器实例

networks = {}  # 创建一个字典用于存储不同神经网络实例
train_loss = {}  # 创建一个字典用于存储不同优化器对应的训练损失
for key in optimizers.keys():  # 遍历所有优化器键值
    networks[key] = MultiLayerNet(
        input_size=784, hidden_size_list=[100, 100, 100, 100],  # 初始化输入、隐藏层、输出层大小
        output_size=10)  # 初始化神经网络实例并存入字典
    train_loss[key] = []  # 将训练损失列表初始化为空


# 2:开始训练
for i in range(max_iterations):  # 进行迭代训练
    batch_mask = np.random.choice(train_size, batch_size)  # 从训练数据集中选择小批量样本
    x_batch = x_train[batch_mask]  # 获取输入特征
    t_batch = t_train[batch_mask]  # 获取真实标签

    for key in optimizers.keys():  # 对于每一种优化器
        grads = networks[key].gradient(x_batch, t_batch)  # 计算梯度
        optimizers[key].update(networks[key].params, grads)  # 更新网络参数

        loss = networks[key].loss(x_batch, t_batch)  # 计算损失值
        train_loss[key].append(loss)  # 将损失值添加到训练损失列表中

    if i % 100 == 0:  # 每100次迭代打印一次损失
        print("===========" + "iteration:" + str(i) + "===========")  # 打印当前迭代次数
        for key in optimizers.keys():  # 遍历所有优化器键值
            loss = networks[key].loss(x_batch, t_batch)  # 计算损失值
            print(key + ":" + str(loss))  # 打印每种优化器的损失值


# 3.绘制图形
markers = {"SGD": "o", "Momentum": "x", "AdaGrad": "s", "Adam": "D"}  # 定义各种标记
x = np.arange(max_iterations)  # 创建一个等差数组，作为横坐标
for key in optimizers.keys():  # 遍历所有优化器键值
    plt.plot(x, smooth_curve(train_loss[key]), marker=markers[key], markevery=100, label=key)  # 绘制训练损失曲线
plt.xlabel("iterations")  # 设置x轴标签
plt.ylabel("loss")  # 设置y轴标签
plt.ylim(0, 1)  # 设置y轴显示范围在0到1之间
plt.legend()  # 显示图例
plt.show()  # 显示图像
