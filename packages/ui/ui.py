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
    List,
)

from PyQt6.QtGui import QResizeEvent

from enum import Enum


class MeasuringUnit(Enum):
    PERCENTAGE = 0
    PIXEL = 0


class LayoutInfo(TypedDict):
    layout: NotRequired[QVBoxLayout]


class UIInfo(TypedDict):
    ui: Callable[[QWidget], QWidget]
    unit: MeasuringUnit = MeasuringUnit.PIXEL
    size: QSize = QSize(100, 100)
    stretch: NotRequired[int] = None
    alignment: NotRequired[Qt.AlignmentFlag] = None


UIInfos = NewType("UIInfos", List[UIInfo])


class WindowInfo(TypedDict):
    title: NotRequired[str]
    ui: NotRequired[UIInfos]
    width: NotRequired[int]
    height: NotRequired[int]


class CustomWindow(QWidget):
    app: QApplication
    uis: UIInfos
    layout_info: LayoutInfo

    def __init__(
        self,
        title: str,
        ui: UIInfos = [],
        width: int = 1280,
        height: int = 720,
        layout: LayoutInfo = {},
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ):
        super(parent, flags)

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

        self.init_winidow(layout, ui)

    def resizeEvent(self, event: QResizeEvent):
        new_size = event.size()  # Get the new size of the window
        print(f"Window resized to: {new_size.width()}x{new_size.height()}")

    def init_winidow(self, layout_info: LayoutInfo = {}, ui: UIInfos = []):
        self.layout_info = layout_info

        if self.layout_info["layout"] == None:
            self.layout_info["layout"] = QVBoxLayout()

        self.uis = ui

        for ui_info in self.uis:
            if ui_info.stretch == None and ui_info.alignment == None:
                self.layout_info["layout"].addWidget(a0=ui_info["ui"]())
            elif ui_info.stretch != None and ui_info.alignment == None:
                self.layout_info["layout"].addWidget(
                    a0=ui_info["ui"](), stretch=ui_info["stretch"]
                )
            elif ui_info.stretch == None and ui_info.alignment != None:
                self.layout_info["layout"].addWidget(
                    a0=ui_info["ui"](), alignment=ui_info["alignment"]
                )
            elif ui_info.stretch != None and ui_info.alignment != None:
                self.layout_info["layout"].addWidget(
                    a0=ui_info["ui"](),
                    stretch=ui_info["stretch"],
                    alignment=ui_info["alignment"],
                )
        # Show the window
        # self.layout_info["layout"].addStretch
        self.setLayout(layout_info["layout"])
        self.show()


Windows = NewType("Windows", List[CustomWindow])


class CustomApp(QApplication):
    windows: Windows

    def __init__(self, windows_infos: List[WindowInfo], argv: list[str] = []):
        for window_info in windows_infos:
            title = None
            if "title" in window_info:
                title = window_info["title"]

            ui = None
            if "width" in window_info:
                ui = window_info["ui"]

            width = None
            if "width" in window_info:
                width = window_info["width"]

            height = None
            if "height" in window_info:
                height = window_info["height"]

            self.windows.append(
                CustomWindow(title=title, ui=ui, width=width, height=height)
            )
        super(argv)

    def add_window(self, window_info: WindowInfo):
        title = window_info["title"]
        if title == None:
            title = ""

        ui = window_info["ui"]

        width = window_info["width"]

        height = window_info["height"]

        self.windows.append(
            CustomWindow(title=title, ui=ui, width=width, height=height)
        )
