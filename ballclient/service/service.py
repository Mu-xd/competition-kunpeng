# encoding:utf8
'''
业务方法模块，需要选手实现

选手也可以另外创造模块，在本模块定义的方法中填入调用逻辑。这由选手决定

所有方法的参数均已经被解析成json，直接使用即可

所有方法的返回值为dict对象。客户端会在dict前面增加字符个数。

1、防守时按照方向和距离远离进攻方
2、防守时候能左右走就不上下走
3、远离传送阵的出口

'''
import ballclient.service.constants as constants
import random
#防守模式
def Defense(map, player):
    x = int(player['x'])
    y = int(player['y'])
    d_x = []
    d_y = []
    r_x = 0
    r_y = 0
    d = []
    res = ""
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    for i in range(height):                                                  #读取基础地图
        for j in range(width):
            if map[i][j][0] == '-':
                d_y.append(i)
                d_x.append(j)
    if(len(d_x) == 0): #如果视野内没有敌人 看看附近有没有分数
        return Attack(map, player,[])
    d = []
    #计算与敌人的距离
    for i in range(len(d_x)):
        d.append(pow((pow((d_x[i] - x), 2)) + pow(d_y[i] - y, 2), 0.5))
    for i in range(len(d)):
        if d[i] == 1:
            r_x += (d_x[i] - x) * 0.9
            r_y += (d_y[i] - y) * 0.9
        elif 2 > d[i] > 1:
            r_x += (d_x[i] - x) * 0.09
            r_y += (d_y[i] - y) * 0.09
        elif d[i] == 2:
            r_x += (d_x[i] - x) * 0.009
            r_y += (d_y[i] - y) * 0.009
        elif 3 > d[i] > 2:
            r_x += (d_x[i] - x) * 0.0009
            r_y += (d_y[i] - y) * 0.0009
        elif d[i] == 3:
            r_x += (d_x[i] - x) * 0.00009
            r_y += (d_y[i] - y) * 0.00009
        elif 4 > d[i] > 3:
            r_x += (d_x[i] - x) * 0.00001
            r_y += (d_y[i] - y) * 0.00001
    if r_x == 0 and r_y == 0:       #离得很远#或者两个方向的相同抵消了
        if x > 0 and map[y][x - 1][0] != '-':#认为在左右两侧
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                return 'up'
            else:
                return 'down'
        elif x < (width -1) and map[y][x + 1][0] != '-':
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V' :
                return 'up'
            else:
                return 'down'
        elif y > 0 and map[y - 1][x][0] != '-':#认为在上下两侧
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-'and map[y][x - 1] != '>':
                return 'left'
            else:
                return 'right'
        elif y < height -1 and map[y + 1][x][0] != '-':#认为在上下两侧
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                return 'left'
            else:
                return 'right'
        return Attack(map, player)
    elif r_x == 0 and r_y > 0:#这个敌人在下面
        if y > 1 and map[y - 2][x][0] != '-':
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and  map[y - 1][x] != 'V':
                res = 'up'
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0  and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'down'
        else:#在下面稍远的位置或者上面稍远的位置有一个对其影响了
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0  and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'up'
    elif r_x == 0 and r_y < 0:#这个敌人在上面
        if y < height - 2 and map[y + 2][x][0] != '-':
            if y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0  and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'up'
        else:
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0  and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'down'
    elif r_x > 0 and r_y == 0:#这个敌人在右面
        if x > 1 and map[y][x - 2][0] != '-':
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'right'
        else:
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'left'
    elif r_x < 0 and r_y == 0:#这个敌人在左面
        if x < width - 2 and map[y][x + 2][0] != '-':
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'left'
        else:
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'right'
    else:
        O = r_y / r_x
        if (O > 1 or O < -1) and r_y > 0:        #方向向下
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = "up"
            else:
                if O > 0:
                    if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    else:
                        res = 'down'
                else:
                    if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    else:
                        res = 'down'
        elif (O > 1 or O < -1) and r_y < 0:      #方向向上
            if y < height - 1 and map[y + 1][x] != 'x'and map[y + 1][x][0] != '-'and map[y + 1][x] != '^':
                res = "down"
            else:
                if O < 0:
                    if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    else:
                        res = 'up'
                else:
                    if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    else:
                        res = 'up'
        elif -1 < O < 1 and r_x > 0:            #方向向右
            if x > 0 and x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = "left"
            else:
                if O > 0:
                    if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    elif y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    else:
                        res = 'right'
                else:
                    if y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    else:
                        res = 'right'
        elif -1 < O < 1 and r_x < 0:            #方向向左
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = "right"
            else:
                if O > 0:
                    if y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    else:
                        res = 'left'
                else:
                    if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    elif y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    else:
                        res = 'left'
        elif O == -1 and r_x > 0:               #判断两个方向走都可以的情况 右下
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':#左侧没有石头并且油路
                res = "left"
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':  # 上侧没有石头并且有路
                res = "up"
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = "right"
            else:
                res = "down"
        elif O == 1 and r_x < 0 :               #判断两个方向走都可以的情况 左上
            if x < width -1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':#右侧没有石头并且油路
                res = "right"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x]!= '^':    #下侧没有石头并且有路
                res = "down"
            elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':  # 左侧没有石头并且油路
                res = "left"
            else:
                res = "up"
        elif O == -1 and r_x < 0:               #判断两个方向走都可以的情况 左下
            if x < width -1 and map[y][x +1] != 'x' and map[y][x +1][0] != '-' and map[y][x +1] != '<':#右侧没有石头并且油路
                res = "right"
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':    #上侧没有石头并且有路
                res = "up"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x]!= '^':    #下侧没有石头并且有路
                res = "down"
            else:
                res = "left"
        elif O == 1 and r_x < 0:               #判断两个方向走都可以的情况 右上
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':#左侧没有石头并且油路
                res = "left"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':  # 下侧没有石头并且有路
                res = "down"
            else:
                res = "up"
    return res
