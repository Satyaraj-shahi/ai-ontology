import tkinter as tk
import math
import random
from rdflib import Graph


# Path to OWL file
ontology_file = "geometric.owl"  # Path to your OWL file
g = Graph()
g.parse(ontology_file)

# Function to show/hide input fields based on selected shape
def update_inputs(*args):
    shape = shape_var.get()
    if shape == "Triangle":
        entry_base.grid(row=2, column=1, padx=10, pady=5)
        label_base.grid(row=2, column=0, padx=10, pady=5)
        entry_height.grid(row=3, column=1, padx=10, pady=5)
        label_height.grid(row=3, column=0, padx=10, pady=5)

        entry_side.grid_remove()
        label_side.grid_remove()
        entry_radius.grid_remove()
        label_radius.grid_remove()
    elif shape == "Square":
        entry_side.grid(row=2, column=1, padx=10, pady=5)
        label_side.grid(row=2, column=0, padx=10, pady=5)

        entry_base.grid_remove()
        label_base.grid_remove()
        entry_height.grid_remove()
        label_height.grid_remove()
        entry_radius.grid_remove()
        label_radius.grid_remove()
    elif shape == "Circle":
        entry_radius.grid(row=2, column=1, padx=10, pady=5)
        label_radius.grid(row=2, column=0, padx=10, pady=5)

        entry_base.grid_remove()
        label_base.grid_remove()
        entry_height.grid_remove()
        label_height.grid_remove()
        entry_side.grid_remove()
        label_side.grid_remove()
    else:
        # Hide all inputs if no valid shape is selected
        entry_base.grid_remove()
        label_base.grid_remove()
        entry_height.grid_remove()
        label_height.grid_remove()
        entry_side.grid_remove()
        label_side.grid_remove()
        entry_radius.grid_remove()
        label_radius.grid_remove()

# Function to calculate area
def calculate_area():
    shape = shape_var.get()
    try:
        if shape == "Triangle":
            base = float(entry_base.get())
            height = float(entry_height.get())
            result = (base * height) / 2
            output_label.config(text=f"Area of Triangle: {result:.2f}")
        elif shape == "Square":
            side = float(entry_side.get())
            result = side * side
            output_label.config(text=f"Area of Square: {result:.2f}")
        elif shape == "Circle":
            radius = float(entry_radius.get())
            result = math.pi * (radius ** 2)
            output_label.config(text=f"Area of Circle: {result:.2f}")
        else:
            output_label.config(text="Invalid Shape")
    except ValueError:
        output_label.config(text="Please enter valid numbers!")

# Function to start the quiz
def start_quiz():
    global quiz_shape, quiz_question_label, quiz_answer_entry, submit_quiz_button, quiz_feedback_label

    quiz_shape = random.choice(["Triangle", "Square", "Circle"])

    if quiz_shape == "Triangle":
        base = random.randint(1, 20)
        height = random.randint(1, 20)
        quiz_correct_answer.set((base * height) / 2)
        quiz_question_label.config(text=f"A {quiz_shape} has a base of {base} and a height of {height}. What is its area?")
    elif quiz_shape == "Square":
        side = random.randint(1, 20)
        quiz_correct_answer.set(side * side)
        quiz_question_label.config(text=f"A {quiz_shape} has a side length of {side}. What is its area?")
    elif quiz_shape == "Circle":
        radius = random.randint(1, 20)
        quiz_correct_answer.set(math.pi * (radius ** 2))
        quiz_question_label.config(text=f"A {quiz_shape} has a radius of {radius}. What is its area?")

    quiz_feedback_label.config(text="")

# Function to check the quiz answer
def check_quiz_answer():
    try:
        user_answer = float(quiz_answer_entry.get())
        correct_answer = quiz_correct_answer.get()
        if math.isclose(user_answer, correct_answer, rel_tol=1e-2):
            quiz_feedback_label.config(text="Your answer is Correct !", fg="green")
        else:
            quiz_feedback_label.config(text=f"Incorrect 'better luck next time' ! Correct answer: {correct_answer:.2f}", fg="red")
    except ValueError:
        quiz_feedback_label.config(text="Please enter a valid number!", fg="red")

# Function to display OWL content
def show_owl_data():
    try:
        # Load the OWL file
        g = Graph()
        g.parse(ontology_path, format="xml")

        # Extract triples (subject, predicate, object) from the OWL file
        owl_content = ""
        for s, p, o in g:
            owl_content += f"{s} {p} {o}\n"

        # Display OWL content in the text box
        owl_text_box.delete("1.0", tk.END)  # Clear existing text
        owl_text_box.insert(tk.END, owl_content)  # Insert OWL data

    except Exception as e:
        owl_text_box.delete("1.0", tk.END)
        owl_text_box.insert(tk.END, f"Error loading OWL file: {e}")

# GUI setup
root = tk.Tk()
root.title("Geometric Shape ITS")
root.geometry("800x600")  # Larger window size for better usability
root.configure(bg="#f0f0f0")

# Styles
button_style = {"bg": "orange", "fg": "white", "font": ("Arial", 10, "bold")}
label_style = {"bg": "#f0f0f0", "font": ("Arial", 10)}

# Dropdown for shape selection
shape_var = tk.StringVar(value="Select Shape")
shape_var.trace("w", update_inputs)  # Trace changes to the dropdown

label_select_shape = tk.Label(root, text="Select Shape:", **label_style)
label_select_shape.grid(row=0, column=0, padx=10, pady=10, sticky="e")

shape_dropdown = tk.OptionMenu(root, shape_var, "Triangle", "Square", "Circle")
shape_dropdown.config(**button_style)
shape_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Labels and input fields
label_base = tk.Label(root, text="Base:", **label_style)
entry_base = tk.Entry(root)

label_height = tk.Label(root, text="Height:", **label_style)
entry_height = tk.Entry(root)

label_side = tk.Label(root, text="Side:", **label_style)
entry_side = tk.Entry(root)

label_radius = tk.Label(root, text="Radius:", **label_style)
entry_radius = tk.Entry(root)

# Button to calculate area
calculate_button = tk.Button(root, text="Calculate", command=calculate_area, **button_style)
calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

# Output label
output_label = tk.Label(root, text="Result will be displayed here", **label_style)
output_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Quiz Section
quiz_frame = tk.Frame(root, bg="#f0f0f0")
quiz_frame.grid(row=6, column=0, columnspan=2, pady=20)

quiz_correct_answer = tk.DoubleVar()

quiz_question_label = tk.Label(quiz_frame, text="Click 'Start Quiz' to begin! ", font=("Arial", 12, "bold"), bg="#f0f0f0")
quiz_question_label.grid(row=0, column=0, columnspan=2, pady=10)

quiz_answer_entry = tk.Entry(quiz_frame)
quiz_answer_entry.grid(row=1, column=0, padx=10, pady=5)

submit_quiz_button = tk.Button(quiz_frame, text="Submit Answer", command=check_quiz_answer, **button_style)
submit_quiz_button.grid(row=1, column=1, padx=10, pady=5)

quiz_feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12), bg="#f0f0f0")
quiz_feedback_label.grid(row=2, column=0, columnspan=2, pady=10)

start_quiz_button = tk.Button(quiz_frame, text="Start Quiz", command=start_quiz, **button_style)
start_quiz_button.grid(row=3, column=0, columnspan=2, pady=10)
# Initialize by hiding all inputs
update_inputs()
root.mainloop()
