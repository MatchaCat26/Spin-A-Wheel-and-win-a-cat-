import tkinter as tk
from tkinter import messagebox
import random
import math
from effects.sound import play_spin, stop_spin, play_win, play_button, play_confetti
from effects.confetti import start_confetti

'''
CONFIG
'''

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
WHEEL_RADIUS = min(CANVAS_WIDTH,CANVAS_HEIGHT)//2-40
WHEEL_CENTER = (CANVAS_WIDTH//2,CANVAS_HEIGHT//2+20)
BACKGROUND_COLOR = "#90E0F3"
WHEEL_OUTLINE_COLOR = "#114E4E"
POINTER_COLOR = "#B8B3E9"
COLOR_PALETTE = ["#D999B9","#D17B88","#84DCC6","#D6EDFF","#ACD7EC","#8B95C9","#478978","#A491D3","#818AA3"]



'''
APP STATE
'''

class WheelState:        #This is a constructer, something along those lines
    def __init__(self):
        self.choices = []    #list of strings
        self.color_map = {}    #the map assigns choice to color
        self.current_angle = 0.0   #degree of the angle of the wheel picker thing-a-ma-bob
        self.spinning = False   #If the wheel is spinning
        self.spin_speed = 0.0   #Degrees per frame

state = WheelState()

'''
MAIN WINDOW
'''

root = tk.Tk()
root.title("ZE WHEEL")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg = BACKGROUND_COLOR)

'''
UI LAYOUT
'''

top_frame = tk.Frame(root,bg = BACKGROUND_COLOR)
top_frame.pack(pady=10)

title_label = tk.Label(
    top_frame,
    text = "Ze Wheel",
    font = ("Oregano",24),
    fg = "white",
    bg = BACKGROUND_COLOR
)
title_label.pack()

middle_frame = tk.Frame(root,bg = BACKGROUND_COLOR)
middle_frame.pack(pady=10)

#Left Side Controls

controls_frame = tk.Frame(middle_frame, bg = BACKGROUND_COLOR)
controls_frame.pack(side = tk.LEFT, padx = 20)

entry_label = tk.Label(
    controls_frame,
    text = "Add a choice",
    font = ("Oregano",12),
    fg = "white",
    bg = BACKGROUND_COLOR
)
entry_label.pack(anchor = "w")

choice_var = tk.StringVar()
choice_entry = tk.Entry(controls_frame,textvariable = choice_var, width = 25)
choice_entry.pack(pady = 5)

def add_choice():
    text = choice_var.get().strip()
    if not text:
        return
    state.choices.append(text)
    #assign color if new
    if text not in state.color_map:
        idx = len(state.color_map)%len(COLOR_PALETTE)
        state.color_map[text] = COLOR_PALETTE[idx]
    choice_var.set("")
    refresh_choice_list()
    draw_wheel()
    play_button()
    
add_button = tk.Button(
    controls_frame,
    text = "add choice",
    command = add_choice,
    font = "Oregano",
    width = 12,
    height = 2,
    bg = "#708DA3",
    fg = "white",
    activebackground = "#233646",
    activeforeground  = "white",
    relief = "flat",
    cursor = "hand2"
)
add_button.pack(pady = 5)

choices_label = tk.Label(
    controls_frame,
    text = "current choices: ",
    font = ("Oregano", 12),
    fg = "white",
    bg = BACKGROUND_COLOR
)
choices_label.pack(anchor = "w", pady = 10)

choices_listbox = tk.Listbox(
    controls_frame,
    width = 25,
    height = 10
)
choices_listbox.pack(pady = 5)

def refresh_choice_list():
    choices_listbox.delete(0,tk.END)
    for c in state.choices:
        choices_listbox.insert(tk.END,c)

def reset_wheel():
    state.choices = []
    state.color_map = {}
    state.current_angle = 0.0
    state.spinning = False
    state.spin_speed = 0.0
    refresh_choice_list()
    draw_wheel()
    play_button()

reset_button = tk.Button(
    controls_frame,
    text = "reset",
    command = reset_wheel,
    font = "Oregano",
    width = 12,
    height = 2,
    bg = "#708DA3",
    fg = "white",
    activebackground = "#233646",
    activeforeground  = "white",
    relief = "flat",
    cursor = "hand2"
)
reset_button.pack(pady = (0,10))

#Spin Controls

def start_spin():
    if not state.choices:
        messagebox.showinfo("No choices", "add at least one choice before spinning")
        return
    if state.spinning:
        return #already spinning
    #Random initial speed
    state.spin_speed = random.uniform(15,25)  #degrees per frame
    state.spinning = True
    animate_spin()
    play_button()
    play_spin()

