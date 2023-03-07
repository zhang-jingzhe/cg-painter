#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # print("draw", p_list)
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        # print(x0,x1,y0,y1)
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        # print(x0,x1,y0,y1)
        y_max, y_min, x_max, x_min = max(y0, y1), min(y0, y1), max(x0, x1), min(x0, x1)
        if x0 == x1:
            for y in range(y_min, y_max + 1):
                result.append((x0, y))
        else:
            k = (y1 - y0) / (x1 - x0)
            if k == 0:
                for x in range(x_min, x_max + 1):
                    result.append((x, y0))
            elif abs(k) <= 1:
                if x1 >= x0:
                    for x in range(x0, x1 + 1):
                        result.append((x, round(y0)))
                        y0 += k
                else:
                    for x in range(x0, x1 - 1, -1):
                        result.append((x, round(y0)))
                        y0 -= k
            else:
                k = 1 / k
                if y1 >= y0:
                    for y in range(y0, y1 + 1):
                        result.append((round(x0), y))
                        x0 += k
                else:
                    for y in range(y0, y1 - 1, -1):
                        result.append((round(x0), y))
                        x0 -= k
    elif algorithm == 'Bresenham':
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        x, y = x0, y0
        if dy < dx:
            p = 2 * dy - dx
            k = 0
            while k <= dx:
                result.append((x, y))
                if p > 0:
                    x += sx
                    y += sy
                    p += 2 * (dy - dx)
                else:
                    x += sx
                    p += 2 * dy
                k += 1
        else:
            p = 2 * dx - dy
            k = 0
            while k <= dy:
                # print(x, y)
                result.append((x, y))
                if p > 0:
                    x += sx
                    y += sy
                    p += 2 * (dx - dy)
                else:
                    y += sy
                    p += 2 * dx
                k += 1
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    # print("draw_ellipse", p_list)
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 < y1:
        y0, y1 = y1, y0
    result = []
    xc, yc = int((x0 + x1) / 2), int((y0 + y1) / 2)
    rx, ry = x1 - xc, y0 - yc
    rx2 = rx ** 2
    ry2 = ry ** 2
    x, y = 0, ry
    p = ry2 + rx2 / 4 - rx2 * ry
    while ry2 * x < rx2 * y:
        result.append([x, y])
        result.append([-x, y])
        result.append([-x, -y])
        result.append([x, -y])
        x += 1
        if p < 0:
            p = p + 2 * ry2 * x + ry2
        else:
            y -= 1
            p = p + 2 * ry2 * x + ry2 - 2 * rx2 * y
    p = ry2 * (x + 1 / 2) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
    while y >= 0:
        result.append([x, y])
        result.append([-x, y])
        result.append([-x, -y])
        result.append([x, -y])
        y -= 1
        if p > 0:
            p = p - 2 * rx2 * y + rx2
        else:
            x += 1
            p = p + 2 * ry2 * x - 2 * rx2 * y + rx2
    res = []
    for point in result:
        res.append((point[0] + xc, point[1] + yc))
    return res


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    n = len(p_list)
    result = []
    if algorithm == 'Bezier':
        U = []
        u = 0
        while u <= 1:
            U.append(u)
            u = round(u + 0.001, 3)
        for i in range(1001):
            u = U[i]
            x = 0
            y = 0
            for j in range(n):
                b = math.comb(n - 1, j) * (1 - u) ** (n - 1 - j) * u ** j
                x += b * p_list[j][0]
                y += b * p_list[j][1]
            result.append([int(x), int(y)])
    elif algorithm == 'B-spline':
        k = 4  # 四阶三次B样条基函数
        n = len(p_list) - 1  # n+1为控制点个数
        if n <= 2:
            return result
        t = [i / (k + n) for i in range(k + n + 1)]
        u = t[k - 1]
        U = []
        while u <= t[n + 1]:
            U.append(u)
            u = round(u + (t[n + 1] - t[k - 1]) * 0.001, 4)
        for i in range(len(U)):
            u = U[i]
            x = 0
            y = 0
            for j in range(n + 1):
                b = deboor_cox(u, j, 4, t)
                x += b * p_list[j][0]
                y += b * p_list[j][1]
            result.append([int(x), int(y)])
    return result


