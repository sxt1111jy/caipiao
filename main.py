import numpy as np
import random
import sklearn
import sys

class CaiPiao():
    def __init__(self, red_ball_num):
        '''
        :param red_ball_num: 红球数量，双色球6，大乐透5
        '''
        self.red_ball_num = red_ball_num
        if self.red_ball_num == 6:
            self.blue_ball_num = 1
            self.red_ball_max = 33
            self.blue_ball_max = 16
        elif self.red_ball_num == 5:
            self.blue_ball_num = 2
            self.red_ball_max = 35
            self.blue_ball_max = 12
        else:
            sys.exit("输入数据有误， red数量只能是5或者6")

    def getBallDataByRandom(self, ball_num, group_num):
        '''
        根据random.randint函数产生随机数据
        :param ball_num: 取值为self.red_ball_num或者self.blue_ball_num
        :param group_num: 组数（注数），要获取多少注给定颜色的小球数据
        :return: 一定注数的小球数据
        '''
        ball_list= []
        if ball_num == self.red_ball_num:
            ball_data = range(1, self.red_ball_max + 1, 1)
        elif ball_num == self.blue_ball_num:
            ball_data = range(1, self.red_ball_max + 1, 1)
        else:
            sys.exit("输入有误， ball_num定义域：{1, 2, 5, 6}")
        for i in range(group_num):
            ball_list.append(sorted(np.random.choice(ball_data, ball_num, replace = False)))
        return ball_list

    def getOneBallDataByPolynomialAlgorithm(self, ball_index, gropu_num):
        '''
        使用多项式算法预测小球数据
        :param ball_index: 无论双色球还是大乐透，一注7个小球数据，
        :param gropu_num: 组数（注数），要获取多少注给定颜色的小球数据
        :return: 一定注数的某个小球数据
        '''
        pass

if __name__ == "__main__":
    shuangseqiu = CaiPiao(6)
    # for i in range(6):
    #     print(shuangseqiu.getBallDataByRandom(6, 5))
