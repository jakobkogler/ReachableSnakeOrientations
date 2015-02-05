import visualize

def rotation(fixed, points, dir=0):
    p = points.pop(0)
    fixed.append(p)

    q1 = points[-1]
    #remember last point

    #translate
    points = [(x-p[0],y-p[1]) for (x,y) in points]
    #rotate
    points = [(-y, x) for (x,y) in points] if dir==0 else [(y, -x) for (x,y) in points]
    # translate_back
    points = [(x+p[0],y+p[1]) for (x,y) in points]

    q2 = points[-1]
    rect_x = [q1[0], q2[0]]
    rect_y = [q1[1], q2[1]]


    if not any(min(rect_x)<=p[0]<=max(rect_x) and min(rect_y)<=p[1]<=max(rect_y) and (fixed[-1][0]-p[0])**2 + (fixed[-1][1]-p[1])**2 <= len(points)**2 for p in fixed[:-1]):
        return fixed, points
    else:
        return None

points = [(1,0), (2,0), (3,0), (4,0), (5,0)]

fixed = [(0,0)]
for i in range(4):
    ret = rotation(fixed, points)
    if ret:
        fixed, points = ret
        print(fixed + points)
        visualize.visual(fixed+points, "{}.png".format(i))
    else:
        break



