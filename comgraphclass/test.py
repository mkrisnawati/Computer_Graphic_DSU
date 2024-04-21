#import library
import pygame
import sys
import numpy as np
import math
import threading
import pygame_menu

#setting display        
width = 1200
height = 750
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Lagrange Interpolation, Bezier Curves, Cubic Hermite, and Cubic Spline Interpolation')

# Define the buttons
menu_button = pygame.Rect(1050, 35, 100, 50)
cls_button = pygame.Rect(1050, height - 80, 100, 50)

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
DARK_RED = (139,0,0)
GOLD = (178, 151, 0)
GOLDEN_BROWN = (153,101,21)
DARK_GRAY = (169,169,169)
GRAY = (128,128,128)
YELLOW = (255,255,0)
LIGHT_YELLOW = (255,255,51)
ORANGE = (255,140,0)
SILVER = (245,245,245)
CUSTOM_GRAY = (153,153,153)

#font name
font = pygame.font.SysFont("timesnewroman",19)

pts = []
t_lgr = []
knots = []
count = 0
screen.fill(SILVER)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

#pygame Menu
selector_value = 0

def do_nothing():
    pass

def set_curve(option, value):
    global selector_value

    # print("Option : ", option, " Value : ", value)
    if value == 0:
        selector_value = 0
    elif value == 1:
        selector_value = 1
    elif value == 2:
        selector_value = 2
    elif value == 3:
        selector_value = 3
    elif value == 4:
        selector_value = 4
    else:
        selector_value = 0


def select_option():
    global lagrange, bazier, cubic_hermite, cubic_spline, selector_value

    if selector_value == 0:
        print("You Select None")
        lagrange, bazier, cubic_hermite, cubic_spline = False, False, False, False
    elif selector_value == 1:
        print("You Select Lagrange Interpolation")
        lagrange, bazier, cubic_hermite, cubic_spline = True, False, False, False
    elif selector_value == 2:
        print("You Select Bezier Curves")
        lagrange, bazier, cubic_hermite, cubic_spline = False, True, False, False
    elif selector_value == 3:
        print("You Select Cubic Hermite Interpolation")
        lagrange, bazier, cubic_hermite, cubic_spline = False, False, True, False
    elif selector_value == 4:
        print("You Select Cubic Spline Interpolation")
        lagrange, bazier, cubic_hermite, cubic_spline = False, False, False, True


def open_menu(window_width, window_height):
    pymenu_font = pygame_menu.font.FONT_OPEN_SANS
    menu = pygame_menu.Menu(screen, bgfun=do_nothing,
                           window_width=width, window_height=height,
                           menu_width=int(window_width), menu_height=int(window_height),
                           font=pymenu_font, font_size=23, font_size_title=27,
                           font_color=SILVER, color_selected=DARK_RED,
                           menu_alpha=100, menu_color_title=DARK_RED, menu_color=GOLD,
                           onclose=pygame_menu.events.CLOSE,
                           title='Main Menu',
                           widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                           option_margin=19,
                           title_offsetx=4, title_offsety=4)
    menu.add_selector('Options :', [('None', 0),
                                    ('Lagrange Interpolation', 1),
                                    ('Bezier Curves', 2),
                                    ('Cubic Hermite Interpolation', 3),
                                    ('Cubic Spline Interpolation', 4)],
                      onchange=set_curve)
    menu.add_button('Select', select_option)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    return menu
##########################################################################################################


def redrawScreen(button_colour=DARK_GRAY, text_colour=YELLOW):
    pygame.draw.rect(screen, SILVER, (0, 0, width, height))
    printText('Number of points = ' + str(len(pts)), BLACK, (50, 35))

    x, y = pygame.mouse.get_pos()
    if menu_button.collidepoint(x,y):
        pygame.draw.rect(screen, CUSTOM_GRAY, menu_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, 35, 100, 50), 1)
        printText('MENU', LIGHT_YELLOW, (1080, 50))

        pygame.draw.rect(screen, GRAY, cls_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, height - 80, 100, 50), 2)
        printText('CLS', YELLOW, (1085, height - 65))
    elif cls_button.collidepoint(pt[0], pt[1]):
        pygame.draw.rect(screen, GRAY, menu_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, 35, 100, 50), 2)
        printText('MENU', YELLOW, (1080, 50))

        pygame.draw.rect(screen, CUSTOM_GRAY, cls_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, height - 80, 100, 50), 1)
        printText('CLS', LIGHT_YELLOW, (1085, height - 65))
    else:
        pygame.draw.rect(screen, GRAY, menu_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, 35, 100, 50), 2)
        printText('MENU', YELLOW, (1080, 50))

        pygame.draw.rect(screen, GRAY, cls_button, 0)
        pygame.draw.rect(screen, YELLOW, (1050, height - 80, 100, 50), 2)
        printText('CLS', YELLOW, (1085, height - 65))

    pygame.draw.line(screen, DARK_RED, [100, height-55], [950, height-55], 3)


