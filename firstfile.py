
import turtle
import math
import random

# =========================
# WINDOW & SCALING
# =========================
BASE_W, BASE_H = 900, 500
TARGET_W = 1920
TARGET_H = int(TARGET_W * BASE_H / BASE_W)  # 1067 to preserve 1.8 ratio

SCALE = TARGET_W / BASE_W
SPEED_FACTOR = 1.0 / SCALE  # reduce base-step so pixel-speed stays similar

screen = turtle.Screen()
screen.setup(TARGET_W, TARGET_H)
screen.bgcolor(0, 0.9, 0.9)
screen.title("2D Village Scenery")
screen.tracer(0)

# =========================
# SCALE HELPERS
# =========================
def sx(x):
    return x * SCALE


def sy(y):
    return y * SCALE


def spt(p):
    return (sx(p[0]), sy(p[1]))


def set_pensize_scaled(t, size):
    # keep a minimum of 1 so lines remain visible
    t.pensize(max(1, int(round(size * SCALE))))


# =========================
# animation variables (keep in BASE coordinates)
# =========================
bx = 50          # boat/cloud offset
car_x = -450     # car position
windmill_angle = 0
bird_positions = [[-400, 180], [-350, 200], [-300, 190]]
wind_offset = 0
frame_count = 0


# =========================
# DRAWING PRIMITIVES (SCALED OUTPUT)
# =========================
def draw_polygon(t, points):
    """Draw a filled polygon from list of BASE points; render scaled."""
    pts = [spt(p) for p in points]
    t.penup()
    t.goto(pts[0])
    t.pendown()
    t.begin_fill()
    for p in pts[1:]:
        t.goto(p)
    t.goto(pts[0])
    t.end_fill()


def draw_circle_with_turtle(t, rx, ry, cx, cy):
    """Draw an ellipse/circle (BASE units); render scaled."""
    rx_s = rx * SCALE
    ry_s = ry * SCALE
    cx_s = sx(cx)
    cy_s = sy(cy)

    t.penup()
    t.goto(cx_s, cy_s - ry_s)
    t.pendown()
    t.begin_fill()
    for i in range(361):
        angle = math.radians(i)
        x = rx_s * math.cos(angle) + cx_s
        y = ry_s * math.sin(angle) + cy_s
        t.goto(x, y)
    t.end_fill()


def midpoint_circle_algorithm(t, radius, cx, cy):
    """Draw a filled circle using Midpoint Circle Algorithm (scaled)."""
    # Scale radius to pixel-ish units
    r = max(1, int(round(radius * SCALE)))
    cx_s = sx(cx)
    cy_s = sy(cy)

    x = 0
    y = r
    d = 1 - r

    octant_points = []
    while x <= y:
        octant_points.append((x, y))
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1

    circle_points = set()
    for px, py in octant_points:
        circle_points.add((cx_s + px, cy_s + py))
        circle_points.add((cx_s - px, cy_s + py))
        circle_points.add((cx_s + px, cy_s - py))
        circle_points.add((cx_s - px, cy_s - py))
        circle_points.add((cx_s + py, cy_s + px))
        circle_points.add((cx_s - py, cy_s + px))
        circle_points.add((cx_s + py, cy_s - px))
        circle_points.add((cx_s - py, cy_s - px))

    sorted_points = sorted(
        circle_points,
        key=lambda p: math.atan2(p[1] - cy_s, p[0] - cx_s)
    )

    if sorted_points:
        t.penup()
        t.goto(sorted_points[0])
        t.pendown()
        t.begin_fill()
        for p in sorted_points:
            t.goto(p)
        t.goto(sorted_points[0])
        t.end_fill()


def dda_line(t, x1, y1, x2, y2):
    """Draw a line using DDA algorithm (BASE units); render scaled."""
    # scale endpoints
    x1, y1 = sx(x1), sy(y1)
    x2, y2 = sx(x2), sy(y2)

    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        return

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1
    t.penup()
    t.goto(x, y)
    t.pendown()

    for _ in range(steps + 1):
        t.goto(x, y)
        x += x_inc
        y += y_inc


