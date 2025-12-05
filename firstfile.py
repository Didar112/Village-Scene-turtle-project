import turtle
import math
import random

# Setup screen
screen = turtle.Screen()
screen.setup(900, 500)
screen.bgcolor(0, 0.9, 0.9)
screen.title("Enhanced Village Scenery")
screen.tracer(0)

# Global variables for animation
bx = 50   # boat/cloud x offset
car_x = -450  # car position
windmill_angle = 0  # windmill rotation
bird_positions = [[-400, 180], [-350, 200], [-300, 190]]  # bird positions
wind_offset = 0  # wind effect for trees

def draw_polygon(t, points):
    """Draw a filled polygon from list of points."""
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.begin_fill()
    for point in points[1:]:
        t.goto(point)
    t.goto(points[0])
    t.end_fill()

def draw_circle_with_turtle(t, rx, ry, cx, cy):
    """Draw an ellipse/circle."""
    t.penup()
    t.goto(cx, cy - ry)
    t.pendown()
    t.begin_fill()
    for i in range(361):
        angle = math.radians(i)
        x = rx * math.cos(angle) + cx
        y = ry * math.sin(angle) + cy
        t.goto(x, y)
    t.end_fill()

# Create persistent turtles for each layer
background_turtle = turtle.Turtle()
background_turtle.hideturtle()
background_turtle.speed(0)

bridge_turtle = turtle.Turtle()
bridge_turtle.hideturtle()
bridge_turtle.speed(0)

boat_turtle = turtle.Turtle()
boat_turtle.hideturtle()
boat_turtle.speed(0)

cloud_turtle = turtle.Turtle()
cloud_turtle.hideturtle()
cloud_turtle.speed(0)

car_turtle = turtle.Turtle()
car_turtle.hideturtle()
car_turtle.speed(0)

windmill_turtle = turtle.Turtle()
windmill_turtle.hideturtle()
windmill_turtle.speed(0)

bird_turtle = turtle.Turtle()
bird_turtle.hideturtle()
bird_turtle.speed(0)

foreground_turtle = turtle.Turtle()
foreground_turtle.hideturtle()
foreground_turtle.speed(0)

def draw_boat_with_turtle(t, offset):
    """Draw boat at horizontal offset."""
    t.color(0, 0, 0)
    t.penup()
    t.goto(75 + offset, -30)
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, -30), (175 + offset, 0), (50 + offset, 0), (75 + offset, -30)]:
        t.goto(point)
    t.end_fill()
    
    t.color(205/255, 133/255, 63/255)
    t.penup()
    t.goto(75 + offset, 0)
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, 0), (140 + offset, 30), (85 + offset, 30), (75 + offset, 0)]:
        t.goto(point)
    t.end_fill()
    
    t.color(160/255, 82/255, 45/255)
    t.penup()
    t.goto(110 + offset, 30)
    t.pendown()
    t.begin_fill()
    for point in [(120 + offset, 30), (120 + offset, 60), (110 + offset, 60), (110 + offset, 30)]:
        t.goto(point)
    t.end_fill()
    
    t.color(128/255, 0, 128/255)
    t.penup()
    t.goto(85 + offset, 40)
    t.pendown()
    t.begin_fill()
    for point in [(140 + offset, 40), (140 + offset, 125), (85 + offset, 125), (85 + offset, 40)]:
        t.goto(point)
    t.end_fill()

def draw_clouds_with_turtle(t, offset):
    """Draw clouds at horizontal offset."""
    t.color(1, 1, 1)
    
    def draw_c(rx, ry, cx, cy):
        t.penup()
        t.goto(cx, cy - ry)
        t.pendown()
        t.begin_fill()
        for i in range(361):
            angle = math.radians(i)
            x = rx * math.cos(angle) + cx
            y = ry * math.sin(angle) + cy
            t.goto(x, y)
        t.end_fill()
    
    # 1st cloud
    draw_c(20, 30, 210 + offset, 210)
    draw_c(15, 20, 195 + offset, 210)
    draw_c(15, 20, 225 + offset, 210)
    
    # 2nd cloud
    draw_c(20, 30, 140 + offset, 170)
    draw_c(15, 20, 155 + offset, 170)
    draw_c(15, 20, 125 + offset, 170)