def deboor_cox(u, i, k, nodes):
    if k == 1:
        if nodes[i] <= u < nodes[i + 1]:
            return 1
        else:
            return 0
    else:
        b1 = b2 = 0
        if nodes[i + k - 1] - nodes[i] != 0:
            b1 = (u - nodes[i]) / (nodes[i + k - 1] - nodes[i])
        if nodes[i + k] - nodes[i + 1] != 0:
            b2 = (nodes[i + k] - u) / (nodes[i + k] - nodes[i + 1])
        return b1 * deboor_cox(u, i, k - 1, nodes) + b2 * deboor_cox(u, i + 1, k - 1, nodes)


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        p_list[i][0] += dx
        p_list[i][1] += dy
    return p_list


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    r = math.radians(r)  # 以左上为原点，x轴指向右，y轴指向下
    for i in range(len(p_list)):
        xi = p_list[i][0]
        yi = p_list[i][1]
        p_list[i][0] = int(x + (xi - x) * math.cos(r) - (yi - y) * math.sin(r))
        p_list[i][1] = int(y + (xi - x) * math.sin(r) + (yi - y) * math.cos(r))
    return p_list


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        xi = p_list[i][0]
        yi = p_list[i][1]
        p_list[i][0] = int(x + (xi - x) * s)
        p_list[i][1] = int(y + (yi - y) * s)
    return p_list


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if algorithm == 'Cohen-Sutherland':
        while 1:
            # print("x0=", x0, ",y0=", y0)
            # print("x1=", x1, ",y1=", y1)
            code0 = point_clip([x0, y0], x_min, y_min, x_max, y_max)
            code1 = point_clip([x1, y1], x_min, y_min, x_max, y_max)
            # print("code0=", code0, ",code1=", code1)
            if code0 & code1 != 0b0000:
                return
            elif code0 | code1 == 0b0000:
                return [[x0, y0], [x1, y1]]
            elif x1 == x0:
                if x_min <= x0 <= x_max:
                    if max(min(y0, y1), y_min) <= min(max(y0, y1), y_max):
                        return [[x0, max(min(y0, y1), y_min)], [x1, min(max(y0, y1), y_max)]]
            elif y1 == y0:
                if y_min <= y0 <= y_max:
                    if max(min(x0, x1), x_min) <= min(max(x0, x1), x_max):
                        return [[max(min(x0, x1), x_min), y0], [min(max(x0, x1), x_max), y1]]
            m = (y1 - y0) / (x1 - x0)
            # print("m=", m)
            if code0 == 0:
                [x0, y0], [x1, y1] = [x1, y1], [x0, y0]
            elif (code0 & 0b1000) == 0b1000:  # 上边界
                x = int(x0 + (y_max - y0) / m)
                x0, y0 = x, y_max
            elif (code0 & 0b0100) == 0b0100:  # 下边界
                x = int(x0 + (y_min - y0) / m)
                x0, y0 = x, y_min
            elif (code0 & 0b0010) == 0b0010:  # 右边界
                y = int(y0 + m * (x_max - x0))
                x0, y0 = x_max, y
            elif (code0 & 0b0001) == 0b0001:  # 左边界
                y = int(y0 + m * (x_min - x0))
                x0, y0 = x_min, y
    elif algorithm == 'Liang-Barsky':
        u0, u1 = 0.0, 1.0
        dx, dy = x1 - x0, y1 - y0
        if dx == 0:
            if x_min <= x0 <= x_max:
                if max(min(y0, y1), y_min) <= min(max(y0, y1), y_max):
                    return [[x0, max(min(y0, y1), y_min)], [x1, min(max(y0, y1), y_max)]]
        elif dy == 0:
            if y_min <= y0 <= y1:
                if max(min(x0, x1), x_min) <= min(max(x0, x1), x_max):
                    return [[max(min(x0, x1), x_min), y0], [min(max(x0, x1), x_max), y1]]
        else:
            u0, u1 = cut(-dx, x0 - x_min, u0, u1)
            u0, u1 = cut(dx, x_max - x0, u0, u1)
            u0, u1 = cut(-dy, y0 - y_min, u0, u1)
            u0, u1 = cut(dy, y_max - y0, u0, u1)
        if u0 <= u1:
            x_0 = int(x0 + u0 * dx)
            y_0 = int(y0 + u0 * dy)
            x_1 = int(x0 + u1 * dx)
            y_1 = int(y0 + u1 * dy)
            return [[x_0, y_0], [x_1, y_1]]


def cut(p, q, u0, u1):
    u = q / p
    if p > 0:
        if u < u1:
            u1 = u
    elif p < 0:
        if u > u0:
            u0 = u
    return u0, u1


def point_clip(point, x_min, y_min, x_max, y_max):
    x0, y0 = point
    code = 0b0000
    if x0 < x_min:
        code += 0b0001
    if x0 > x_max:
        code += 0b0010
    if y0 < y_min:
        code += 0b0100
    if y0 > y_max:
        code += 0b1000
    return code
