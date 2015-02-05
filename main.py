import time

def rotation(fixed, points, dir=0):
    p = points[0]
    points = points[1:]
    fixed = fixed[:]
    fixed.append(p)

    q1 = points[-1]
    #remember last point

    #translate, rotate, translate
    if dir==0:
        points = [(p[1]-y+p[0],x-p[0]+p[1]) for (x,y) in points]
    else:
        points = [(y-p[1]+p[0],p[0]-x+p[1]) for (x,y) in points]

    q2 = points[-1]
    rect_x = [q1[0], q2[0]]
    rect_y = [q1[1], q2[1]]


    if not any(min(rect_x)<=p[0]<=max(rect_x) and min(rect_y)<=p[1]<=max(rect_y) and (fixed[-1][0]-p[0])**2 + (fixed[-1][1]-p[1])**2 <= len(points)**2 for p in fixed[:-1]):
        return fixed, points
    else:
        return None


def compute_reachable_snake_orientations(n):
    ret = recursive_search([(0,0)], [(0,i+1) for i in range(n)], [])
    #print ret
    return len(set(ret))


def recursive_search(fixed, points, rotations, rotation_done = 0):
    orientations = []

    if len(points) <= 1:
        rot = tuple(rotations)
        rot = min(rot, rot[::-1], tuple(2-r for r in rot), tuple(2-r for r in rot)[::-1])
        value = 0
        for r in rot: value = 3*value + r
        orientations.append(value)
        return orientations

    # try rotation left
    rot_left = rotation(fixed, points, 0)
    if rot_left:

        fixed_left, points_left = rot_left
        orientations += recursive_search(fixed_left, points_left, rotations + [0], 1)

    # try rotation right
    if rotation_done:
        rot_right = rotation(fixed, points, 1)
        if rot_right:
            fixed_right, points_right = rot_right
            orientations += recursive_search(fixed_right, points_right, rotations + [2], rotation_done)

    # straight
    fixed.append(points.pop(0))
    orientations += recursive_search(fixed, points, rotations + [1], rotation_done)

    return orientations


for n in range(20):
    start_time = time.time()
    result = compute_reachable_snake_orientations(n)
    end_time = time.time()
    print "Result for", n, "is", result
    print "duration =", end_time - start_time
