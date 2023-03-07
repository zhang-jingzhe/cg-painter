#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QInputDialog,
    QStyleOptionGraphicsItem,
    QColorDialog)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QImage
from PyQt5.QtCore import QRectF, Qt


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.polygon_list = []
        self.curve_list = []
        self.rotated = False
        self.r = 0
        self.scaled = False
        self.s = 0
        self.cliped = False
        self.clip_list = []
        self.clip_algorithm = ''
        self.color = QColor(0, 0, 0)

    def start_set_pen(self, color):
        self.color = color

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.polygon_list = []

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.curve_list = []

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def start_translate(self, x, y):
        if self.selected_id != '':
            p_list = self.item_dict[self.selected_id].p_list
            p_list = alg.translate(p_list, x, y)
            self.item_dict[self.selected_id].p_list = p_list
            self.updateScene([self.sceneRect()])

    def start_rotate(self, r):
        if self.selected_id != '':
            self.rotated = True
            self.r = r

    def start_scale(self, s):
        if self.selected_id != '':
            self.scaled = True
            self.s = s

    def start_clip(self, algorithm):
        if self.selected_id != '':
            self.cliped = True
            self.clip_algorithm = algorithm

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.color)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon':
            if event.buttons() == Qt.LeftButton:
                self.polygon_list.append([x, y])
                self.temp_item = MyItem(self.temp_id, self.status, self.polygon_list, self.temp_algorithm, self.color)
                self.scene().addItem(self.temp_item)
            elif event.buttons() == Qt.RightButton:
                if self.polygon_list != []:
                    print(self.polygon_list)
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.polygon_list = []
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.color)
            self.scene().addItem(self.temp_item)
        elif self.status == 'curve':
            if event.buttons() == Qt.LeftButton:
                self.curve_list.append([x, y])
                self.temp_item = MyItem(self.temp_id, self.status, self.curve_list, self.temp_algorithm, self.color)
                self.scene().addItem(self.temp_item)
            elif event.buttons() == Qt.RightButton:
                if self.curve_list != []:
                    print(self.curve_list)
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.curve_list = []
        if self.rotated:
            self.rotated = False
            p_list = self.item_dict[self.selected_id].p_list
            p_list = alg.rotate(p_list, x, y, self.r)
            self.item_dict[self.selected_id].p_list = p_list
        elif self.scaled:
            self.scaled = False
            p_list = self.item_dict[self.selected_id].p_list
            p_list = alg.scale(p_list, x, y, self.s)
            self.item_dict[self.selected_id].p_list = p_list
        elif self.cliped:
            self.clip_list.append([x, y])
            self.clip_list.append([x, y])
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            if event.buttons() == Qt.LeftButton:
                self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            if event.buttons() == Qt.LeftButton:
                self.temp_item.p_list[-1] = [x, y]
        if self.cliped:
            self.clip_list[-1] = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        if self.cliped:
            self.cliped = False
            p_list = self.item_dict[self.selected_id].p_list
            xmin = min(self.clip_list[0][0], self.clip_list[1][0])
            xmax = max(self.clip_list[0][0], self.clip_list[1][0])
            ymin = min(self.clip_list[0][1], self.clip_list[1][1])
            ymax = max(self.clip_list[0][1], self.clip_list[1][1])
            p_list = alg.clip(p_list, xmin, ymin, xmax, ymax, self.clip_algorithm)
            self.item_dict[self.selected_id].p_list = p_list
            self.clip_list = []
            self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color: QColor = QColor(0, 0, 0),
                 parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id  # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list  # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.color = color

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.color)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            resx = [x for x, _ in self.p_list]
            resy = [y for _, y in self.p_list]
            x = min(resx)
            y = min(resy)
            w = max(resx) - x
            h = max(resy) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            resx = [x for x, _ in self.p_list]
            resy = [y for _, y in self.p_list]
            x = min(resx)
            y = min(resy)
            w = max(resx) - x
            h = max(resy) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        set_pen_act.triggered.connect(self.set_pen_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def set_pen_action(self):
        self.statusBar().showMessage('设置画笔颜色')
        color = QColorDialog.getColor()
        self.canvas_widget.start_set_pen(color)
        self.scene.update()

    def save_canvas_action(self):
        self.statusBar().showMessage('保存画布')
        view = self.canvas_widget
        image = QImage(view.size(), QImage.Format_ARGB32)
        color = QColor(Qt.white)
        image.fill(color.rgb())
        painter = QPainter(image)
        view.render(painter)
        painter.end()
        name, nameok = QInputDialog.getText(self, '保存画布', '输入文件名')
        if nameok:
            image.save(name + ".png")
            folder = os.getcwd()
            os.system("start explorer %s" % folder)

    def reset_canvas_action(self):
        self.statusBar().showMessage('重置画布')
        self.item_cnt = 0
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.list_widget.currentTextChanged.disconnect(
            self.canvas_widget.selection_changed)  # 在清空QListWidget之前应该把链接上的信号和槽解除链接
        self.list_widget.clear()
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        self.scene.clear()

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.scene.update()

    def translate_action(self):
        self.statusBar().showMessage('平移变换')
        x, xok = QInputDialog.getInt(self, '平移', 'x方向平移')
        if xok:
            y, yok = QInputDialog.getInt(self, '平移', 'y方向平移')
            if yok:
                self.canvas_widget.start_translate(x, y)
        self.scene.update()

    def rotate_action(self):
        self.statusBar().showMessage('旋转变换')
        r, rok = QInputDialog.getInt(self, '旋转', '旋转角度')
        if rok:
            self.canvas_widget.start_rotate(r)
        self.scene.update()

    def scale_action(self):
        self.statusBar().showMessage('缩放变换')
        s, sok = QInputDialog.getDouble(self, '缩放', '缩放倍数')
        if sok:
            self.canvas_widget.start_scale(s)
        self.scene.update()

    def clip_cohen_sutherland_action(self):
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪线段')
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.scene.update()

    def clip_liang_barsky_action(self):
        self.statusBar().showMessage('Liang-Barsky算法裁剪线段')
        self.canvas_widget.start_clip('Liang-Barsky')
        self.scene.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