spin_button = tk.Button(
    controls_frame,
    text = "spin",
    command = start_spin,
    font = "Oregano",
    width = 12,
    height = 2,
    bg = "#708DA3",
    fg = "white",
    activebackground = "#233646",
    activeforeground  = "white",
    relief = "flat",
    cursor = "hand2"
)
spin_button.pack(pady = 10)

#Canvas for wheel right side
canvas_frame = tk.Frame(middle_frame,bg = BACKGROUND_COLOR)
canvas_frame.pack(side = tk.RIGHT, padx = 20)
canvas = tk.Canvas(
    canvas_frame,
    width = CANVAS_WIDTH,
    height = CANVAS_HEIGHT,
    bg = BACKGROUND_COLOR,
    highlightthickness = 0
)
canvas.pack()

'''
DRAWING FUNCTIONS
'''

def draw_label(x,y,text):
    canvas.create_text(x+1,y+1,text=text, fill = "white", font = ("Oregano", 11))
    canvas.create_text(x,y,text=text, fill = "black", font = ("Oregano", 11))

def draw_wheel():
    canvas.delete("all")
    cx,cy = WHEEL_CENTER
    r = WHEEL_RADIUS
    #background circle for wheel
    canvas.create_oval(
        cx-r,cy-r,cx+r,cy+r,
        fill = "#957FEF",
        outline = WHEEL_OUTLINE_COLOR,
        width = 5
    )

    hub_r = int(r*0.12)
    canvas.create_oval(
        cx-hub_r,
        cy-hub_r,
        cx+hub_r,
        cy+hub_r,
        fill = "black",
        outline = "white",
        width = 2
    )

    n = len(state.choices)
    if n == 0:
        draw_label(cx,cy,"Add a choice and press spin")
        draw_pointer()
        return
    slice_angle = 360/n

    #drawing slices
    for i, choice in enumerate(state.choices):
        start_angle = state.current_angle + i * slice_angle
        color = state.color_map.get(choice,"#ffffff")

        #slice arc
        canvas.create_arc(
            cx-r,cy-r,cx+r,cy+r,
            start = start_angle,
            extent = slice_angle,
            fill = color,
            outline = WHEEL_OUTLINE_COLOR
            )
        
        #text label
        mid_angle_deg = start_angle + slice_angle/2
        mid_angle_rad = math.radians(mid_angle_deg)

        text_r = r*0.5
        text_x = cx + text_r*math.cos(mid_angle_rad)
        text_y = cy - text_r*math.sin(mid_angle_rad)

        canvas.create_text(
            text_x,text_y,
            text = choice,
            fill = "black",
            font = ("Oregano",10)
        )

    draw_pointer()

def draw_pointer():
    #pointer at top center of the wheel
    cx,cy = WHEEL_CENTER
    pointer_height = 30
    pointer_width = 30

    base_y = cy - WHEEL_RADIUS-20
    tip_y = base_y + pointer_height
    left_x = cx-pointer_width//2
    right_x = cx+ pointer_width//2
    

    canvas.create_polygon(
        
        left_x,base_y,
        right_x,base_y,
        cx,tip_y,
        fill = POINTER_COLOR,
        outline = "black"
    )

'''
spin animation & winner logic
'''

def animate_spin():
    if not state.spinning:
        return
    #rotate the wheel
    state.current_angle = (state.current_angle + state.spin_speed)%360
    draw_wheel()

    #slow it down a little each frame
    state.spin_speed *= 0.99

    #if it's very slow stop and pick a winner
    if state.spin_speed < 0.5:
        state.spinning = False
        state.spin_speed = 0.0
        pick_winner()
        stop_spin()
    else:
        #schedule the next animation frame
        root.after(30,animate_spin)

    

def pick_winner():
    #figure out which slice is under the pointer and show a pop up
    if not state.choices:
        return
    n = len(state.choices)
    slice_angle = 360/n

    #our pointer is at the top of the wheel which is 90 degrees
    pointer_angle = 90

    #adjust for the wheel's current rotation
    adjusted = (pointer_angle-state.current_angle)%360

    #figure out which slice the angle falls into 
    index = int(adjusted//slice_angle)
    if index >= n:
        index = n-1
    winner = state.choices[index]
    play_win()
    play_confetti()
    messagebox.showinfo("Winner", f"the wheel chose:\n\n{winner}")





root.mainloop()
