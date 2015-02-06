import time
import sys


class SnakeOrientations:
    def rotation_allowed(self, fixed_points, points, rotation_direction):
        p = fixed_points[-1]
        q = points[-1]

        if rotation_direction == 0:
            rect_x = [q[0], p[1]-q[1]+p[0]]
            rect_y = [q[1], q[0]-p[0]+p[1]]
        else:
            rect_x = [q[0], q[1]-p[1]+p[0]]
            rect_y = [q[1], p[0]-q[0]+p[1]]

        return not any(min(rect_x) <= q[0] <= max(rect_x) and min(rect_y) <= q[1] <= max(rect_y)
                  and (p[0] - q[0])**2 + (p[1] - q[1])**2 <= len(points)**2 for q in fixed_points[:-1])

    def rotate(self, fixed_points, points, rotation_direction = 0):
        p = fixed_points[-1]

        # translate, rotate, translate
        if rotation_direction == 0:
            return [(p[1] - y + p[0], x - p[0] + p[1]) for (x, y) in points]
        else:
            return [(y - p[1] + p[0], p[0] - x + p[1]) for (x, y) in points]

    def compute_reachable_snake_orientations(self, n):
        self.orientations = set()
        self.recursive_search([(0, 0)], [(0, i+1) for i in range(n)], [])
        return len(self.orientations)

    def recursive_search(self, fixed, points, rotations, rotation_done = 0):
        if len(points) <= 1:
            rot = rotations
            rot = min(rot, rot[::-1], [2-r for r in rot], [2-r for r in rot][::-1])
            value = 0
            for r in rot:
                value = 3*value + r
            self.orientations.add(value)
            return

        fixed = fixed + [points.pop(0)]

        # rotation left
        if self.rotation_allowed(fixed, points, 0):
            self.recursive_search(fixed, self.rotate(fixed, points, 0), rotations + [0], 1)

        # rotation right
        if rotation_done and self.rotation_allowed(fixed, points, 1):
            self.recursive_search(fixed, self.rotate(fixed, points, 1), rotations + [2], rotation_done)

        # no rotatio
        self.recursive_search(fixed, points, rotations + [1], rotation_done)


if __name__ == "__main__":
    snakeOrientations = SnakeOrientations()

    if len(sys.argv) > 1:
        print(snakeOrientations.compute_reachable_snake_orientations(int(sys.argv[1])))
    else:
        for n in range(21):
            start_time = time.time()
            result = snakeOrientations.compute_reachable_snake_orientations(n)
            print("{:2d}: {:8d} ({:6.2f} seconds)".format(n, result, time.time() - start_time))
