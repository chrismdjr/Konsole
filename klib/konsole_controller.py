from pyPS4Controller.controller import Controller as ControllerEventHandler

import struct
import enum
import threading
import queue
import os
import time

class Controller:
    def __init__(self):
        self._controller_event_handler = _KonsoleControllerEventHandler(interface="/dev/input/js0", connecting_using_ds4drv=False)
        self._controller_event_queue = queue.Queue()

        self._controller_thread = threading.Thread(
            target=_run_controller_thread,
            args=(self._controller_event_handler, self._controller_event_queue),
            daemon=True
        )

    def wait_for_interface(self, renderer):
        renderer.clear()
        renderer.draw_text(1, 0, "WAITING FOR\nCONTROLLER", (255, 255, 255))
        renderer.present()

        self._controller_event_handler.wait_for_interface()

    def start(self):
        self._controller_thread.start()

    def poll_events(self):
        controller_events = []
        while True:
            try:
                controller_events.append(self._controller_event_queue.get(block=False))
            except queue.Empty:
                break

        return controller_events

class ControllerEventType(enum.Enum):
    X_PRESS = enum.auto()
    X_RELEASE = enum.auto()
    TRIANGLE_PRESS = enum.auto()
    TRIANGLE_RELEASE = enum.auto()
    CIRCLE_PRESS = enum.auto()
    CIRCLE_RELEASE = enum.auto()
    SQUARE_PRESS = enum.auto()
    SQUARE_RELEASE = enum.auto()
    L1_PRESS = enum.auto()
    L1_RELEASE = enum.auto()
    L2_PRESS = enum.auto()
    L2_RELEASE = enum.auto()
    R1_PRESS = enum.auto()
    R1_RELEASE = enum.auto()
    R2_PRESS = enum.auto()
    R2_RELEASE = enum.auto()
    UP_ARROW_PRESS = enum.auto()
    DOWN_ARROW_PRESS = enum.auto()
    UP_OR_DOWN_ARROW_RELEASE = enum.auto()
    LEFT_ARROW_PRESS = enum.auto()
    RIGHT_ARROW_PRESS = enum.auto()
    LEFT_OR_RIGHT_ARROW_RELEASE = enum.auto()
    L3_UP = enum.auto()
    L3_DOWN = enum.auto()
    L3_LEFT = enum.auto()
    L3_RIGHT = enum.auto()
    L3_X_AT_REST = enum.auto()
    L3_Y_AT_REST = enum.auto()
    L3_PRESS = enum.auto()
    L3_RELEASE = enum.auto()
    R3_UP = enum.auto()
    R3_DOWN = enum.auto()
    R3_LEFT = enum.auto()
    R3_RIGHT = enum.auto()
    R3_X_AT_REST = enum.auto()
    R3_Y_AT_REST = enum.auto()
    R3_PRESS = enum.auto()
    R3_RELEASE = enum.auto()
    OPTIONS_PRESS = enum.auto()
    OPTIONS_RELEASE = enum.auto()
    SHARE_PRESS = enum.auto()
    SHARE_RELEASE = enum.auto()
    PLAYSTATION_BUTTON_PRESS = enum.auto()
    PLAYSTATION_BUTTON_RELEASE = enum.auto()

class ControllerEvent:
    def __init__(self, event_type, value=None):
        self.event_type = event_type
        self.value = value

