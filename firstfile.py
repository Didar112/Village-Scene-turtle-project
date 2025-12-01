import turtle
import math

# Setup screen
screen = turtle.Screen()
screen.setup(900, 500)
screen.bgcolor(0, 0.9, 0.9)
screen.title("Village Scenery")
screen.tracer(0)  # manual updates for smooth animation

# Global variables for animation
bx = 50   # boat/cloud x offset
ax = 10   # unused, kept for compatibility

def draw_polygon(t, points):
    """Draw a filled polygon from list of points using turtle t."""
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.begin_fill()
    for point in points[1:]:
        t.goto(point)
    t.goto(points[0])
    t.end_fill()

def draw_circle_with_turtle(t, rx, ry, cx, cy):
    """Draw an ellipse/circle with specific turtle t."""
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

boat_turtle = turtle.Turtle()
boat_turtle.hideturtle()
boat_turtle.speed(0)

cloud_turtle = turtle.Turtle()
cloud_turtle.hideturtle()
cloud_turtle.speed(0)

foreground_turtle = turtle.Turtle()
foreground_turtle.hideturtle()
foreground_turtle.speed(0)

def draw_boat_with_turtle(t, offset):
    """Draw boat using a specific turtle t at horizontal offset."""
    # We don't clear here because we clear before calling this in animate
    # Boat hull (bottom)
    t.color(0, 0, 0)
    t.penup()
    t.goto(75 + offset, -30)
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, -30), (175 + offset, 0), (50 + offset, 0), (75 + offset, -30)]:
        t.goto(point)
    t.end_fill()
    
    # Boat body
    t.color(205/255, 133/255, 63/255)
    t.penup()
    t.goto(75 + offset, 0)
    t.pendown()
    t.begin_fill()
    for point in [(150 + offset, 0), (140 + offset, 30), (85 + offset, 30), (75 + offset, 0)]:
        t.goto(point)
    t.end_fill()
    
    # Mast
    t.color(160/255, 82/255, 45/255)
    t.penup()
    t.goto(110 + offset, 30)
    t.pendown()
    t.begin_fill()
    for point in [(120 + offset, 30), (120 + offset, 60), (110 + offset, 60), (110 + offset, 30)]:
        t.goto(point)
    t.end_fill()
    
    # Sail
    t.color(128/255, 0, 128/255)
    t.penup()
    t.goto(85 + offset, 40)
    t.pendown()
    t.begin_fill()
    for point in [(140 + offset, 40), (140 + offset, 125), (85 + offset, 125), (85 + offset, 40)]:
        t.goto(point)
    t.end_fill()

def draw_clouds_with_turtle(t, offset):
    """Draw clouds using a specific turtle t at horizontal offset."""
    t.clear()
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

def draw_background():
    """Draw background elements once (ground, river, hills)."""
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

    #Sun
    background_turtle.color(255/255, 215/255, 0)
    draw_circle_with_turtle(background_turtle, 25, 30, -75, 200)


def draw_foreground():
    """Draw foreground elements (houses, tree, sun) using foreground_turtle."""
    t = foreground_turtle
    # Note: we do NOT call t.clear() here because animate will clear it when redrawing.
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
    draw_circle_with_turtle(t, 30, 40, -215, 70)
    draw_circle_with_turtle(t, 30, 40, -165, 70)
    draw_circle_with_turtle(t, 25, 30, -205, 120)
    draw_circle_with_turtle(t, 30, 30, -180, 120)
    draw_circle_with_turtle(t, 25, 30, -195, 150)
    

def animate():
    """Main animation loop — draw boat between background & foreground."""
    global bx, ax

    
    boat_turtle.clear()
    
    cloud_turtle.clear()
    
    foreground_turtle.clear()

    
    draw_boat_with_turtle(boat_turtle, bx)

    
    draw_clouds_with_turtle(cloud_turtle, bx)

    
    draw_foreground()

    # Update positions
    bx += 1.9
    if bx > 500:
        bx = -550

    # commit visual update
    screen.update()
    # schedule next frame
    screen.ontimer(animate, 20)


draw_background()

draw_foreground()

# animation loop
animate()
screen.mainloop()
