import sys
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)  # 메인 위젯

        # 그래프를 그리기 위한 도화지 준비 // figsize -> 도화지 크기
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)  # verticalbox 레이아웃
        vbox.addWidget(canvas)  # 도화지 넣기

        self.addToolBar(NavigationToolbar(canvas, self))  # 그래프 툴바

        self.ax = canvas.figure.subplots()  # 좌표축 준비
        self.ax.plot([0, 1, 2], [1, 5, 3], '-')  # 점 찍기(x좌표, y좌표, 뭘로 그릴건지)

        dynamic_canvas = FigureCanvas(
            Figure(figsize=(4, 3)))  # 움직이는 그래프를 위한 도화지
        vbox.addWidget(dynamic_canvas)  # 도화지 넣기

        self.dynamic_ax = dynamic_canvas.figure.subplots()  # 좌표축 준비
        self.timer = dynamic_canvas.new_timer(
            100, [(self.update_canvas, (), {})])  # 그래프가 변하는 주기를 위한 타이머 준비 (0.1초, 실행되는 함수)
        self.timer.start()  # 타이머 시작

        self.setWindowTitle('Matplotlib in PyQt5')
        self.setGeometry(300, 100, 600, 600)
        self.show()

    def update_canvas(self):  # 그래프 변화 함수
        self.dynamic_ax.clear()
        t = np.linspace(0, 2 * np.pi, 101)  # 0 ~ 2파이까지 101개의 숫자로 채우기
        self.dynamic_ax.plot(t, np.sin(t + time.time()),
                             color='deeppink')  # 점 찍기
        self.dynamic_ax.figure.canvas.draw()  # 그리기


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