def draw_sun_rays(t, cx, cy, inner_radius, outer_radius, num_rays):
    """Draw sun rays using DDA line drawing algorithm."""
    t.color(255/255, 215/255, 0)
    set_pensize_scaled(t, 2)

    for i in range(num_rays):
        angle = (360 / num_rays) * i
        rad = math.radians(angle)

        x1 = cx + inner_radius * math.cos(rad)
        y1 = cy + inner_radius * math.sin(rad)
        x2 = cx + outer_radius * math.cos(rad)
        y2 = cy + outer_radius * math.sin(rad)

        dda_line(t, x1, y1, x2, y2)

    set_pensize_scaled(t, 1)


# =========================
# PERSISTENT TURTLES (LAYERS)
# =========================
background_turtle = turtle.Turtle(); background_turtle.hideturtle(); background_turtle.speed(0)
bridge_turtle = turtle.Turtle(); bridge_turtle.hideturtle(); bridge_turtle.speed(0)
boat_turtle = turtle.Turtle(); boat_turtle.hideturtle(); boat_turtle.speed(0)
cloud_turtle = turtle.Turtle(); cloud_turtle.hideturtle(); cloud_turtle.speed(0)
car_turtle = turtle.Turtle(); car_turtle.hideturtle(); car_turtle.speed(0)
windmill_turtle = turtle.Turtle(); windmill_turtle.hideturtle(); windmill_turtle.speed(0)
bird_turtle = turtle.Turtle(); bird_turtle.hideturtle(); bird_turtle.speed(0)
foreground_turtle = turtle.Turtle(); foreground_turtle.hideturtle(); foreground_turtle.speed(0)


# =========================
# SCENE OBJECTS (ORIGINAL CONTENT)
# =========================
def draw_boat_with_turtle(t, offset):
    t.color(0, 0, 0)
    t.penup()
    t.goto(sx(75 + offset), sy(-30))
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, -30), (175 + offset, 0), (50 + offset, 0), (75 + offset, -30)]:
        t.goto(sx(point[0]), sy(point[1]))
    t.end_fill()

    t.color(205/255, 133/255, 63/255)
    t.penup()
    t.goto(sx(75 + offset), sy(0))
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, 0), (140 + offset, 30), (85 + offset, 30), (75 + offset, 0)]:
        t.goto(sx(point[0]), sy(point[1]))
    t.end_fill()

    # Mast
    t.color(160/255, 82/255, 45/255)
    t.penup()
    t.goto(sx(110 + offset), sy(30))
    t.pendown()
    t.begin_fill()
    for point in [(120 + offset, 30), (120 + offset, 60), (110 + offset, 60), (110 + offset, 30)]:
        t.goto(sx(point[0]), sy(point[1]))
    t.end_fill()

    # Curved Sail
    t.color(128/255, 0, 128/255)
    t.penup()
    t.goto(sx(120 + offset), sy(125))
    t.pendown()
    t.begin_fill()

    for i in range(11):
        t_param = i / 10
        # FIXED TYPO HERE: t_paramuhin -> t_param
        curve_x = 120 + offset + 25 * (1 - (1 - t_param) ** 2)
        curve_y = 125 - 85 * t_param
        t.goto(sx(curve_x), sy(curve_y))

    t.goto(sx(120 + offset), sy(40))
    t.goto(sx(120 + offset), sy(125))
    t.end_fill()


def draw_clouds_with_turtle(t, offset):
    t.color(1, 1, 1)

    def draw_c(rx, ry, cx, cy):
        draw_circle_with_turtle(t, rx, ry, cx, cy)

    draw_c(20, 30, 280 + offset, 220)
    draw_c(15, 20, 265 + offset, 220)
    draw_c(15, 20, 295 + offset, 220)

    draw_c(20, 30, 200 + offset, 180)
    draw_c(15, 20, 215 + offset, 180)
    draw_c(15, 20, 185 + offset, 180)

    draw_c(18, 25, -100 + offset, 210)
    draw_c(14, 18, -113 + offset, 210)
    draw_c(14, 18, -87 + offset, 210)

    draw_c(18, 25, -30 + offset, 190)
    draw_c(14, 18, -43 + offset, 190)
    draw_c(14, 18, -17 + offset, 190)