def draw_flowers():
    """Draw flowers on the ground."""
    t = background_turtle
    flower_positions = [(-400, -200), (-350, -180), (-300, -210), 
                       (-420, -160), (350, -190), (380, -170), (320, -200)]
    
    for fx, fy in flower_positions:
        # Flower petals (red)
        t.color(1, 0.2, 0.2)
        for i in range(5):
            angle = i * 72
            petal_x = fx + 8 * math.cos(math.radians(angle))
            petal_y = fy + 8 * math.sin(math.radians(angle))
            draw_circle_with_turtle(t, 4, 5, petal_x, petal_y)
        
        # Flower center (yellow)
        t.color(1, 1, 0)
        draw_circle_with_turtle(t, 3, 3, fx, fy)

def draw_car(t, offset):
    """Draw a moving car."""
    # Car body
    t.color(1, 0, 0)
    draw_polygon(t, [(offset, 100), (offset + 60, 100), 
                     (offset + 60, 120), (offset, 120)])
    
    # Car top
    t.color(0.8, 0, 0)
    draw_polygon(t, [(offset + 10, 120), (offset + 50, 120), 
                     (offset + 45, 135), (offset + 15, 135)])
    
    # Windows
    t.color(0.6, 0.8, 1)
    draw_polygon(t, [(offset + 15, 122), (offset + 28, 122), 
                     (offset + 26, 132), (offset + 17, 132)])
    draw_polygon(t, [(offset + 32, 122), (offset + 45, 122), 
                     (offset + 43, 132), (offset + 34, 132)])
    
    # Wheels
    t.color(0.1, 0.1, 0.1)
    draw_circle_with_turtle(t, 6, 6, offset + 15, 100)
    draw_circle_with_turtle(t, 6, 6, offset + 45, 100)

def draw_windmill(t, angle, wind_sway):
    """Draw a spinning windmill on riverbank."""
    base_x = 250
    base_y = -50 + wind_sway
    
    # Windmill tower
    t.color(0.5, 0.3, 0.1)
    draw_polygon(t, [(base_x - 10, -100), (base_x + 10, -100), 
                     (base_x + 8, base_y + 50), (base_x - 8, base_y + 50)])
    
    # Windmill house
    t.color(0.8, 0.8, 0.8)
    draw_circle_with_turtle(t, 15, 15, base_x, base_y + 50)
    
    # Windmill blades (4 blades rotating)
    t.color(1, 1, 1)
    for i in range(4):
        blade_angle = angle + i * 90
        rad = math.radians(blade_angle)
        
        # Calculate blade endpoints
        x1 = base_x + 5 * math.cos(rad)
        y1 = base_y + 50 + 5 * math.sin(rad)
        x2 = base_x + 35 * math.cos(rad)
        y2 = base_y + 50 + 35 * math.sin(rad)
        
        # Draw blade
        t.penup()
        t.goto(x1, y1)
        t.pendown()
        t.begin_fill()
        
        # Create blade shape
        perpendicular = blade_angle + 90
        perp_rad = math.radians(perpendicular)
        
        pts = [
            (x1 + 3 * math.cos(perp_rad), y1 + 3 * math.sin(perp_rad)),
            (x2 + 1 * math.cos(perp_rad), y2 + 1 * math.sin(perp_rad)),
            (x2 - 1 * math.cos(perp_rad), y2 - 1 * math.sin(perp_rad)),
            (x1 - 3 * math.cos(perp_rad), y1 - 3 * math.sin(perp_rad))
        ]
        
        for pt in pts:
            t.goto(pt)
        t.goto(pts[0])
        t.end_fill()

