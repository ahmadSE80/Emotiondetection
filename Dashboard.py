import tkinter as tk
from tkinter import ttk
import threading
import shared_data
import webcam_emotion
from PIL import Image, ImageTk
import cv2
import random

detection_started = False

def start_detection():

    global timer_running
    global paused
    global detection_started

    paused = False
    shared_data.paused = False

    if not timer_running:
        timer_running = True
        update_timer()

    if not detection_started:
        detection_started = True

        threading.Thread(
            target=webcam_emotion.start_detection,
            daemon=True
        ).start()



def pause_detection():

    global paused

    paused = not paused

    shared_data.paused = paused


def stop_detection():

    global timer_running
    global detection_started
    global paused

    timer_running = False
    detection_started = False
    paused = False

    shared_data.paused = False

    webcam_emotion.stop_detection()


def update_webcam():

    if paused:
        root.after(30, update_webcam)
        return

    frame = shared_data.current_frame

    if frame is not None:

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        img = Image.fromarray(frame)

        img = img.resize((650, 400))

        photo = ImageTk.PhotoImage(img)

        webcam_label.imgtk = photo
        webcam_label.configure(image=photo)

    root.after(30, update_webcam)

graph_values = []

def animate_graph():

    if paused:
        root.after(1000, animate_graph)
        return

    graph_canvas.delete("all")

    # Title
    graph_canvas.create_text(
        250,
        15,
        text="Class Engagement (%)",
        font=("Arial", 14, "bold")
    )

    # Grid + Y Labels
    for i in range(6):

        y = 280 - (i * 50)

        graph_canvas.create_line(
            50,
            y,
            450,
            y,
            fill="#dddddd"
        )

        graph_canvas.create_text(
            30,
            y,
            text=str(i * 20)
        )

    # Axes
    graph_canvas.create_line(
        50, 280,
        450, 280,
        width=2
    )

    graph_canvas.create_line(
        50, 280,
        50, 30,
        width=2
    )

    # Store latest score
    graph_values.append(
        shared_data.engagement_score
    )

    if len(graph_values) > 10:
        graph_values.pop(0)

    points = []

    for i, value in enumerate(graph_values):

        x = 50 + (i * 40)

        y = 280 - int(value * 2.2)

        points.extend([x, y])

        # Draw point
        graph_canvas.create_oval(
            x-4,
            y-4,
            x+4,
            y+4,
            fill="red"
        )

        # X labels
        graph_canvas.create_text(
            x,
            295,
            text=str(i+1),
            font=("Arial", 8)
        )

    # Dynamic color
    score = shared_data.engagement_score

    if score >= 80:
        line_color = "green"
    elif score >= 60:
        line_color = "orange"
    else:
        line_color = "red"

    # Draw line
    if len(points) >= 4:

        graph_canvas.create_line(
            points,
            fill=line_color,
            width=3,
            smooth=True
        )

    # Current score
    graph_canvas.create_text(
        380,
        40,
        text=f"Current: {score}%",
        font=("Arial", 12, "bold"),
        fill=line_color
    )

    root.after(
        1000,
        animate_graph
    )


def update_dashboard():

    if paused:
        root.after(1000, update_dashboard)
        return

    student_count = len(shared_data.students)

    student_card.config(
        text=str(student_count)
    )

    engagement_card.config(
        text=f"{shared_data.engagement_score}%"
    )

    if shared_data.engagement_score >= 80:
        mood = "Happy"

    elif shared_data.engagement_score >= 60:
        mood = "Normal"

    else:
        mood = "Low Focus"

    mood_card.config(
        text=mood
    )

    # Clear table
    for item in tree.get_children():
        tree.delete(item)

    # Insert latest students
    for row in shared_data.students:
        tree.insert("", "end", values=row)

    progress["value"] = shared_data.engagement_score

    score_label.config(
        text=f"{shared_data.engagement_score}%"
    )

    root.after(1000, update_dashboard)


def update_timer():

    global time_left
    global timer_running
    global paused

    if not timer_running:
        return

    if not paused:

        mins = time_left // 60
        secs = time_left % 60

        time_card.config(
            text=f"{mins:02d}:{secs:02d}"
        )

        time_left -= 1

        if time_left < 0:

            stop_detection()

            time_card.config(
                text="Finished"
            )

            return

    root.after(
        1000,
        update_timer
    )
    
root = tk.Tk()
root.title("AI Classroom Engagement Simulation Dashboard")
root.geometry("1400x1000")

# =========================
# SCROLLABLE WINDOW
# =========================
main_canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)

scrollable_frame = ttk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )

main_canvas.bind_all(
    "<MouseWheel>",
    _on_mousewheel
)


