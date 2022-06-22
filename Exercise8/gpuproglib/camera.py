from pyrr import Matrix44, Vector3, Quaternion

class Camera:
    def __init__(self, target, eye, upVec, ar, fov, zNear, zFar):
        self.target: Vector3 = Vector3(target)
        self.eye: Vector3 = Vector3(eye)
        self.up: Vector3 = Vector3(upVec).normalized
        self.ar_ = ar
        self.fov_ = fov
        self.zNear_ = zNear
        self.zFar_ = zFar

    def rotate(self, dx, dy):
        self.rotate_x(dy)
        self.rotate_y(dx)

    def rotate_y(self, angle):
        q = Quaternion.from_y_rotation(angle)
        pos = q * (self.eye - self.target)
        self.eye = pos + self.target

    def rotate_x(self, angle):
        forward = (self.target - self.eye).normalized
        up = self.up.normalized
        axis = forward ^ up
        q = Quaternion.from_axis_rotation(axis, angle)

        pos = q * (self.eye - self.target)
        self.eye = pos + self.target

    def get_view_matrix(self):
        return Matrix44.look_at(self.eye, self.target, self.up)

    def get_projection_matrix(self):
        return Matrix44.perspective_projection(self.fov_, self.ar_, self.zNear_, self.zFar_)