def draw_flowers():
    t = background_turtle
    flower_positions = [(-400, -200), (-350, -180), (-300, -210),
                        (-420, -160), (350, -190), (380, -170), (320, -200)]

    for fx, fy in flower_positions:
        t.color(1, 0.2, 0.2)
        for i in range(5):
            angle = i * 72
            petal_x = fx + 8 * math.cos(math.radians(angle))
            petal_y = fy + 8 * math.sin(math.radians(angle))
            draw_circle_with_turtle(t, 4, 5, petal_x, petal_y)

        t.color(1, 1, 0)
        draw_circle_with_turtle(t, 3, 3, fx, fy)


def draw_car(t, offset):
    t.color(1, 0, 0)
    draw_polygon(t, [(offset, 100), (offset + 60, 100),
                     (offset + 60, 120), (offset, 120)])

    t.color(0.8, 0, 0)
    draw_polygon(t, [(offset + 10, 120), (offset + 50, 120),
                     (offset + 45, 135), (offset + 15, 135)])

    t.color(0.6, 0.8, 1)
    draw_polygon(t, [(offset + 15, 122), (offset + 28, 122),
                     (offset + 26, 132), (offset + 17, 132)])
    draw_polygon(t, [(offset + 32, 122), (offset + 45, 122),
                     (offset + 43, 132), (offset + 34, 132)])

    t.color(0.1, 0.1, 0.1)
    draw_circle_with_turtle(t, 6, 6, offset + 15, 100)
    draw_circle_with_turtle(t, 6, 6, offset + 45, 100)


def draw_windmill(t, angle, wind_sway):
    base_x = 250
    base_y = -50 + wind_sway

    t.color(0.5, 0.3, 0.1)
    draw_polygon(t, [(base_x - 10, -100), (base_x + 10, -100),
                     (base_x + 8, base_y + 50), (base_x - 8, base_y + 50)])

    t.color(0.8, 0.8, 0.8)
    draw_circle_with_turtle(t, 15, 15, base_x, base_y + 50)

    t.color(1, 1, 1)
    for i in range(4):
        blade_angle = angle + i * 90
        rad = math.radians(blade_angle)

        x1 = base_x + 5 * math.cos(rad)
        y1 = base_y + 50 + 5 * math.sin(rad)
        x2 = base_x + 35 * math.cos(rad)
        y2 = base_y + 50 + 35 * math.sin(rad)

        t.penup(); t.goto(sx(x1), sy(y1)); t.pendown();
        t.begin_fill()

        perpendicular = blade_angle + 90
        perp_rad = math.radians(perpendicular)

        pts = [
            (x1 + 3 * math.cos(perp_rad), y1 + 3 * math.sin(perp_rad)),
            (x2 + 1 * math.cos(perp_rad), y2 + 1 * math.sin(perp_rad)),
            (x2 - 1 * math.cos(perp_rad), y2 - 1 * math.sin(perp_rad)),
            (x1 - 3 * math.cos(perp_rad), y1 - 3 * math.sin(perp_rad))
        ]

        t.goto(sx(pts[0][0]), sy(pts[0][1]))
        for px, py in pts[1:]:
            t.goto(sx(px), sy(py))
        t.goto(sx(pts[0][0]), sy(pts[0][1]))
        t.end_fill()


def draw_bird(t, x, y, wing_up):
    t.color(0.2, 0.2, 0.2)
    set_pensize_scaled(t, 2)

    draw_circle_with_turtle(t, 3, 3, x, y)

    t.penup()
    if wing_up:
        t.goto(sx(x - 8), sy(y - 3))
        t.pendown()
        t.goto(sx(x), sy(y))
        t.goto(sx(x + 8), sy(y - 3))
    else:
        t.goto(sx(x - 8), sy(y + 3))
        t.pendown()
        t.goto(sx(x), sy(y))
        t.goto(sx(x + 8), sy(y + 3))

    set_pensize_scaled(t, 1)