# =========================
# TITLE
# =========================
title = tk.Label(
    scrollable_frame,
    text="AI Classroom Engagement Simulation Dashboard",
    font=("Arial", 24, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=15,
    anchor="center"
)
title.pack(fill="x")

# =========================
# TOP CARDS
# =========================
cards_frame = tk.Frame(scrollable_frame)
cards_frame.pack(fill="x", pady=10)

student_frame = tk.LabelFrame(cards_frame, text="Students", padx=20, pady=15)
student_frame.pack(side="left", padx=10)

student_card = tk.Label(
    student_frame,
    text="0",
    font=("Arial",20,"bold")
)
student_card.pack()

engagement_frame_card = tk.LabelFrame(cards_frame, text="Engagement", padx=20, pady=15)
engagement_frame_card.pack(side="left", padx=10)

engagement_card = tk.Label(
    engagement_frame_card,
    text="0%",
    font=("Arial",20,"bold")
)
engagement_card.pack()

mood_frame = tk.LabelFrame(cards_frame, text="Mood", padx=20, pady=15)
mood_frame.pack(side="left", padx=10)

mood_card = tk.Label(
    mood_frame,
    text="Waiting...",
    font=("Arial",20,"bold")
)
mood_card.pack()

time_frame_card = tk.LabelFrame(cards_frame, text="Time Left", padx=20, pady=15)
time_frame_card.pack(side="left", padx=10)

time_card = tk.Label(
    time_frame_card,
    text="05:00",
    font=("Arial",20,"bold")
)
time_card.pack()

# =========================
# CONTROL BUTTONS
# =========================

time_left = 300
timer_running = False
paused = False

control_frame = tk.LabelFrame(
    scrollable_frame,
    text="Simulation Controls"
)
control_frame.pack(fill="x", padx=10, pady=10)

tk.Button(
    control_frame,
    text="▶ Start",
    width=15,
    height=2,
    bg="lightgreen",
    command=start_detection
).pack(side="left", padx=10, pady=10)

tk.Button(
    control_frame,
    text="⏸ Pause",
    width=15,
    height=2,
    bg="khaki",
    command=pause_detection
).pack(side="left", padx=10, pady=10)

tk.Button(
    control_frame,
    text="⏹ Stop",
    width=15,
    height=2,
    bg="salmon",
    command=stop_detection
).pack(side="left", padx=10, pady=10)

tk.Button(
    control_frame,
    text="📄 Generate Report",
    width=18,
    height=2
).pack(side="left", padx=10, pady=10)

tk.Button(
    control_frame,
    text="❌ Exit",
    width=15,
    height=2,
    command=root.destroy
).pack(side="left", padx=10, pady=10)

# =========================
# WEBCAM + GRAPH
# =========================

middle_frame = tk.Frame(scrollable_frame)
middle_frame.pack(fill="x", padx=10)

# Webcam
webcam_frame = tk.LabelFrame(
    middle_frame,
    text="Live Webcam Feed"
)
webcam_frame.pack(side="left", padx=10)

webcam_label = tk.Label(
    webcam_frame,
    bg="black"
)
webcam_label.pack()


# Graph
graph_frame = tk.LabelFrame(
    middle_frame,
    text="Live Engagement Graph"
)
graph_frame.pack(side="left", padx=10)

graph_canvas = tk.Canvas(
    graph_frame,
    width=500,
    height=330,
    bg="white"
)
graph_canvas.pack()

# X Axis
graph_canvas.create_line(
    50, 280,
    450, 280,
    width=2
)

# Y Axis
graph_canvas.create_line(
    50, 280,
    50, 30,
    width=2
)

# Sample Graph
graph_canvas.create_line(
    50, 220,
    120, 180,
    190, 120,
    260, 150,
    330, 90,
    400, 110,
    width=3,
    fill="blue",
    smooth=True
)

graph_canvas.create_text(
    250,
    20,
    text="Class Engagement",
    font=("Arial", 14, "bold")
)

# =========================
# STUDENT TABLE
# =========================
table_frame = tk.LabelFrame(
    scrollable_frame,
    text="Current Student Status"
)
table_frame.pack(fill="x", padx=10, pady=10)

columns = (
    "Student",
    "Emotion",
    "Score",
    "Status"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=6
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="x")

data = [
    ("Student 1", "Happy", "100", "Engaged"),
    ("Student 2", "Neutral", "70", "Normal"),
    ("Student 3", "Sad", "30", "Low Focus"),
    ("Student 4", "Happy", "100", "Engaged"),
    ("Student 5", "Surprise", "90", "Interested")
]

for row in data:
    tree.insert("", "end", values=row)

# =========================
# ENGAGEMENT SCORE
# =========================
engagement_frame = tk.LabelFrame(
    scrollable_frame,
    text="Class Engagement Score"
)
engagement_frame.pack(fill="x", padx=10, pady=10)

score_label = tk.Label(
    engagement_frame,
    text="0%",
    font=("Arial", 28, "bold")
)
score_label.pack()

progress = ttk.Progressbar(
    engagement_frame,
    length=600,
    mode="determinate"
)
progress["value"] = 0
progress.pack(pady=10)

tk.Label(
    engagement_frame,
    text="GOOD ENGAGEMENT",
    font=("Arial", 14, "bold")
).pack()


# =========================
# EMOTION DISTRIBUTION
# =========================
emotion_frame = tk.LabelFrame(
    scrollable_frame,
    text="Emotion Distribution"
)
emotion_frame.pack(fill="x", padx=10, pady=10)

emotions = [
    ("Happy", 40),
    ("Neutral", 25),
    ("Surprise", 15),
    ("Sad", 10),
    ("Angry", 5),
    ("Fear", 3),
    ("Disgust", 2)
]

for emotion, value in emotions:
    row = tk.Frame(emotion_frame)
    row.pack(fill="x", padx=10, pady=2)

    tk.Label(
        row,
        text=f"{emotion:10}",
        width=10,
        anchor="w"
    ).pack(side="left")

    ttk.Progressbar(
        row,
        length=400,
        value=value
    ).pack(side="left", padx=10)

    tk.Label(
        row,
        text=f"{value}%"
    ).pack(side="left")

bottom_space = tk.Frame(
    scrollable_frame,
    height=100
)
bottom_space.pack(fill="x")

update_dashboard()
update_webcam()
animate_graph()

root.mainloop()