def printText(msg, color=BLACK, pos=(10,10)):
    textSurface = font.render(msg, True, color, None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)


def drawPoint(pt, color='GREEN', thick=3):
    pygame.draw.circle(screen, color, pt, thick)


# HW2 implement drawLine with drawPoint
def draw_lagrange(color='GREEN', thick=1):
    redrawScreen()

    for t in np.arange(0, len(pts)-1, 0.01):
        f_x = np.zeros(2, dtype=np.float32)
        for i in np.arange(0, len(pts), 1):
            num, den = 1, 1
            for j in np.arange(0, len(pts), 1):
                if j!=i:
                    num = num * (t - t_lgr[j])
                    den = den * (t_lgr[i] - t_lgr[j])
            f_x = f_x + np.dot(pts[i], num/den)

            if t == 0:
                # Draw point
                pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
                # Draw t
                pygame.draw.rect(screen, GOLD, (100 + ((t_lgr[i] / t_lgr[len(t_lgr) - 1]) * 850) - margin, height - 55 - margin, 2 * margin, 2 * margin), 3)

        f_x = f_x.astype(int)
        drawPoint(f_x, color=RED, thick=1)

        f_x_sl = np.dot(-t+math.floor(t), pts[math.floor(t)]) + pts[math.floor(t)] + np.dot(t-math.floor(t), pts[math.ceil(t)])
        f_x_sl = f_x_sl.astype(int)
        drawPoint(f_x_sl, color=BLUE, thick=1)


def casteljau_cons(p_sim):
    global cas_t
    p_sim_loc = [0]

    if len(p_sim) > 2 :
        for i in np.arange(0, len(p_sim) - 2, 1):
            q_0 = np.dot((1 - cas_t), p_sim[i]) + np.dot(cas_t, p_sim[i+1])
            q_1 = np.dot((1 - cas_t), p_sim[i+1]) + np.dot(cas_t, p_sim[i+2])

            p_sim_loc[i+0] = q_0
            p_sim_loc.append(q_1)
            pygame.draw.line(screen, DARK_RED, q_0, q_1, 2)
            pygame.display.update()

        if len(p_sim_loc) >= 2:
            casteljau_cons(p_sim_loc)
    elif len(p_sim) == 2:
        q = np.dot((1 - cas_t), p_sim[0]) + np.dot(cas_t, p_sim[1])
        q = q.astype(int)
        pygame.draw.circle(screen, GOLDEN_BROWN, q, 7)
        pygame.display.update()


def nCr(n,r):
    f = math.factorial
    return f(n) / (f(r) * f(n-r))


def draw_bezier(color='GREEN', thick=1):
    redrawScreen()

    pygame.draw.rect(screen, GOLD, (100 - margin, height - 55 - margin, 2 * margin, 2 * margin), 3)
    pygame.draw.rect(screen, GOLD, (950 - margin, height - 55 - margin, 2 * margin, 2 * margin), 3)


    n = len(pts)
    for t in np.arange(0, 1, 0.005):
        b_z  = np.zeros(2, dtype=np.float32)
        for i in np.arange(0, n, 1):
            if n > 2:
                b_z = b_z + np.dot(nCr(n-1, i)*((1-t)**(n-1-i))*(t**i),pts[i])

            if i < n-1:
                b_z_sl = np.dot((1-t),pts[i]) + np.dot(t,pts[i+1])
                b_z_sl = b_z_sl.astype(int)
                drawPoint(b_z_sl, color=BLUE, thick=1)

            # Draw point
            if t==0:
                pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)

        b_z = b_z.astype(int)
        drawPoint(b_z, color=RED, thick=1)


