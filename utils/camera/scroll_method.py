from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from utils.camera.camera import Camera
    from utils.entities.player import Player


class ScrollMethod(ABC):
    def __init__(self, camera: Camera, player: Player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(ScrollMethod):
    def __init__(self, camera: Camera, player: Player, Kp: float, Ki: float, Kd: float):
        super().__init__(camera, player)

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error_x = 0
        self.integral_x = 0

    def scroll(self):
        error_x = self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x

        self.integral_x += error_x

        derivative_x = error_x - self.prev_error_x

        self.prev_error_x = error_x

        self.camera.offset_float.x += (self.Kp * error_x +
                                       self.Ki * self.integral_x + self.Kd * derivative_x)
        self.camera.offset_float.y += (self.player.rect.y -
                                       self.camera.offset_float.y + self.camera.CONST.y)

        self.camera.offset.x, self.camera.offset.y = int(
            self.camera.offset_float.x), int(self.camera.offset_float.y)


class Border(Follow):
    def __init__(self, camera: Camera, player: Player, Kp: float, Ki: float, Kd: float, border_left: int | None = None, border_right: int | None = None):
        super().__init__(camera, player, Kp, Ki, Kd)

        self.border_left = border_left
        self.border_right = border_right

    def __bound_camera_offset(self):
        if self.border_left is not None:
            self.camera.offset.x = max(
                self.camera.offset.x, self.border_left)

        if self.border_right is not None:
            self.camera.offset.x = min(
                self.camera.offset.x, self.border_right - self.camera.DISPLAY_SIZE.x)

    def scroll(self):
        # self.camera.offset_float.x += (self.player.rect.x -
        #                                self.camera.offset_float.x + self.camera.CONST.x)
        # self.camera.offset_float.y += (self.player.rect.y -
        #                                self.camera.offset_float.y + self.camera.CONST.y)

        # self.camera.offset.x, self.camera.offset.y = int(
        #     self.camera.offset_float.x), int(self.camera.offset_float.y)

        # # self.camera.offset.x = max(0, self.camera.offset.x)
        super().scroll()

        self.__bound_camera_offset()
