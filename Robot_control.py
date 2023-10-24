import urx
from tqdm import tqdm
import numpy as np

mm_to_meter = 1 / 1000


class RobotControl:
    def __init__(self, robot_ip="172.26.20.211", workspace_length=500, step_size=100, ):
        self.robot = urx.Robot(robot_ip)
        self.workspace_length = workspace_length  # 单位mm
        self.step_size = step_size  # 单位mm
        # 输入工作空间起始点，最右下角的那个点，该点的xyz坐标最小
        self.start_position = [-0.2, -0.8, -0.2, 3.14, 0, 0]  # 底面右前
        self.range = None

    def move(self, pos_type):
        if pos_type == "init":
            target_position = [0.111, -0.487, 0.433, 3.14, 0, 0]
        elif pos_type == "home":
            target_position = [0, -0.194, 1, 0, -2.23, 2.22]
        else:
            raise ValueError("Invalid position type")

        self.robot.movel(target_position, acc=0.1, vel=0.3, wait=True)

    def stop(self):
        self.robot.stopl()

    def start_scan(self, workspace=(500, 500, 500), interval=(10, 10, 10)):
        assert len(workspace) == 3
        assert len(interval) == 3

        workspace = np.array(workspace)
        interval = np.array(interval)

        self.final_position = self.start_position[:3] + workspace * mm_to_meter

        x_steps, y_steps, z_steps = interval  # 单位mm
        workspace_lengthx, workspace_lengthy, workspace_lengthz = workspace  # 单位mm
        self.step_interval = interval  # move_step中使用
        self.numx = int(workspace_lengthx / x_steps + 1)
        self.numy = int(workspace_lengthy / y_steps + 1)
        self.numz = int(workspace_lengthz / z_steps + 1)

        self.num = np.ceil(workspace / interval) + (1, 1, 1)

        # scan_total_num 记录扫描过程的总步数，配合tqdm使用
        # TODO: np.prod()
        self.scan_total_num = np.prod(self.num)

        self.x_range = (self.start_position[0], self.start_position[0] + workspace_lengthx * mm_to_meter)
        self.y_range = (self.start_position[1], self.start_position[1] + workspace_lengthy * mm_to_meter)
        self.z_range = (self.start_position[2], self.start_position[2] + workspace_lengthz * mm_to_meter)

    def _extract_step(self, step):
        if step < 0 or step >= self.scan_total_num:
            raise ValueError("step value out of range!")

        # 确定x, y, z的相对偏移
        x_offset = (step // self.num[1]) % self.num[0]
        y_offset = step % self.num[1]
        z_offset = step // (self.num[0] * self.num[1])
        # 计算实际位置
        return x_offset, y_offset, z_offset

    def move_step(self, step=0, wait=True):

        x, y, z = self._extract_step(step)

        min_pose = self.start_position[:3]
        max_pose = self.final_position[:3]

        actual_pos = self.start_position[:3] + [x, y, z] * self.step_interval * mm_to_meter
        # 与最大和最小位置比较，防止actual_pos数值越界
        actual_pos = np.max(np.vstack([min_pose, actual_pos]), axis=0)
        actual_pos = np.min(np.vstack([max_pose, actual_pos]), axis=0)

        # TODO: bounding box
        actual_pos = np.hstack([actual_pos, self.start_position[3:]])  # 保持rx,ry,rz不变

        if self.x_range[0] <= actual_pos[0] <= self.x_range[1] and \
                self.y_range[0] <= actual_pos[1] <= self.y_range[1] and \
                self.z_range[0] <= actual_pos[2] <= self.z_range[1]:

            self.robot.movel(actual_pos, acc=0.1, vel=0.2, wait=wait)

    def get_pose(self):
        pose = self.robot.getl()
        print("Current Robot Pose:", pose)
        return pose


def main():
    robot = RobotControl()

    robot.move('init')

    robot.start_scan(workspace=(500, 500, 500),
                     interval=(250, 250, 250))  # workspace工作空间(x,y,z), interval各个方向上的步长(x,y,z), 单位都是mm
    # tqdm包，实现实时进度条显示
    for step in tqdm(range(int(robot.scan_total_num))):
        robot.move_step(step, wait=True)  # step为执行到第几步， 总步数为scan_total_num
        


if __name__ == "__main__":
    main()
    # rob = RobotControl()
    # rob.move("init")  # 移动到初始位置
    # rob.get_pose()   # 读取当前位姿
    # rob.stop()  # 暂停机械臂运动