def draw_birds_flying(t, positions, frame):
    wing_up = (frame // 5) % 2 == 0
    for pos in positions:
        draw_bird(t, pos[0], pos[1], wing_up)


# =========================
# YOUR ORIGINAL 3D COW (UNCHANGED GEOMETRY; SCALED VIA draw_polygon)
# =========================
def draw_3d_cow(t):
    base_x = 350
    base_y = -150

    white_top = (1, 1, 1)
    white_front = (0.9, 0.9, 0.9)
    white_side = (0.75, 0.75, 0.75)

    black_top = (0.2, 0.2, 0.2)
    black_front = (0.1, 0.1, 0.1)
    black_side = (0.05, 0.05, 0.05)

    pink_top = (1, 0.8, 0.8)
    pink_front = (0.95, 0.7, 0.7)
    pink_side = (0.85, 0.6, 0.6)

    brown_top = (0.6, 0.4, 0.2)
    brown_front = (0.5, 0.3, 0.15)
    brown_side = (0.4, 0.25, 0.1)

    # Back-left leg
    t.color(white_side)
    draw_polygon(t, [(base_x - 22, base_y), (base_x - 22, base_y + 30),
                     (base_x - 18, base_y + 32), (base_x - 18, base_y + 2)])
    t.color(white_front)
    draw_polygon(t, [(base_x - 18, base_y + 2), (base_x - 18, base_y + 32),
                     (base_x - 10, base_y + 32), (base_x - 10, base_y + 2)])
    t.color(white_top)
    draw_polygon(t, [(base_x - 22, base_y + 30), (base_x - 18, base_y + 32),
                     (base_x - 10, base_y + 32), (base_x - 14, base_y + 30)])

    # Back-right leg
    t.color(white_side)
    draw_polygon(t, [(base_x + 10, base_y), (base_x + 10, base_y + 30),
                     (base_x + 14, base_y + 32), (base_x + 14, base_y + 2)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 14, base_y + 2), (base_x + 14, base_y + 32),
                     (base_x + 22, base_y + 32), (base_x + 22, base_y + 2)])
    t.color(white_top)
    draw_polygon(t, [(base_x + 10, base_y + 30), (base_x + 14, base_y + 32),
                     (base_x + 22, base_y + 32), (base_x + 18, base_y + 30)])

    # Main body
    t.color(white_side)
    draw_polygon(t, [(base_x - 30, base_y + 30), (base_x - 30, base_y + 55),
                     (base_x - 20, base_y + 60), (base_x - 20, base_y + 35)])
    t.color(white_front)
    draw_polygon(t, [(base_x - 20, base_y + 35), (base_x - 20, base_y + 60),
                     (base_x + 30, base_y + 60), (base_x + 30, base_y + 35)])
    t.color(white_top)
    draw_polygon(t, [(base_x - 30, base_y + 55), (base_x - 20, base_y + 60),
                     (base_x + 30, base_y + 60), (base_x + 20, base_y + 55)])

    # Spots
    t.color(black_front)
    draw_polygon(t, [(base_x - 10, base_y + 45), (base_x - 10, base_y + 55),
                     (base_x + 2, base_y + 55), (base_x + 2, base_y + 45)])
    t.color(black_front)
    draw_polygon(t, [(base_x + 10, base_y + 38), (base_x + 10, base_y + 50),
                     (base_x + 22, base_y + 50), (base_x + 22, base_y + 38)])
    t.color(black_top)
    draw_polygon(t, [(base_x - 15, base_y + 56), (base_x - 8, base_y + 58),
                     (base_x + 0, base_y + 58), (base_x - 7, base_y + 56)])
    t.color(black_side)
    draw_polygon(t, [(base_x - 28, base_y + 40), (base_x - 28, base_y + 48),
                     (base_x - 22, base_y + 50), (base_x - 22, base_y + 42)])

    # Neck
    t.color(white_side)
    draw_polygon(t, [(base_x - 30, base_y + 55), (base_x - 30, base_y + 65),
                     (base_x - 26, base_y + 67), (base_x - 26, base_y + 57)])
    t.color(white_front)
    draw_polygon(t, [(base_x - 26, base_y + 57), (base_x - 26, base_y + 67),
                     (base_x - 18, base_y + 67), (base_x - 18, base_y + 57)])
    t.color(white_top)
    draw_polygon(t, [(base_x - 30, base_y + 65), (base_x - 26, base_y + 67),
                     (base_x - 18, base_y + 67), (base_x - 22, base_y + 65)])

    # Head
    t.color(white_side)
    draw_polygon(t, [(base_x - 45, base_y + 65), (base_x - 45, base_y + 80),
                     (base_x - 38, base_y + 83), (base_x - 38, base_y + 68)])
    t.color(white_front)
    draw_polygon(t, [(base_x - 38, base_y + 68), (base_x - 38, base_y + 83),
                     (base_x - 18, base_y + 83), (base_x - 18, base_y + 68)])
    t.color(white_top)
    draw_polygon(t, [(base_x - 45, base_y + 80), (base_x - 38, base_y + 83),
                     (base_x - 18, base_y + 83), (base_x - 25, base_y + 80)])

    t.color(black_front)
    draw_polygon(t, [(base_x - 35, base_y + 72), (base_x - 35, base_y + 80),
                     (base_x - 25, base_y + 80), (base_x - 25, base_y + 72)])

    # Snout
    t.color(pink_side)
    draw_polygon(t, [(base_x - 50, base_y + 68), (base_x - 50, base_y + 75),
                     (base_x - 46, base_y + 76), (base_x - 46, base_y + 69)])
    t.color(pink_front)
    draw_polygon(t, [(base_x - 46, base_y + 69), (base_x - 46, base_y + 76),
                     (base_x - 38, base_y + 76), (base_x - 38, base_y + 69)])
    t.color(pink_top)
    draw_polygon(t, [(base_x - 50, base_y + 75), (base_x - 46, base_y + 76),
                     (base_x - 38, base_y + 76), (base_x - 42, base_y + 75)])

    # Nostrils
    t.color(0.1, 0.05, 0.05)
    draw_polygon(t, [(base_x - 44, base_y + 72), (base_x - 44, base_y + 74),
                     (base_x - 42, base_y + 74), (base_x - 42, base_y + 72)])
    draw_polygon(t, [(base_x - 44, base_y + 70), (base_x - 44, base_y + 71.5),
                     (base_x - 42, base_y + 71.5), (base_x - 42, base_y + 70)])

    # Eyes
    t.color(0.05, 0.05, 0.05)
    draw_polygon(t, [(base_x - 36, base_y + 78), (base_x - 36, base_y + 81),
                     (base_x - 33, base_y + 81), (base_x - 33, base_y + 78)])
    draw_polygon(t, [(base_x - 24, base_y + 78), (base_x - 24, base_y + 81),
                     (base_x - 21, base_y + 81), (base_x - 21, base_y + 78)])

    # Ears
    t.color(pink_side)
    draw_polygon(t, [(base_x - 42, base_y + 83), (base_x - 44, base_y + 90),
                     (base_x - 40, base_y + 91)])
    t.color(pink_front)
    draw_polygon(t, [(base_x - 40, base_y + 83), (base_x - 40, base_y + 91),
                     (base_x - 36, base_y + 91), (base_x - 36, base_y + 83)])

    t.color(pink_front)
    draw_polygon(t, [(base_x - 22, base_y + 83), (base_x - 22, base_y + 91),
                     (base_x - 18, base_y + 91), (base_x - 18, base_y + 83)])
    t.color(pink_top)
    draw_polygon(t, [(base_x - 22, base_y + 91), (base_x - 20, base_y + 92),
                     (base_x - 18, base_y + 91)])

    # Horns
    t.color(brown_side)
    draw_polygon(t, [(base_x - 40, base_y + 85), (base_x - 39, base_y + 93),
                     (base_x - 37, base_y + 92)])
    t.color(brown_front)
    draw_polygon(t, [(base_x - 37, base_y + 85), (base_x - 37, base_y + 92),
                     (base_x - 35, base_y + 85)])

    t.color(brown_side)
    draw_polygon(t, [(base_x - 24, base_y + 85), (base_x - 23, base_y + 93),
                     (base_x - 21, base_y + 92)])
    t.color(brown_front)
    draw_polygon(t, [(base_x - 21, base_y + 85), (base_x - 21, base_y + 92),
                     (base_x - 19, base_y + 85)])

    # Front legs
    t.color(white_side)
    draw_polygon(t, [(base_x - 18, base_y), (base_x - 18, base_y + 35),
                     (base_x - 14, base_y + 37), (base_x - 14, base_y + 2)])
    t.color(white_front)
    draw_polygon(t, [(base_x - 14, base_y + 2), (base_x - 14, base_y + 37),
                     (base_x - 6, base_y + 37), (base_x - 6, base_y + 2)])
    t.color(white_top)
    draw_polygon(t, [(base_x - 18, base_y + 35), (base_x - 14, base_y + 37),
                     (base_x - 6, base_y + 37), (base_x - 10, base_y + 35)])

    t.color(white_side)
    draw_polygon(t, [(base_x + 14, base_y), (base_x + 14, base_y + 35),
                     (base_x + 18, base_y + 37), (base_x + 18, base_y + 2)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 18, base_y + 2), (base_x + 18, base_y + 37),
                     (base_x + 26, base_y + 37), (base_x + 26, base_y + 2)])
    t.color(white_top)
    draw_polygon(t, [(base_x + 14, base_y + 35), (base_x + 18, base_y + 37),
                     (base_x + 26, base_y + 37), (base_x + 22, base_y + 35)])

    # Hooves
    t.color(0.05, 0.05, 0.05)
    draw_polygon(t, [(base_x - 22, base_y), (base_x - 22, base_y + 4),
                     (base_x - 18, base_y + 5), (base_x - 18, base_y + 1)])
    draw_polygon(t, [(base_x - 18, base_y + 1), (base_x - 18, base_y + 5),
                     (base_x - 10, base_y + 5), (base_x - 10, base_y + 1)])

    draw_polygon(t, [(base_x + 10, base_y), (base_x + 10, base_y + 4),
                     (base_x + 14, base_y + 5), (base_x + 14, base_y + 1)])
    draw_polygon(t, [(base_x + 14, base_y + 1), (base_x + 14, base_y + 5),
                     (base_x + 22, base_y + 5), (base_x + 22, base_y + 1)])

    draw_polygon(t, [(base_x - 18, base_y), (base_x - 18, base_y + 4),
                     (base_x - 14, base_y + 5), (base_x - 14, base_y + 1)])
    draw_polygon(t, [(base_x - 14, base_y + 1), (base_x - 14, base_y + 5),
                     (base_x - 6, base_y + 5), (base_x - 6, base_y + 1)])

    draw_polygon(t, [(base_x + 14, base_y), (base_x + 14, base_y + 4),
                     (base_x + 18, base_y + 5), (base_x + 18, base_y + 1)])
    draw_polygon(t, [(base_x + 18, base_y + 1), (base_x + 18, base_y + 5),
                     (base_x + 26, base_y + 5), (base_x + 26, base_y + 1)])

    # Tail
    t.color(white_side)
    draw_polygon(t, [(base_x + 28, base_y + 50), (base_x + 28, base_y + 58),
                     (base_x + 30, base_y + 58), (base_x + 30, base_y + 50)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 30, base_y + 50), (base_x + 30, base_y + 58),
                     (base_x + 34, base_y + 58), (base_x + 34, base_y + 50)])

    t.color(white_side)
    draw_polygon(t, [(base_x + 32, base_y + 48), (base_x + 32, base_y + 50),
                     (base_x + 36, base_y + 48), (base_x + 36, base_y + 46)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 36, base_y + 46), (base_x + 36, base_y + 48),
                     (base_x + 40, base_y + 46), (base_x + 40, base_y + 44)])

    t.color(black_side)
    draw_polygon(t, [(base_x + 38, base_y + 40), (base_x + 38, base_y + 46),
                     (base_x + 40, base_y + 46), (base_x + 40, base_y + 40)])
    t.color(black_front)
    draw_polygon(t, [(base_x + 40, base_y + 40), (base_x + 40, base_y + 46),
                     (base_x + 45, base_y + 46), (base_x + 45, base_y + 40)])
    t.color(black_top)
    draw_polygon(t, [(base_x + 38, base_y + 46), (base_x + 40, base_y + 46),
                     (base_x + 45, base_y + 46), (base_x + 43, base_y + 46)])

    # Udder
    t.color(pink_side)
    draw_polygon(t, [(base_x + 0, base_y + 30), (base_x + 0, base_y + 38),
                     (base_x + 4, base_y + 39), (base_x + 4, base_y + 31)])
    t.color(pink_front)
    draw_polygon(t, [(base_x + 4, base_y + 31), (base_x + 4, base_y + 39),
                     (base_x + 14, base_y + 39), (base_x + 14, base_y + 31)])
    t.color(pink_top)
    draw_polygon(t, [(base_x + 0, base_y + 38), (base_x + 4, base_y + 39),
                     (base_x + 14, base_y + 39), (base_x + 10, base_y + 38)])

    t.color(pink_front)
    for teat_x in [5, 9, 13]:
        draw_polygon(t, [(base_x + teat_x, base_y + 29), (base_x + teat_x, base_y + 31),
                         (base_x + teat_x + 2, base_y + 31), (base_x + teat_x + 2, base_y + 29)])