def draw_cubicHerimte(color='GREEN', thick=1, const=0.5):
    redrawScreen()

    n = len(pts)
    npa = np.asarray(pts, dtype=np.float32)
    for t in np.arange(0, 1, 0.005):
        h1 = (2 * (t ** 3)) - (3 * (t ** 2)) + 1
        h2 = (-2 * (t ** 3)) + (3 * (t ** 2))
        h3 = (t ** 3) - (2 * (t ** 2)) + t
        h4 = (t ** 3) - (t ** 2)
        for i in np.arange(0, n-1, 1):
            if n>2:
                if i == 0:
                    tan_pt2 = npa[i + 2] - npa[i]
                    tan1 = np.zeros(2, dtype=np.float32)
                    tan2 = np.dot(const, tan_pt2)
                elif i > 0 and i < n-2:
                    tan_pt1 = npa[i + 1] - npa[i - 1]
                    tan_pt2 = npa[i + 2] - npa[i]
                    tan1 = np.dot(const,tan_pt1)
                    tan2 = np.dot(const,tan_pt2)
                else:
                    tan_pt1 = npa[i + 1] - npa[i - 1]
                    tan1 = np.dot(const, tan_pt1)
                    tan2 = np.zeros(2, dtype=np.float32)
            else:
                tan1 = np.zeros(2, dtype=np.float32)
                tan2 = np.zeros(2, dtype=np.float32)

            c_h = np.dot(h1,pts[i]) + np.dot(h2,pts[i+1]) + np.dot(h3,tan1) + np.dot(h4,tan2)
            c_h = c_h.astype(int)
            drawPoint(c_h, color=RED, thick=1)

            # Draw point
            if t==0:
                pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
                if i==n-2:
                    pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
                    pygame.draw.rect(screen, GOLD, (pts[i+1][0] - margin, pts[i+1][1] - margin, 2 * margin, 2 * margin), 5)


def draw_cubicSpline(color='GREEN', thick=1):
    redrawScreen()

    n=len(pts)
    npa = np.asarray(pts, dtype=np.float32)

    A = np.dot(4, np.eye(n, dtype=float))
    A[0][0], A[n-1][n-1] = 2, 2

    f = np.zeros((n, 2), dtype=np.float32)
    for i in range(n):
        if i == 0:
            A[i][i + 1] = 1
            f[i] = np.dot(3, (npa[i+1]-npa[i]))
        elif i > 0 and i < n-1:
            A[i][i - 1] = 1
            A[i][i + 1] = 1
            f[i] = np.dot(3, (npa[i + 1] - npa[i-1]))
        else:
            A[i][i - 1] = 1
            f[i] = np.dot(3, (npa[i] - npa[i - 1]))

        # Draw Point
        pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)

    M = np.dot(np.linalg.inv(A),f)

    for t in np.arange(0, 1, 0.005):
        for i in range(n-1):
            a=npa[i]
            b=M[i]
            c=np.dot(3, (npa[i+1] - npa[i]))-np.dot(2, M[i]) - M[i+1]
            d=np.dot(2, (npa[i] - npa[i+1]))+M[i]+M[i+1]
            Y=a+np.dot(b,t)+np.dot(c,t**2)+np.dot(d,t**3)

            Y = Y.astype(int)
            drawPoint(Y, color=RED, thick=1)