#进攻模式
def Attack(map, player,zj):
    x = int(player['x'])
    y = int(player['y'])
    d_x = []
    d_y = []
    r_x = 0
    r_y = 0
    s = []
    d = []
    res = ""
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    for i in range(height):  # 读取基础地图
        for j in range(width):
            try:
                if map[i][j][0] == '-' or map[i][j][0] == 'p':#有敌人和分
                    s.append(int(map[i][j][1:]))
                    d_y.append(i)
                    d_x.append(j)
            except ValueError:
                continue
    if(len(d_x) == 0): #敌人和分数都没有
        if x < 2:
            if map[y][x + 1] != 'x' and map[y][x + 1] != '<' and (str(x + 1) + '_' + str(y)) not in zj:
                return "right"
        if x > width - 3:
            if map[y][x -1] != 'x' and map[y][x -1] != '>'and (str(x - 1) + '_' + str(y)) not in zj:
                return "left"
        if y < 2:
            if map[y + 1][x] != 'x' and map[y + 1][x] != '^' and (str(x) + '_' + str(y + 1)) not in zj:
                return "down"
        if y > height - 3:
            if map[y - 1][x] != 'x' and map[y - 1][x] != 'V' and (str(x) + '_' + str(y - 1)) not in zj:
                return 'up'
        return direction[random.randint(1, 4)] #随机走
    else:   #地图上有敌人或分数
        d = []
        # 计算与敌人的距离
        for i in range(len(d_x)):
            d.append(pow((pow((d_x[i] - x), 2)) + pow(d_y[i] - y, 2), 0.5))
        for i in range(len(d)):#这里配置权重
            #if d[i]<=4:
                #r_x += (d_x[i] - x) * pow(0.9, d[i]) * s[i]
                #r_y += (d_y[i] - y) * pow(0.9, d[i]) * s[i]
            if d[i] == 1:
                r_x += (d_x[i] - x) * 0.9 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.9 * pow(10, s[i])
            elif 2 > d[i] > 1:
                r_x += (d_x[i] - x) * 0.09 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.09 * pow(10, s[i])
            elif d[i] == 2:
                r_x += (d_x[i] - x) * 0.009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.009 * pow(10, s[i])
            elif 3 > d[i] > 2:
                r_x += (d_x[i] - x) * 0.0009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.0009 * pow(10, s[i])
            elif d[i] == 3:
                r_x += (d_x[i] - x) * 0.00009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.00009 * pow(10, s[i])
            elif 4 > d[i] > 3:
                r_x += (d_x[i] - x) * 0.00001 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.00001 * pow(10, s[i])

        if r_x == 0 and r_y == 0:       #离得很远#或者两个方向的相同抵消了
            try:
                if x > 0:
                    a1 = int(map[y][x - 1][1:])
            except ValueError:
                a1 = 0
            try:
                if x < width - 1:
                    a2 = int(map[y][x + 1][1:])
            except ValueError:
                a2 = 0
            try:
                if y > 0:
                    a3 = int(map[y - 1][x][1:])
            except ValueError:
                a3 = 0
            try:
                if y< height - 1:
                    a4 = int(map[y + 1][x][1:])
            except ValueError:
                a4 = 0
            if x > 0 and (a1 > 0) and (str(x - 1) + '_' + str(y)) not in zj:#认为在左右两侧
                return 'left'
            elif x < (width - 1) and (a2 > 0) and (str(x + 1) + '_' + str(y)) not in zj:
                return 'right'
            elif y > 0 and (a3 > 0) and (str(x) + '_' + str(y - 1)) not in zj:#认为在上下两侧
                return 'up'
            elif y < height - 1 and (a4 > 0) and (str(x) + '_' + str(y + 1)) not in zj:#认为在上下两侧
                return 'down'
            else: #分/敌人离得很远
                if x < 2:
                    if map[y][x + 1] != 'x' and map[y][x + 1] != '<' and (str(x + 1) + '_' + str(y)) not in zj:
                        return "right"
                if x > width - 2:
                    if map[y][x - 1] != 'x' and map[y][x - 1] != '>' and (str(x - 1) + '_' + str(y)) not in zj:
                        return "left"
                if y < 2:
                    if map[y + 1][x] != 'x' and map[y + 1][x] != '^' and (str(x) + '_' + str(y + 1)) not in zj:
                        return "down"
                if y > height - 2:
                    if map[y - 1][x] != 'x' and map[y - 1][x] != 'V' and (str(x) + '_' + str(y - 1)) not in zj:
                        return 'up'
            return direction[random.randint(1, 4)]  # 随机走
        elif r_x == 0 and r_y > 0:#这个分数在下面
            if y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y - 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                res = "down"
            elif x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            else:
                res = 'up'
        elif r_x == 0 and r_y < 0:#这个分在上面
            if y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            elif x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            else:
                res = 'left'
        elif r_x > 0 and r_y == 0:#这个分在右面
            if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            else:
                res = 'down'
        elif r_x < 0 and r_y == 0:#这个敌人在左面
            if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                res = 'left'
            elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            else:
                res = 'down'
        else:
            O = r_y / r_x
            if (O > 1 or O < -1) and r_y > 0:        #方向向下
                if y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                    res = "down"
                else:
                    if O < 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                        res = 'left'
                    else:
                        res = 'right'
            elif (O > 1 or O < -1) and r_y < 0:      #方向向上
                if y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                    res = "up"
                else:
                    if O > 0 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                        res = 'right'
                    else:
                        res = 'left'
            elif -1 < O < 1 and r_x > 0:            #方向向右
                if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                    res = "right"
                else:
                    if O > 0 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                        res = 'down'
                    else:
                        res = 'up'
            elif -1 < O < 1 and r_x < 0:            #方向向左
                if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                    res = "left"
                else:
                    if O > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                        res = 'up'
                    else:
                        res = 'down'
            elif O == -1 and r_x > 0:               #判断两个方向走都可以的情况 右上
                if x < width -1 and (map[y][x +1] != 'x' and map[y][x +1] != '+' and map[y][x +1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:#右侧没有石头并且油路
                    res = "right"
                elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:    #上侧没有石头并且有路
                    res = "up"
                else:
                    res = "left"

            elif O == 1 and r_x < 0 :               #判断两个方向走都可以的情况 左上
                if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:#左侧没有石头并且油路
                    res = "left"
                elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:  # 上侧没有石头并且有路
                    res = "up"
                else:
                    res = "down"

            elif O == -1 and r_x < 0:               #判断两个方向走都可以的情况 左下
                if x > 0  and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '<') and (str(x - 1) + '_' + str(y)) not in zj:#zuo侧没有石头并且油路
                    res = "left"
                elif y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:  # 下侧没有石头并且有路
                    res = "down"
                else:
                    res = "right"
            elif O == 1 and r_x > 0:               #判断两个方向走都可以的情况 右xia
                if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:#右侧没有石头并且油路
                    res = "right"
                elif y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:    #下侧没有石头并且有路
                    res = "down"
                else:
                    res = "up"
    return res


def leg_start(msg):
    '''
    :param msg:
    :return: None
    '''
    print ("round start")
    try:
        global width
        global height
        global vision
        global map_s
        global my_id
        global R_B
    finally:
        a = 1 + 1
    width = int(msg['msg_data']['map']['width'])
    height = int(msg['msg_data']['map']['height'])
    vision = int(msg['msg_data']['map']['vision'])
    map_s = [['o' for i in range(width)]for i in range(height)]         #可以走的地方
    for itm in msg['msg_data']['map']['meteor']:
        map_s[int(itm['y'])][int(itm['x'])] = 'x'                       #陨石
    for itm in msg['msg_data']['map']['tunnel']:
        if itm['direction'] == 'down':
            map_s[int(itm['y'])][int(itm['x'])] = 'V'                   #快速通道
        elif itm['direction'] == 'up':
            map_s[int(itm['y'])][int(itm['x'])] = '^'                   #快速通道
        elif itm['direction'] == 'left':
            map_s[int(itm['y'])][int(itm['x'])] = '<'                   #快速通道
        elif itm['direction'] == 'right':
            map_s[int(itm['y'])][int(itm['x'])] = '>'                   #快速通道
    for itm in msg['msg_data']['map']['wormhole']:
            map_s[int(itm['y'])][int(itm['x'])] = itm['name']          #传送门
    try:
        my_id = []
        for my in msg['msg_data']['teams']:
            if my['id'] == constants.team_id:
                R_B = my['force']
                for i in range(4):
                    my_id.append(int(my['players'][i]))
    except KeyError:
        a = 1+1
    for i in range(height):
        for j in range(width):
            print(map_s[i][j],end=" ")
        print("")

    print ("msg_name:%s" % msg['msg_name'])
    print ("map_width:%s" % msg['msg_data']['map']['width'])
    print ("map_height:%s" % msg['msg_data']['map']['height'])
    print ("vision:%s" % msg['msg_data']['map']['vision'])
    print ("meteor:%s" % msg['msg_data']['map']['meteor'])
    # print ("cloud:%s" % msg['msg_data']['map']['cloud'])
    print ("tunnel:%s" % msg['msg_data']['map']['tunnel'])
    print ("wormhole:%s" % msg['msg_data']['map']['wormhole'])
    print ("teams:%s" % msg['msg_data']['teams'])
    f = open("E:\用户\文档\桌面\鲲鹏\测试\out.txt", "a")
    for i in range(height):
        for j in range(width):
            print(map_s[i][j],end=" ",file=f)
        print("",file=f)
    print ("round start",file=f)
    print (str(msg),file=f)

    print ("msg_name:%s" % msg['msg_name'],file=f)
    print ("map_width:%s" % msg['msg_data']['map']['width'],file=f)
    print ("map_height:%s" % msg['msg_data']['map']['height'],file=f)
    print ("vision:%s" % msg['msg_data']['map']['vision'],file=f)
    print ("meteor:%s" % msg['msg_data']['map']['meteor'],file=f)
    # print ("cloud:%s" % msg['msg_data']['map']['cloud'],file=f)
    print ("tunnel:%s" % msg['msg_data']['map']['tunnel'],file=f)
    print ("wormhole:%s" % msg['msg_data']['map']['wormhole'],file=f)
    print ("teams:%s" % msg['msg_data']['teams'],file=f)


def leg_end(msg):
    '''

    :param msg:
    {
        "msg_name" : "leg_end",
        "msg_data" : {
            "teams" : [
            {
                "id" : 1001,				#队ID
                "point" : 770             #本leg的各队所得点数
            },
            {
            "id" : 1002,
            "point" : 450
             }
            ]
        }
    }

    :return:
    '''
    print ("round over")
    teams = msg["msg_data"]['teams']
    for team in teams:
        print ("teams:%s" % team['id'])
        print ("point:%s" % team['point'])
        print ("\n\n")
    f = open("E:\用户\文档\桌面\鲲鹏\测试\out.txt", "a")
    print ("round over",file=f)

def game_over(msg):
    print ("game over!")
    f = open("out.txt", "a")
    print ("game over!", file = f)


def round(msg):
    import random
    '''
    :param msg: dict
    :return:
    return type: dict
    '''
    print ("round")
    #移动方向定义
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    # 创建本回合的视野地图
    round_map = [['o' for i in range(20)]for i in range(20)]                #创建地图模型
    for i in range(height):                                                  #读取基础地图
        for j in range(width):
            round_map[i][j] = map_s[i][j]
    try:                                                                    #获取能量位置
        for itm in msg['msg_data']['power']:
            round_map[int(itm['y'])][int(itm['x'])] = 'p' + str(itm['point'])
    except KeyError:
        a = 1 + 1
    try:                                                                    #获取对手和自己的位置
        for itm in msg['msg_data']['players']:
            if itm['team'] == constants.team_id:
                round_map[int(itm['y'])][int(itm['x'])] = '+'
            else:
                round_map[int(itm['y'])][int(itm['x'])] = "-" + str(itm['score'])
    except KeyError:
        a = 1+1
    #获取回合信息
    #获取回合号
    round_id = msg['msg_data']['round_id']
    # 获取本回合场上玩家信息
    try:
        players = msg['msg_data']['players']
    except KeyError:
        a = 1
    # 获取本回合的进攻防守模式 beat防守 think进攻
    mode = msg['msg_data']['mode']
    #确定自己的动作
    action = []
    # 记录足迹
    zj = []
    try:
        if str(mode) == str(R_B):#进攻模式
            for player in players:
                if player['team'] == constants.team_id:
                    a = Attack(round_map, player,zj)
                    if a == 'down':
                        zj.append(str(player['x']) + '_' + str(player['y'] + 1))
                    if a == 'up':
                        zj.append(str(player['x']) + '_' + str(player['y'] - 1))
                    if a == 'right':
                        zj.append(str(player['x'] + 1) + '_' + str(player['y']))
                    if a == 'left':
                        zj.append(str(player['x'] - 1) + '_' + str(player['y']))
                    print(a)
                    action.append({"team": player['team'], "player_id": player['id'],
                        "move": [a]})
        else:#防守模式
            for player in players:
                if player['team'] == constants.team_id:
                    a = Defense(round_map, player)
                    print(a)
                    action.append({"team": player['team'], "player_id": player['id'],
                        "move": [a]})
    except KeyError:
        a = 1
    except UnboundLocalError:
        a = 1
    #返回信息模型
    result = {
        "msg_name": "action",
        "msg_data": {
            "round_id": round_id
        }
    }
    result['msg_data']['actions'] = action
    ## 输出
    f =open("E:\用户\文档\桌面\鲲鹏\测试\out.txt", "a")
    print("youshi:{}".format(msg['msg_data']['mode']))
    print(msg, file=f)
    for i in range(height):
        for j in range(width):
            print(round_map[i][j], end=" ", file=f)
        print("", end="\n", file=f)
    return result

# pushd %CD%
# cd /d bin
# client.exe %1 %2 %3
# popd

# EXIT