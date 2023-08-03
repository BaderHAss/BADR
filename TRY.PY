import tkinter as tk
import random

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Game")
        
        # Variables to store current level, question, and answer
        self.current_level = tk.StringVar()
        self.current_question = tk.StringVar()
        self.current_answer = tk.StringVar()
        
        # Create label for level selection
        level_label = tk.Label(root, text="Select Level:", font=("Arial", 18), pady=10)
        level_label.pack()
        
        # Create radio buttons for level selection
        self.level = tk.StringVar()
        easy_radio = tk.Radiobutton(root, text="Easy", variable=self.level, value="easy")
        easy_radio.pack()
        medium_radio = tk.Radiobutton(root, text="Medium", variable=self.level, value="medium")
        medium_radio.pack()
        hard_radio = tk.Radiobutton(root, text="Hard", variable=self.level, value="hard")
        hard_radio.pack()
        
        # Create label to display the question
        self.question_label = tk.Label(root, textvariable=self.current_question, font=("Arial", 24), pady=10)
        self.question_label.pack()
        
        # Create entry for the answer
        self.answer_entry = tk.Entry(root, font=("Arial", 18), textvariable=self.current_answer)
        self.answer_entry.pack()
        
        # Create button to submit the answer
        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack()
        
        # Initialize the game
        self.initialize_game()
    
    def initialize_game(self):
        # Clear previous values
        self.current_question.set("")
        self.current_answer.set("")
        
        # Disable the submit button
        self.submit_button.configure(state="disabled")
        
        # Enable level selection
        self.level.set("")
        self.level.configure(state="normal")
        
        # Clear the answer entry and set the focus
        self.answer_entry.delete(0, "end")
        self.answer_entry.focus_set()
    
    def start_game(self):
        # Disable level selection
        self.level.configure(state="disabled")
        
        # Enable the submit button
        self.submit_button.configure(state="normal")
        
        # Generate a random question based on the selected level
        level = self.level.get()
        
        if level == "easy":
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
        elif level == "medium":
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
        elif level == "hard":
            num1 = random.randint(50, 100)
            num2 = random.randint(50, 100)
        
        operator = random.choice(["+", "-"])
        
        if operator == "+":
            question = f"{num1} + {num2} ="
            answer = num1 + num2
        else:
            question = f"{num1} - {num2} ="
            answer = num1 - num2
        
        self.current_question.set(question)
        self.correct_answer = answer
    
    def check_answer(self):
        # Get the answer from the entry
        answer = self.current_answer.get()
        
        # Compare the answer with the correct answer
        if answer == str(self.correct_answer):
            result = "Correct!"
        else:
            result = "Wrong!"
        
        # Show a message box with the result
        tk.messagebox.showinfo("Result", result)
        
        # Start a new game
        self.start_game()

# Create the root window
root = tk.Tk()

# Create an instance of the MathGame class
game = MathGame(root)

# Create a button to start the game
start_button = tk.Button(root, text="Start Game", command=game.start_game)
start_button.pack()

# Run the Tkinter event loop
root.mainloop()

       

