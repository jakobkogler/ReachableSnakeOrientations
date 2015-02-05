from PIL import Image, ImageDraw

GRID_SIZE = 15
LINE_WIDTH = 2

def visual(points, file_name):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    min_x, max_x, min_y, max_y = -6, 6, -6, 6
    width = max_x - min_x + 2
    height = max_y - min_y + 2
    #points = [(x - min_x, y - min_y) for (x, y) in points]
    points = [(x + 6, y + 6) for (x, y) in points]
    im = Image.new("RGB", (GRID_SIZE*width, GRID_SIZE*height), "white")
    draw = ImageDraw.Draw(im)
    for x in range(1,width):
        for i in range(LINE_WIDTH):
            draw.line([GRID_SIZE*x+i,0,GRID_SIZE*x+i,im.size[1]], fill=(0,0,0))
    for y in range(1,height):
        for j in range(LINE_WIDTH):
            draw.line([0,GRID_SIZE*y+j,im.size[0],GRID_SIZE*y+j], fill=(0,0,0))
    for ((x1, y1), (x2, y2)) in zip(points, points[1:]):
        draw.line([(x1+1)*GRID_SIZE, (y1+1)*GRID_SIZE, (x2+1)*GRID_SIZE, (y2+1)*GRID_SIZE], fill=(255,0,0), width=3)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(file_name)
