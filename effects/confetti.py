import random, math

#wheel store particals globally
_particles = []

def start_confetti(canvas,origin_xy,colors,count=150,duration_ms=1500):
    '''
    Docstring for start_confetti
    
    :param canvas: tkinter canvas
    :param origin_xy: tuple for explosion center
    :param colors: list of colors of confetti
    :param count: how many peices of confetti will spawn
    :param duration_ms: how long the animation lasts
    '''

    global _particles
    _particles = []
    ox,oy = origin_xy

    #per particle settings
    for _ in range(count):
        w = random.randint(6,14)
        h = random.randint(4,10)
        #random off set so it doesn't look like a single pixel explosion
        x = ox+random.randint(-8,8)
        y = oy+random.randint(-8,8)

        color = random.choice(colors)

        #create a rectangle particle
        pid = canvas.create_rectangle(x,y,x+w,y+h,fill=color,outline="")
        #choose a random direction and speed
        angle = random.uniform(0,2*math.pi)
        speed = random.uniform(4.0,12.0)

        vx = math.cos(angle)*speed
        vy = -math.sin(angle)*speed

        #random spin by changing vx over time
        spin = random.uniform(-0.15,0.15)

        #particle = [id,vx,vy,spin]
        _particles.append([pid,vx,vy,spin])

    #the total frame is based on 60 fps
    frames = max(1,int(duration_ms/16))
    _animate(canvas,frames_left=frames)



def stop_confetti(canvas):
    #we are deleting any confetti corrently on the screen
    global _particles
    for p in _particles:
        canvas.delete(p[0])
    _particles = []

def _animate(canvas,frames_left):
    #animation loop
    global _particles
    if frames_left <= 0 or not _particles:
        #clean up
        for p in _particles:
            canvas.delete(p[0])
        _particles = []
        return
    
    gravity = 0.35
    drag = 0.99

    for p in _particles:
        pid,vx,vy,spin=p
        #move particles
        canvas.move(pid,vx,vy)
        #apply physics
        vy+=gravity
        vx=(vx+spin)*drag
        vy=vy*drag

        #update
        p[1]=vx
        p[2]=vy

        #if particle falls below view delete it early
        coords = canvas.coords(pid)
        if coords:
            x1,y1,x2,y2 = coords
            if y1 > canvas.winfo_height()+50:
                canvas.delete(pid)
                p[0] = None

    #remove deleted particles
    _particles[:] = [p for p in _particles if p[0] is not None]
    #next frame
    canvas.after(16,_animate,canvas,frames_left-1)