def draw_bird(t, x, y, wing_up):
    """Draw a flying bird."""
    t.color(0.2, 0.2, 0.2)
    t.pensize(2)
    
    # Bird body (small circle)
    draw_circle_with_turtle(t, 3, 3, x, y)
    
    # Wings - simple V shape
    t.penup()
    if wing_up:
        # Wings up
        t.goto(x - 8, y - 3)
        t.pendown()
        t.goto(x, y)
        t.goto(x + 8, y - 3)
    else:
        # Wings down
        t.goto(x - 8, y + 3)
        t.pendown()
        t.goto(x, y)
        t.goto(x + 8, y + 3)
    
    t.pensize(1)

def draw_birds_flying(t, positions, frame):
    """Draw multiple flying birds."""
    wing_up = (frame // 5) % 2 == 0  # Flap wings every 5 frames
    
    for pos in positions:
        draw_bird(t, pos[0], pos[1], wing_up)

def draw_3d_cow(t):
    """Draw a highly realistic 3D Minecraft-style cow with isometric perspective."""
    base_x = 350
    base_y = -150
    
    # Define colors for 3D shading (light=top, medium=front, dark=side)
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
    
    # === BACK LEGS (4 rectangular prisms) ===
    # Back-left leg
    # Side face (darkest)
    t.color(white_side)
    draw_polygon(t, [(base_x - 22, base_y), (base_x - 22, base_y + 30),
                     (base_x - 18, base_y + 32), (base_x - 18, base_y + 2)])
    # Front face (medium)
    t.color(white_front)
    draw_polygon(t, [(base_x - 18, base_y + 2), (base_x - 18, base_y + 32),
                     (base_x - 10, base_y + 32), (base_x - 10, base_y + 2)])
    # Top face (lightest)
    t.color(white_top)
    draw_polygon(t, [(base_x - 22, base_y + 30), (base_x - 18, base_y + 32),
                     (base_x - 10, base_y + 32), (base_x - 14, base_y + 30)])
    
    # Back-right leg
    # Side face
    t.color(white_side)
    draw_polygon(t, [(base_x + 10, base_y), (base_x + 10, base_y + 30),
                     (base_x + 14, base_y + 32), (base_x + 14, base_y + 2)])
    # Front face
    t.color(white_front)
    draw_polygon(t, [(base_x + 14, base_y + 2), (base_x + 14, base_y + 32),
                     (base_x + 22, base_y + 32), (base_x + 22, base_y + 2)])
    # Top face
    t.color(white_top)
    draw_polygon(t, [(base_x + 10, base_y + 30), (base_x + 14, base_y + 32),
                     (base_x + 22, base_y + 32), (base_x + 18, base_y + 30)])
    
    # === MAIN BODY (large rectangular prism) ===
    # Side face (darkest) - left side
    t.color(white_side)
    draw_polygon(t, [(base_x - 30, base_y + 30), (base_x - 30, base_y + 55),
                     (base_x - 20, base_y + 60), (base_x - 20, base_y + 35)])
    # Front face (medium) - front
    t.color(white_front)
    draw_polygon(t, [(base_x - 20, base_y + 35), (base_x - 20, base_y + 60),
                     (base_x + 30, base_y + 60), (base_x + 30, base_y + 35)])
    # Top face (lightest)
    t.color(white_top)
    draw_polygon(t, [(base_x - 30, base_y + 55), (base_x - 20, base_y + 60),
                     (base_x + 30, base_y + 60), (base_x + 20, base_y + 55)])
    
    # === BLACK SPOTS ON BODY (with 3D effect) ===
    # Spot 1 on front face
    t.color(black_front)
    draw_polygon(t, [(base_x - 10, base_y + 45), (base_x - 10, base_y + 55),
                     (base_x + 2, base_y + 55), (base_x + 2, base_y + 45)])
    
    # Spot 2 on front face
    t.color(black_front)
    draw_polygon(t, [(base_x + 10, base_y + 38), (base_x + 10, base_y + 50),
                     (base_x + 22, base_y + 50), (base_x + 22, base_y + 38)])
    
    # Spot 3 on top face (lighter)
    t.color(black_top)
    draw_polygon(t, [(base_x - 15, base_y + 56), (base_x - 8, base_y + 58),
                     (base_x + 0, base_y + 58), (base_x - 7, base_y + 56)])
    
    # Spot on side face (darkest)
    t.color(black_side)
    draw_polygon(t, [(base_x - 28, base_y + 40), (base_x - 28, base_y + 48),
                     (base_x - 22, base_y + 50), (base_x - 22, base_y + 42)])
    
    # === NECK (connecting body to head) ===
    # Side face
    t.color(white_side)
    draw_polygon(t, [(base_x - 30, base_y + 55), (base_x - 30, base_y + 65),
                     (base_x - 26, base_y + 67), (base_x - 26, base_y + 57)])
    # Front face
    t.color(white_front)
    draw_polygon(t, [(base_x - 26, base_y + 57), (base_x - 26, base_y + 67),
                     (base_x - 18, base_y + 67), (base_x - 18, base_y + 57)])
    # Top face
    t.color(white_top)
    draw_polygon(t, [(base_x - 30, base_y + 65), (base_x - 26, base_y + 67),
                     (base_x - 18, base_y + 67), (base_x - 22, base_y + 65)])
    
    # === HEAD (rectangular prism) ===
    # Side face (left)
    t.color(white_side)
    draw_polygon(t, [(base_x - 45, base_y + 65), (base_x - 45, base_y + 80),
                     (base_x - 38, base_y + 83), (base_x - 38, base_y + 68)])
    # Front face
    t.color(white_front)
    draw_polygon(t, [(base_x - 38, base_y + 68), (base_x - 38, base_y + 83),
                     (base_x - 18, base_y + 83), (base_x - 18, base_y + 68)])
    # Top face
    t.color(white_top)
    draw_polygon(t, [(base_x - 45, base_y + 80), (base_x - 38, base_y + 83),
                     (base_x - 18, base_y + 83), (base_x - 25, base_y + 80)])
    
    # Black spot on head (front face)
    t.color(black_front)
    draw_polygon(t, [(base_x - 35, base_y + 72), (base_x - 35, base_y + 80),
                     (base_x - 25, base_y + 80), (base_x - 25, base_y + 72)])
    
    # === SNOUT (rectangular prism extending from head) ===
    # Side face
    t.color(pink_side)
    draw_polygon(t, [(base_x - 50, base_y + 68), (base_x - 50, base_y + 75),
                     (base_x - 46, base_y + 76), (base_x - 46, base_y + 69)])
    # Front face
    t.color(pink_front)
    draw_polygon(t, [(base_x - 46, base_y + 69), (base_x - 46, base_y + 76),
                     (base_x - 38, base_y + 76), (base_x - 38, base_y + 69)])
    # Top face
    t.color(pink_top)
    draw_polygon(t, [(base_x - 50, base_y + 75), (base_x - 46, base_y + 76),
                     (base_x - 38, base_y + 76), (base_x - 42, base_y + 75)])
    
    # Nostrils (small dark squares on front)
    t.color(0.1, 0.05, 0.05)
    draw_polygon(t, [(base_x - 44, base_y + 72), (base_x - 44, base_y + 74),
                     (base_x - 42, base_y + 74), (base_x - 42, base_y + 72)])
    draw_polygon(t, [(base_x - 44, base_y + 70), (base_x - 44, base_y + 71.5),
                     (base_x - 42, base_y + 71.5), (base_x - 42, base_y + 70)])
    
    # === EYES (small cubes) ===
    # Left eye
    t.color(0.05, 0.05, 0.05)
    draw_polygon(t, [(base_x - 36, base_y + 78), (base_x - 36, base_y + 81),
                     (base_x - 33, base_y + 81), (base_x - 33, base_y + 78)])
    # Right eye
    draw_polygon(t, [(base_x - 24, base_y + 78), (base_x - 24, base_y + 81),
                     (base_x - 21, base_y + 81), (base_x - 21, base_y + 78)])
    
    # === EARS (3D triangular prisms) ===
    # Left ear - side
    t.color(pink_side)
    draw_polygon(t, [(base_x - 42, base_y + 83), (base_x - 44, base_y + 90),
                     (base_x - 40, base_y + 91)])
    # Left ear - front
    t.color(pink_front)
    draw_polygon(t, [(base_x - 40, base_y + 83), (base_x - 40, base_y + 91),
                     (base_x - 36, base_y + 91), (base_x - 36, base_y + 83)])
    
    # Right ear - front
    t.color(pink_front)
    draw_polygon(t, [(base_x - 22, base_y + 83), (base_x - 22, base_y + 91),
                     (base_x - 18, base_y + 91), (base_x - 18, base_y + 83)])
    # Right ear - top
    t.color(pink_top)
    draw_polygon(t, [(base_x - 22, base_y + 91), (base_x - 20, base_y + 92),
                     (base_x - 18, base_y + 91)])
    
    # === HORNS (small 3D cones/pyramids) ===
    # Left horn
    t.color(brown_side)
    draw_polygon(t, [(base_x - 40, base_y + 85), (base_x - 39, base_y + 93),
                     (base_x - 37, base_y + 92)])
    t.color(brown_front)
    draw_polygon(t, [(base_x - 37, base_y + 85), (base_x - 37, base_y + 92),
                     (base_x - 35, base_y + 85)])
    
    # Right horn
    t.color(brown_side)
    draw_polygon(t, [(base_x - 24, base_y + 85), (base_x - 23, base_y + 93),
                     (base_x - 21, base_y + 92)])
    t.color(brown_front)
    draw_polygon(t, [(base_x - 21, base_y + 85), (base_x - 21, base_y + 92),
                     (base_x - 19, base_y + 85)])
    
    # === FRONT LEGS (2 rectangular prisms - closer to viewer, in front) ===
    # Front-left leg
    # Side face
    t.color(white_side)
    draw_polygon(t, [(base_x - 18, base_y), (base_x - 18, base_y + 35),
                     (base_x - 14, base_y + 37), (base_x - 14, base_y + 2)])
    # Front face
    t.color(white_front)
    draw_polygon(t, [(base_x - 14, base_y + 2), (base_x - 14, base_y + 37),
                     (base_x - 6, base_y + 37), (base_x - 6, base_y + 2)])
    # Top face
    t.color(white_top)
    draw_polygon(t, [(base_x - 18, base_y + 35), (base_x - 14, base_y + 37),
                     (base_x - 6, base_y + 37), (base_x - 10, base_y + 35)])
    
    # Front-right leg
    # Side face
    t.color(white_side)
    draw_polygon(t, [(base_x + 14, base_y), (base_x + 14, base_y + 35),
                     (base_x + 18, base_y + 37), (base_x + 18, base_y + 2)])
    # Front face
    t.color(white_front)
    draw_polygon(t, [(base_x + 18, base_y + 2), (base_x + 18, base_y + 37),
                     (base_x + 26, base_y + 37), (base_x + 26, base_y + 2)])
    # Top face
    t.color(white_top)
    draw_polygon(t, [(base_x + 14, base_y + 35), (base_x + 18, base_y + 37),
                     (base_x + 26, base_y + 37), (base_x + 22, base_y + 35)])
    
    # === HOOVES (dark blocks at bottom of legs) ===
    # Back-left hoof
    t.color(0.05, 0.05, 0.05)
    draw_polygon(t, [(base_x - 22, base_y), (base_x - 22, base_y + 4),
                     (base_x - 18, base_y + 5), (base_x - 18, base_y + 1)])
    draw_polygon(t, [(base_x - 18, base_y + 1), (base_x - 18, base_y + 5),
                     (base_x - 10, base_y + 5), (base_x - 10, base_y + 1)])
    
    # Back-right hoof
    draw_polygon(t, [(base_x + 10, base_y), (base_x + 10, base_y + 4),
                     (base_x + 14, base_y + 5), (base_x + 14, base_y + 1)])
    draw_polygon(t, [(base_x + 14, base_y + 1), (base_x + 14, base_y + 5),
                     (base_x + 22, base_y + 5), (base_x + 22, base_y + 1)])
    
    # Front-left hoof
    draw_polygon(t, [(base_x - 18, base_y), (base_x - 18, base_y + 4),
                     (base_x - 14, base_y + 5), (base_x - 14, base_y + 1)])
    draw_polygon(t, [(base_x - 14, base_y + 1), (base_x - 14, base_y + 5),
                     (base_x - 6, base_y + 5), (base_x - 6, base_y + 1)])
    
    # Front-right hoof
    draw_polygon(t, [(base_x + 14, base_y), (base_x + 14, base_y + 4),
                     (base_x + 18, base_y + 5), (base_x + 18, base_y + 1)])
    draw_polygon(t, [(base_x + 18, base_y + 1), (base_x + 18, base_y + 5),
                     (base_x + 26, base_y + 5), (base_x + 26, base_y + 1)])
    
    # === TAIL (3D segmented tail with tuft) ===
    # Tail segment 1
    t.color(white_side)
    draw_polygon(t, [(base_x + 28, base_y + 50), (base_x + 28, base_y + 58),
                     (base_x + 30, base_y + 58), (base_x + 30, base_y + 50)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 30, base_y + 50), (base_x + 30, base_y + 58),
                     (base_x + 34, base_y + 58), (base_x + 34, base_y + 50)])
    
    # Tail segment 2 (angled down)
    t.color(white_side)
    draw_polygon(t, [(base_x + 32, base_y + 48), (base_x + 32, base_y + 50),
                     (base_x + 36, base_y + 48), (base_x + 36, base_y + 46)])
    t.color(white_front)
    draw_polygon(t, [(base_x + 36, base_y + 46), (base_x + 36, base_y + 48),
                     (base_x + 40, base_y + 46), (base_x + 40, base_y + 44)])
    
    # Tail tuft (3D cluster at end)
    t.color(black_side)
    draw_polygon(t, [(base_x + 38, base_y + 40), (base_x + 38, base_y + 46),
                     (base_x + 40, base_y + 46), (base_x + 40, base_y + 40)])
    t.color(black_front)
    draw_polygon(t, [(base_x + 40, base_y + 40), (base_x + 40, base_y + 46),
                     (base_x + 45, base_y + 46), (base_x + 45, base_y + 40)])
    t.color(black_top)
    draw_polygon(t, [(base_x + 38, base_y + 46), (base_x + 40, base_y + 46),
                     (base_x + 45, base_y + 46), (base_x + 43, base_y + 46)])
    
    # === UDDER (3D pink block underneath body) ===
    # Side face
    t.color(pink_side)
    draw_polygon(t, [(base_x + 0, base_y + 30), (base_x + 0, base_y + 38),
                     (base_x + 4, base_y + 39), (base_x + 4, base_y + 31)])
    # Front face
    t.color(pink_front)
    draw_polygon(t, [(base_x + 4, base_y + 31), (base_x + 4, base_y + 39),
                     (base_x + 14, base_y + 39), (base_x + 14, base_y + 31)])
    # Top face
    t.color(pink_top)
    draw_polygon(t, [(base_x + 0, base_y + 38), (base_x + 4, base_y + 39),
                     (base_x + 14, base_y + 39), (base_x + 10, base_y + 38)])
    
    # Udder teats (small 3D protrusions)
    t.color(pink_front)
    for teat_x in [5, 9, 13]:
        draw_polygon(t, [(base_x + teat_x, base_y + 29), (base_x + teat_x, base_y + 31),
                         (base_x + teat_x + 2, base_y + 31), (base_x + teat_x + 2, base_y + 29)])