# =========================
# BACKGROUND / BRIDGE / FOREGROUND (ORIGINAL)
# =========================
def draw_background():
    t = background_turtle
    t.clear()

    # Ground
    t.color(0, 1, 0)
    draw_polygon(t, [(-450, -250), (450, -250), (450, 50), (-450, 50)])

    # River
    t.color(100/255, 149/255, 237/255)
    draw_polygon(t, [(50, 50), (0, -100), (150, -100), (200, 50)])
    draw_polygon(t, [(50, -100), (0, -250), (150, -250), (200, -100)])
    draw_polygon(t, [(-490, -50), (-450, 50), (450, 50), (450, -50)])

    # Hills
    t.color(184/255, 134/255, 11/255)
    draw_polygon(t, [(-490, 50), (-50, 50), (-150, 200)])
    t.color(218/255, 165/255, 32/255)
    draw_polygon(t, [(-100, 50), (100, 50), (0, 200)])
    t.color(184/255, 134/255, 11/255)
    draw_polygon(t, [(50, 50), (470, 50), (150, 200)])

    # Sun
    t.color(255/255, 215/255, 0)
    midpoint_circle_algorithm(t, 27, -75, 200)
    draw_sun_rays(t, -75, 200, 32, 50, 12)

    # Flowers
    draw_flowers()

    # Road
    t.color(0.3, 0.3, 0.3)
    draw_polygon(t, [(-450, 80), (450, 80), (450, 110), (-450, 110)])

    # Road markings
    t.color(1, 1, 1)
    for i in range(-450, 450, 40):
        draw_polygon(t, [(i, 93), (i + 20, 93), (i + 20, 97), (i, 97)])