class _KonsoleControllerEventHandler(ControllerEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interface_file = None # defined in wait_for_interface()

    def wait_for_interface(self):
        while os.path.exists(self.interface) != True:
            time.sleep(1)

        self._interface_file = open(self.interface, "rb")

    def listen_once(self):
        event = self._read_event()
        if self.stop == True or event == None:
            return

        overflow, value, button_type, button_id = self._unpack_event(event)
        if button_id not in self.black_listed_buttons:
            return self._handle_event(
                button_id=button_id,
                button_type=button_type,
                value=value,
                overflow=overflow,
                debug=self.debug
            )

    def _handle_event(
        self,
        button_id,
        button_type,
        value,
        overflow,
        debug
    ):
        event = self.event_definition(
            button_id=button_id,
            button_type=button_type,
            value=value,
            connecting_using_ds4drv=self.connecting_using_ds4drv,
            overflow=overflow,
            debug=debug
        )

        if event.L3_event():
            if event.L3_up():
                return ControllerEvent(ControllerEventType.L3_UP, event.value)
            elif event.L3_down():
                return ControllerEvent(ControllerEventType.L3_DOWN, event.value)
            elif event.L3_left():
                return ControllerEvent(ControllerEventType.L3_LEFT, event.value)
            elif event.L3_right():
                return ControllerEvent(ControllerEventType.L3_RIGHT, event.value)
            elif event.L3_x_at_rest():
                return ControllerEvent(ControllerEventType.L3_X_AT_REST)
            elif event.L3_y_at_rest():
                return ControllerEvent(ControllerEventType.L3_Y_AT_REST)
        if event.R3_event():
            if event.R3_up():
                return ControllerEvent(ControllerEventType.R3_UP, event.value)
            elif event.R3_down():
                return ControllerEvent(ControllerEventType.R3_DOWN, event.value)
            elif event.R3_left():
                return ControllerEvent(ControllerEventType.R3_LEFT, event.value)
            elif event.R3_right():
                return ControllerEvent(ControllerEventType.R3_RIGHT, event.value)
            elif event.R3_x_at_rest():
                return ControllerEvent(ControllerEventType.R3_X_AT_REST)
            elif event.R3_y_at_rest():
                return ControllerEvent(ControllerEventType.R3_Y_AT_REST)
        elif event.L3_pressed():
            return ControllerEvent(ControllerEventType.L3_PRESS)
        elif event.L3_released():
            return ControllerEvent(ControllerEventType.L3_RELEASE)
        elif event.R3_pressed():
            return ControllerEvent(ControllerEventType.R3_PRESS)
        elif event.R3_released():
            return ControllerEvent(ControllerEventType.R3_RELEASE)
        elif event.x_pressed():
            return ControllerEvent(ControllerEventType.X_PRESS)
        elif event.x_released():
            return ControllerEvent(ControllerEventType.X_RELEASE)
        elif event.triangle_pressed():
            return ControllerEvent(ControllerEventType.TRIANGLE_PRESS)
        elif event.triangle_released():
            return ControllerEvent(ControllerEventType.TRIANGLE_RELEASE)
        elif event.circle_pressed():
            return ControllerEvent(ControllerEventType.CIRCLE_PRESS)
        elif event.circle_released():
            return ControllerEvent(ControllerEventType.CIRCLE_RELEASE)
        elif event.square_pressed():
            return ControllerEvent(ControllerEventType.SQUARE_PRESS)
        elif event.square_released():
            return ControllerEvent(ControllerEventType.SQUARE_RELEASE)
        elif event.L1_pressed():
            return ControllerEvent(ControllerEventType.L1_PRESS)
        elif event.L1_released():
            return ControllerEvent(ControllerEventType.L1_RELEASE)
        elif event.L2_pressed():
            return ControllerEvent(ControllerEventType.L2_PRESS, event.value)
        elif event.L2_released():
            return ControllerEvent(ControllerEventType.L2_RELEASE)
        elif event.R1_pressed():
            return ControllerEvent(ControllerEventType.R1_PRESS)
        elif event.R1_released():
            return ControllerEvent(ControllerEventType.R1_RELEASE)
        elif event.R2_pressed():
            return ControllerEvent(ControllerEventType.R2_PRESS, event.value)
        elif event.R2_released():
            return ControllerEvent(ControllerEventType.R2_RELEASE)
        elif event.up_arrow_pressed():
            return ControllerEvent(ControllerEventType.UP_ARROW_PRESS)
        elif event.down_arrow_pressed():
            return ControllerEvent(ControllerEventType.DOWN_ARROW_PRESS)
        elif event.up_down_arrow_released():
            return ControllerEvent(ControllerEventType.UP_OR_DOWN_ARROW_RELEASE)
        elif event.left_arrow_pressed():
            return ControllerEvent(ControllerEventType.LEFT_ARROW_PRESS)
        elif event.right_arrow_pressed():
            return ControllerEvent(ControllerEventType.RIGHT_ARROW_PRESS)
        elif event.left_right_arrow_released():
            return ControllerEvent(ControllerEventType.LEFT_OR_RIGHT_ARROW_RELEASE)
        elif event.options_pressed():
            return ControllerEvent(ControllerEventType.OPTIONS_PRESS)
        elif event.options_released():
            return ControllerEvent(ControllerEventType.OPTIONS_RELEASE)
        elif event.share_pressed():
            return ControllerEvent(ControllerEventType.SHARE_PRESS)
        elif event.share_released():
            return ControllerEvent(ControllerEventType.SHARE_RELEASE)
        elif event.playstation_button_pressed():
            return ControllerEvent(ControllerEventType.PLAYSTATION_BUTTON_PRESS)
        elif event.playstation_button_released():
            return ControllerEvent(ControllerEventType.PLAYSTATION_BUTTON_RELEASE)

    def _read_event(self):
        return self._interface_file.read(self.event_size)

    def _unpack_event(self, event):
        unpacked_event = struct.unpack(self.event_format, event)
        return unpacked_event[3:], unpacked_event[2], unpacked_event[1], unpacked_event[0]

def _run_controller_thread(controller_event_handler, controller_event_queue):
    while True:
        controller_event = controller_event_handler.listen_once()
        if controller_event != None:
            controller_event_queue.put(controller_event)