def draw_background():
    """Draw background elements once."""
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
    draw_circle_with_turtle(t, 25, 30, -75, 200)
    
    # Flowers
    draw_flowers()
    
    # Road
    t.color(0.3, 0.3, 0.3)
    draw_polygon(t, [(-450, 80), (450, 80), (450, 110), (-450, 110)])
    
    # Road markings (dashed line)
    t.color(1, 1, 1)
    for i in range(-450, 450, 40):
        draw_polygon(t, [(i, 93), (i + 20, 93), (i + 20, 97), (i, 97)])

def draw_bridge():
    """Draw bridge over river."""
    t = bridge_turtle
    t.clear()
    
    # Bridge deck
    t.color(0.6, 0.4, 0.2)
    draw_polygon(t, [(30, 80), (180, 80), (180, 110), (30, 110)])
    
    # Bridge railings
    t.color(0.4, 0.2, 0.1)
    draw_polygon(t, [(30, 110), (180, 110), (180, 115), (30, 115)])
    draw_polygon(t, [(30, 80), (180, 80), (180, 75), (30, 75)])
    
    # Bridge supports
    for x in [50, 90, 130, 170]:
        draw_polygon(t, [(x - 3, 75), (x + 3, 75), (x + 3, 50), (x - 3, 50)])