def draw_bridge():
    t = bridge_turtle
    t.clear()

    t.color(0.6, 0.4, 0.2)
    draw_polygon(t, [(30, 80), (180, 80), (180, 110), (30, 110)])

    t.color(0.4, 0.2, 0.1)
    draw_polygon(t, [(30, 110), (180, 110), (180, 115), (30, 115)])
    draw_polygon(t, [(30, 80), (180, 80), (180, 75), (30, 75)])

    for x in [50, 90, 130, 170]:
        draw_polygon(t, [(x - 3, 75), (x + 3, 75), (x + 3, 50), (x - 3, 50)])


def draw_foreground(wind_sway):
    t = foreground_turtle

    # 2nd House (right)
    t.color(210/255, 105/255, 30/255)
    draw_polygon(t, [(-150, -30), (-50, -30), (-75, 20), (-120, 20)])
    t.color(244/255, 164/255, 96/255)
    draw_polygon(t, [(-150, -80), (-65, -80), (-65, -30), (-150, -30)])
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-150, -80), (-60, -80), (-60, -90), (-150, -90)])
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-110, -80), (-85, -80), (-85, -50), (-110, -50)])

    # 1st House (left)
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-250, -30), (-115, -30), (-140, 20), (-225, 20)])
    t.color(255/255, 222/255, 173/255)
    draw_polygon(t, [(-240, -30), (-200, -30), (-225, 5)])
    t.color(255/255, 222/255, 173/255)
    draw_polygon(t, [(-240, -100), (-200, -100), (-200, -30), (-240, -30)])
    t.color(222/255, 184/255, 135/255)
    draw_polygon(t, [(-200, -100), (-125, -100), (-125, -30), (-200, -30)])
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-240, -100), (-125, -100), (-125, -110), (-240, -110)])
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-175, -100), (-155, -100), (-155, -55), (-175, -55)])
    t.color(160/255, 82/255, 45/255)
    draw_polygon(t, [(-230, -50), (-215, -50), (-215, -75), (-230, -75)])

    # Tree trunk
    t.color(139/255, 69/255, 19/255)
    draw_polygon(t, [(-200, -100), (-180, -100), (-180, 50), (-200, 50)])

    # Tree leaves
    t.color(0, 128/255, 0)
    draw_circle_with_turtle(t, 30, 40, -215 + wind_sway, 70)
    draw_circle_with_turtle(t, 30, 40, -165 + wind_sway, 70)
    draw_circle_with_turtle(t, 25, 30, -205 + wind_sway, 120)
    draw_circle_with_turtle(t, 30, 30, -180 + wind_sway, 120)
    draw_circle_with_turtle(t, 25, 30, -195 + wind_sway, 150)

    # 3D Cow
    draw_3d_cow(t)


