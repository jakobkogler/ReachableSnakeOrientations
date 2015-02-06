import time
import sys


class SnakeOrientations:
    def rotation(self, fixed_points, points, dir=0):
        points = points[:]
        p = fixed_points[-1]
        rect_point_1 = points[-1] # remember last point

        # translate, rotate, translate
        if dir==0:
            points = [(p[1]-y+p[0],x-p[0]+p[1]) for (x,y) in points]
        else:
            points = [(y-p[1]+p[0],p[0]-x+p[1]) for (x,y) in points]

        rect_point_2 = points[-1]
        rect_x = [rect_point_1[0], rect_point_2[0]]
        rect_y = [rect_point_1[1], rect_point_2[1]]

        allowed = not any(min(rect_x) <= q[0] <= max(rect_x) and min(rect_y) <= q[1] <= max(rect_y)
                  and (p[0] - q[0])**2 + (p[1] - q[1])**2 <= len(points)**2 for q in fixed_points[:-1])
        return allowed, points


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
        allowed, points_left = self.rotation(fixed, points, 0)
        if allowed:
            self.recursive_search(fixed, points_left, rotations + [0], 1)

        # rotation right
        if rotation_done:
            allowed, points_right = self.rotation(fixed, points, 1)
            if allowed:
                self.recursive_search(fixed, points_right, rotations + [2], rotation_done)

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