def draw_foreground(wind_sway):
    """Draw foreground elements."""
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
    
    # Tree leaves (with wind sway effect)
    t.color(0, 128/255, 0)
    draw_circle_with_turtle(t, 30, 40, -215 + wind_sway, 70)
    draw_circle_with_turtle(t, 30, 40, -165 + wind_sway, 70)
    draw_circle_with_turtle(t, 25, 30, -205 + wind_sway, 120)
    draw_circle_with_turtle(t, 30, 30, -180 + wind_sway, 120)
    draw_circle_with_turtle(t, 25, 30, -195 + wind_sway, 150)
    
    # Draw 3D Cow on the field
    draw_3d_cow(t)

frame_count = 0

def animate():
    """Main animation loop."""
    global bx, car_x, windmill_angle, bird_positions, wind_offset, frame_count
    
    # Clear animated layers
    boat_turtle.clear()
    cloud_turtle.clear()
    car_turtle.clear()
    windmill_turtle.clear()
    bird_turtle.clear()
    foreground_turtle.clear()
    
    # Wind effect (gentle sway)
    wind_offset = 3 * math.sin(frame_count * 0.05)
    
    # Draw animated elements
    draw_boat_with_turtle(boat_turtle, bx)
    draw_clouds_with_turtle(cloud_turtle, bx)
    draw_car(car_turtle, car_x)
    draw_windmill(windmill_turtle, windmill_angle, wind_offset * 0.5)
    draw_birds_flying(bird_turtle, bird_positions, frame_count)
    draw_foreground(wind_offset)
    
    # Update positions
    bx += 1.9
    if bx > 500:
        bx = -550
    
    car_x += 2
    if car_x > 500:
        car_x = -450
    
    windmill_angle += 3
    if windmill_angle >= 360:
        windmill_angle = 0
    
    # Move birds
    for bird in bird_positions:
        bird[0] += 0.5
        bird[1] += 0.2 * math.sin(frame_count * 0.1 + bird[0] * 0.01)
        if bird[0] > 500:
            bird[0] = -450
            bird[1] = random.randint(160, 220)
    
    frame_count += 1
    
    screen.update()
    screen.ontimer(animate, 20)

# Initialize scene
draw_background()
draw_bridge()

# Start animation
animate()
screen.mainloop()