# =========================
# ANIMATION
# =========================
def animate():
    global bx, car_x, windmill_angle, bird_positions, wind_offset, frame_count

    boat_turtle.clear()
    cloud_turtle.clear()
    car_turtle.clear()
    windmill_turtle.clear()
    bird_turtle.clear()
    foreground_turtle.clear()

    wind_offset = 3 * math.sin(frame_count * 0.05)

    # Car
    draw_car(car_turtle, car_x)

    # Boat
    draw_boat_with_turtle(boat_turtle, bx)

    # Clouds
    draw_clouds_with_turtle(cloud_turtle, bx)

    # Windmill
    draw_windmill(windmill_turtle, windmill_angle, wind_offset * 0.5)

    # Birds
    draw_birds_flying(bird_turtle, bird_positions, frame_count)

    # Foreground
    draw_foreground(wind_offset)

    # Update positions (scaled step)
    bx += 1.9 * SPEED_FACTOR
    if bx > 500:
        bx = -550

    car_x += 2 * SPEED_FACTOR
    if car_x > 500:
        car_x = -450

    windmill_angle += 3
    if windmill_angle >= 360:
        windmill_angle = 0

    # Move birds
    for bird in bird_positions:
        bird[0] += 0.5 * SPEED_FACTOR
        bird[1] += (0.2 * SPEED_FACTOR) * math.sin(frame_count * 0.1 + bird[0] * 0.01)
        if bird[0] > 500:
            bird[0] = -450
            bird[1] = random.randint(160, 220)

    frame_count += 1

    screen.update()
    screen.ontimer(animate, 20)


# =========================
# INIT & RUN
# =========================
draw_background()
draw_bridge()
animate()
screen.mainloop()
