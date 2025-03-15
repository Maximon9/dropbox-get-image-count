from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import QSize, Qt

from typing_extensions import (
    Callable,
    NewType,
    Optional,
    TypedDict,
    NotRequired,
    # list,
)

from PyQt6.QtGui import QResizeEvent

from enum import Enum

from PyQt6.QtCore import QThread, pyqtSignal, QElapsedTimer
import time


class Worker(QThread):
    update = pyqtSignal(int)

    def __init__(self, target_fps=60):
        super().__init__()
        self.target_fps = target_fps
        self.running = True

    def set_fps(self, new_fps):
        """Change the target FPS dynamically."""
        self.target_fps = new_fps

    def run(self):
        fps_counter = 0
        timer = QElapsedTimer()
        timer.start()

        frame_time = 1.0 / self.target_fps  # Target frame time

        while self.running:
            start_time = time.time()
            fps_counter += 1

            # Send FPS count every second
            if timer.elapsed() >= 1000:
                self.update.emit(fps_counter)
                fps_counter = 0
                timer.restart()

            # Sleep to maintain target FPS
            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed_time)
            time.sleep(sleep_time)

    def stop(self):
        """Stops the loop safely."""
        self.running = False
        self.quit()
        self.wait()


class MeasuringUnit(Enum):
    PERCENTAGE = 0
    PIXEL = 0


class LayoutInfo(TypedDict):
    layout: NotRequired[QVBoxLayout]
    stretch_index: NotRequired[int]
    stretch: NotRequired[int]


class GUIInfo(TypedDict):
    gui: Callable[[QWidget], QWidget]
    unit: MeasuringUnit
    size: QSize = QSize(100, 100)
    stretch: NotRequired[int]
    alignment: NotRequired[Qt.AlignmentFlag]


GUIInfos = NewType("GUIInfos", list[GUIInfo])


class WindowInfo(TypedDict):
    title: NotRequired[str]
    guis: NotRequired[GUIInfos]
    width: NotRequired[int]
    height: NotRequired[int]
    resize: NotRequired[Callable[[QResizeEvent]]]
    process: NotRequired[Callable]


class CustomWindow(QWidget):
    app: QApplication
    guis: GUIInfos
    layout_info: LayoutInfo
    layout_info: LayoutInfo
    resize: Callable[[QResizeEvent]]

    def __init__(
        self,
        app: QApplication,
        title: str,
        guis: GUIInfos = [],
        width: int = 1280,
        height: int = 720,
        layout: LayoutInfo = {},
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ):
        super().__init__(parent, flags)
        self.app = app

        screen = self.app.primaryScreen()  # Get the primary screen (main monitor)
        screen_geometry = (
            screen.availableGeometry()
        )  # Get the screen's geometry (x, y, width, height)
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        width = 1280
        height = 720
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.setGeometry(x, y, width, height)

        self.setWindowTitle(title)

        self.init_winidow(layout, guis)

    def resizeEvent(self, event: QResizeEvent):
        self.resize(event)

    def init_winidow(self, layout_info: LayoutInfo = {}, guis: GUIInfos = []):
        self.layout_info = layout_info

        if not "layout" in self.layout_info:
            self.layout_info["layout"] = QVBoxLayout()

        self.guis = guis

        for gui_info in self.guis:
            gui = gui_info["gui"](self)
            if "size" in gui_info:
                gui.setFixedSize(gui_info["size"])
            if not "stretch" in gui_info == None and not "alignment" in gui_info:
                self.layout_info["layout"].addWidget(gui)
            elif "stretch" in gui_info == None and not "alignment" in gui_info:
                self.layout_info["layout"].addWidget(gui, stretch=gui_info["stretch"])
            elif not "stretch" in gui_info == None and "alignment" in gui_info:
                self.layout_info["layout"].addWidget(
                    gui, alignment=gui_info["alignment"]
                )
            elif "stretch" in gui_info == None and "alignment" in gui_info:
                self.layout_info["layout"].addWidget(
                    gui,
                    stretch=gui_info["stretch"],
                    alignment=gui_info["alignment"],
                )
        # Show the window
        if "stretch_index" in self.layout_info and "stretch" in self.layout_info:
            self.layout_info["layout"].setStretch(
                self[layout_info["stretch_index"], layout_info["stretch"]]
            )
        # self.layout_info["layout"].addStretch
        self.setLayout(layout_info["layout"])
        self.show()


Windows = NewType("Windows", list[CustomWindow])


class CustomApp(QApplication):
    windows: Windows
    process: Callable
    worker: Worker

    def __init__(self, worker, windows_infos: list[WindowInfo], argv: list[str] = []):
        super().__init__(argv)

        self.worker = Worker(target_fps=60)
        self.worker.updated.connect(self.update_counter)
        self.worker.start()

        self.windows = []
        for window_info in windows_infos:
            title = ""
            if "title" in window_info:
                title = window_info["title"]

            guis = []
            if "guis" in window_info:
                guis = window_info["guis"]

            width = 1280
            if "width" in window_info:
                width = window_info["width"]

            height = 720
            if "height" in window_info:
                height = window_info["height"]

            self.windows.append(
                CustomWindow(self, title=title, guis=guis, width=width, height=height)
            )

    def add_window(self, window_info: WindowInfo):
        title = ""
        if "title" in window_info:
            title = window_info["title"]

        guis = []
        if "guis" in window_info:
            guis = window_info["guis"]

        width = 1280
        if "width" in window_info:
            width = window_info["width"]

        height = 720
        if "height" in window_info:
            height = window_info["height"]

        self.windows.append(
            CustomWindow(title=title, guis=guis, width=width, height=height)
        )