def draw_straightLine(color='GREEN', thick=3):
    redrawScreen()

    n = len(pts)
    for t in np.arange(0, 1, 0.005):
        for i in np.arange(0, n-1, 1):
            b_z_sl = np.dot((1 - t), pts[i]) + np.dot(t, pts[i + 1])
            b_z_sl = b_z_sl.astype(int)
            drawPoint(b_z_sl, color=BLUE, thick=1)

            # Draw point
            if t==0:
                pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
                if i==n-2:
                    pygame.draw.rect(screen, GOLD, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
                    pygame.draw.rect(screen, GOLD, (pts[i+1][0] - margin, pts[i+1][1] - margin, 2 * margin, 2 * margin), 5)


def drawLine(color='GREEN', thick=1):
    if count < 2: return

    if lagrange: draw_lagrange(color, thick)
    elif bazier: draw_bezier(color, thick)
    elif cubic_hermite: draw_cubicHerimte(color, thick, const=0.7)
    elif cubic_spline: draw_cubicSpline(color, thick)
    else: draw_straightLine(BLUE, 1)


def deletePoint(pt, del_margin):
    global pts

    print('pts = ', pts, " and pt = ", pt)
    for elm in range(len(pts)):
        if (pts[elm][0] > pt[0] - del_margin and pts[elm][0] < pt[0] + del_margin) and (
                pts[elm][1] > pt[1] - del_margin and pts[elm][1] < pt[1] + del_margin):
            pts = np.delete(pts, elm, 0)
            pts = pts.tolist()
            print("I found one point and delete it, index : ", elm)

            # recreate t
            t_lgr.clear()
            for i in range(len(pts)): t_lgr.append(i)

            break
    print('After deleting it, pts = ', pts, "\n")


def movePoint(pt, move_margin):
    global move_point, tlgr_move_point, pts

    if move_point > -1:
        # Update point
        print('Index = ', move_point, ' pts = ', pts, " and pt = ", pt)
        x, y = pygame.mouse.get_pos()
        new_pt = [x, y]
        pts[move_point] = new_pt
        print('After updating it, pts = ', pts, "\n")
    elif tlgr_move_point > -1:
        print('Index = ', tlgr_move_point, ' t = ', t_lgr, " and pt = ", pt)
        # Update t
        x, y = pygame.mouse.get_pos()
        val = ((x - 100) * t_lgr[len(t_lgr) - 1]) / 850
        if val > t_lgr[tlgr_move_point - 1] and val < t_lgr[tlgr_move_point + 1]:
            print('New value : ', val)
            t_lgr[tlgr_move_point] = val
            print('After updating it, t = ', t_lgr, "\n")
    else:
        t_pos = -1
        for elm in range(len(pts)):
            # calculate position of t
            if elm > 0 and elm < len(pts)-1: # To prevent us from moving 1st and last t by letting t_pos = -1
                t_pos = 100 + ((t_lgr[elm] / t_lgr[len(t_lgr) - 1]) * 850)

            if (pts[elm][0] > pt[0] - move_margin and pts[elm][0] < pt[0] + move_margin) and (
                    pts[elm][1] > pt[1] - move_margin and pts[elm][1] < pt[1] + move_margin):
                # Update point
                x, y = pygame.mouse.get_pos()
                new_pt = [x, y]
                pts[elm] = new_pt
                move_point = elm
                print("I found one point, index : ", move_point)
                break
            elif (t_pos > pt[0] - move_margin and t_pos < pt[0] + move_margin) and (height - 55 - margin - move_margin < pt[1]):
                # Update t
                x, y = pygame.mouse.get_pos()
                t_lgr[elm] = ((x-100) * t_lgr[len(t_lgr) - 1])/850
                tlgr_move_point = elm
                print("I found one t, index : ", tlgr_move_point)
                break


# Loop until the user clicks the close button.
done = False
pressed = 0
key_pressed = 0
margin = 6
old_pressed = 0
old_button1, old_button2, old_button3 = 0, 0, 0
old_key_pressed = 0
move_point = -1
tlgr_move_point = -1
lagrange, bazier, cubic_hermite, cubic_spline = False, False, False, False

cas_t = -1

while not done:
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            key_pressed = 1
        else:
            pressed = 0
            key_pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        if menu_button.collidepoint(pt[0],pt[1]):
            menu = open_menu(window_width=590, window_height=330)
            events = pygame.event.get()
            menu.mainloop(events)
            selector_value = 0
        elif cls_button.collidepoint(pt[0], pt[1]):
            lagrange, bazier, cubic_hermite, cubic_spline = False, False, False, False
            pts.clear()
            t_lgr.clear()
        else:
            t_lgr.append(len(pts))
            pts.append(pt)
            count += 1
            pygame.draw.rect(screen, GOLD, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)
            print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
                button1) + " pressed:" + repr(pressed) + " add pts ...\n")
    elif old_pressed == -1 and pressed == 1 and old_button3 == 1 and button3 == 0 :
        # Right click to delete a point
        if len(pts) > 0:
            deletePoint(pt, 10)
        else:
            print("There is no point")
    elif (old_pressed == -1 or old_pressed == 0) and (pressed == -1 or pressed == 0) and old_button1 == 1 and button1 == 1:
        # Hold left click to move a point
        if len(pts) > 0:
            movePoint(pt, 10)
        else:
            print("There is no point")
    elif old_key_pressed == 1 and key_pressed == 0 and bazier:
        cas_t = 0
    else:
        move_point = -1
        tlgr_move_point = -1

    if cas_t >= 0 and cas_t <= 1:
        casteljau_cons(pts)
        pygame.draw.rect(screen, GOLD, (100 + (cas_t * 850) - margin, height - 55 - margin, 2 * margin, 2 * margin), 3)
        pygame.display.update()
        cas_t = cas_t + 0.05
        pygame.time.delay(70)

    if len(pts)>1:
        drawLine(BLUE, 1)
    elif len(pts) == 1:
        redrawScreen()
        pygame.draw.rect(screen, GOLD, (pts[0][0] - margin, pts[0][1] - margin, 2 * margin, 2 * margin), 5)
    else:
        redrawScreen()

    # Update the screen with what we've drawn.
    pygame.display.update()
    old_button1 = button1
    old_button2 = button2
    old_button3 = button3
    old_pressed = pressed
    old_key_pressed = key_pressed

pygame.quit()