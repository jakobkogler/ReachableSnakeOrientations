import time
import sys


class SnakeOrientations:
    def points_in_quadrant(self, rectangle, center, radius, points):
        """Determines, if any points is inside a quadrant.
        The quadrant is defined as intersection of a rectangle and a circle
        """

        x1, x2, y1, y2 = rectangle

        return any(x1 <= x <= x2 and y1 <= y <= y2
                   and (center[0] - x)**2 + (center[1] - y)**2 <= radius**2
                   for (x, y) in points)

    def rotation_allowed(self, fixed_points, points, rotation_direction):
        """Determines, if the rotation of points is allowed or not.
        The rotation point is the last point in fixed_points.
        """

        p = fixed_points[-1]
        q = points[-1]

        if rotation_direction == 0:
            rectangle_x = [q[0], p[1] - q[1] + p[0]]
            rectangle_y = [q[1], q[0] - p[0] + p[1]]
        else:
            rectangle_x = [q[0], q[1]-p[1]+p[0]]
            rectangle_y = [q[1], p[0]-q[0]+p[1]]

        rectangle = (min(rectangle_x), max(rectangle_x), min(rectangle_y), max(rectangle_y))
        return not self.points_in_quadrant(rectangle, p, len(points), fixed_points[:-1])

    def rotate(self, fixed_points, points, rotation_direction=0):
        """Computes and returns rotated points.
        The rotation point is the last point in fixed_points.
        """

        p = fixed_points[-1]

        # translate, rotate, translate
        if rotation_direction == 0:
            return [(p[1] - y + p[0], x - p[0] + p[1]) for (x, y) in points]
        else:
            return [(y - p[1] + p[0], p[0] - x + p[1]) for (x, y) in points]

    def compute_reachable_snake_orientations(self, n):
        """Computes the number of reachable snake orientations of length n
        up to rotation, translation and mirror symmetry.
        """

        self.orientations = set()
        self.recursive_search([(0, 0)], [(0, i+1) for i in range(n)], [])
        return len(self.orientations)

    def recursive_search(self, fixed, points, rotations, rotation_done=False):
        """Recursively searches for all reachable snake orientations.
        """

        if len(points) <= 1:
            rot = rotations
            rot = min(rot, rot[::-1], [2-r for r in rot], [2-r for r in rot][::-1])
            value = 0
            for r in rot:
                value = 3*value + r
            self.orientations.add(value)

        else:
            fixed = fixed + [points.pop(0)]

            # rotation left
            if self.rotation_allowed(fixed, points, 0):
                self.recursive_search(fixed, self.rotate(fixed, points, 0), rotations + [0], True)

            # rotation right
            if rotation_done and self.rotation_allowed(fixed, points, 1):
                self.recursive_search(fixed, self.rotate(fixed, points, 1), rotations + [2], True)

            # no rotation
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
