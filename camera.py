# camera.py
import numpy as np
from math import sin, cos, radians
import glm

class Camera:
    def __init__(self, position=(0, 0, 5), target=(0, 0, 0), up=(0, 1, 0)):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.world_up = np.array(up, dtype=np.float32)

        self.yaw = -90.0   # Olhando para +z inicialmente
        self.pitch = 0.0

        self.speed = 0.5
        self.sensitivity = 0.3

        self.update()

    def get_view_matrix(self):
        return glm.lookAt(
            glm.vec3(*self.position),
            glm.vec3(*self.target),
            glm.vec3(*self.world_up)
        )

    def update(self):
        front = np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ])
        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.world_up)
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.front)
        self.up /= np.linalg.norm(self.up)

    def rotate_yaw(self, angle):
        self.yaw += angle
        self.update()
        self._update_position_from_angles()

    def rotate_pitch(self, angle):
        self.pitch = np.clip(self.pitch + angle, -89.0, 89.0)
        self.update()
        self._update_position_from_angles()

    def _update_position_from_angles(self):
        radius = np.linalg.norm(self.position - self.target)
        self.position = self.target + np.array([
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ]) * radius

    def _look_at(self, eye, center, up):
        f = (center - eye)
        f /= np.linalg.norm(f)
        s = np.cross(f, up)
        s /= np.linalg.norm(s)
        u = np.cross(s, f)

        view = np.identity(4, dtype=np.float32)
        view[0, :3] = s
        view[1, :3] = u
        view[2, :3] = -f
        view[:3, 3] = -np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye)
        return view