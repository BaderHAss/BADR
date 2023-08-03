import tkinter as tk
import random

# Constants
DIFFICULTY_LEVELS = {
    "Easy": {"min_value": 1, "max_value": 10, "color": "#C1FF72"},
    "Medium": {"min_value": 10, "max_value": 50, "color": "#FFDE59"},
    "Hard": {"min_value": 50, "max_value": 100, "color": "#5CE1E6"}
}
SCORE_FILE = "scores.txt"

# Class for a math question
class MathQuestion:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.operator = "+"
        self.num1 = random.randint(DIFFICULTY_LEVELS[difficulty]["min_value"], DIFFICULTY_LEVELS[difficulty]["max_value"])
        self.num2 = random.randint(DIFFICULTY_LEVELS[difficulty]["min_value"], DIFFICULTY_LEVELS[difficulty]["max_value"])
        self.correct_answer = self.num1 + self.num2
    
    def get_question(self):
        question = f"What is {self.num1} + {self.num2}?"
        return question
    
    def get_choices(self):
        choices = [self.correct_answer]
        while len(choices) < 4:
            wrong_choice = random.randint(DIFFICULTY_LEVELS[self.difficulty]["min_value"], DIFFICULTY_LEVELS[self.difficulty]["max_value"]) + random.randint(-5, 5)
            if wrong_choice not in choices:
                choices.append(wrong_choice)
        random.shuffle(choices)
        return choices

# Class for the math game
class MathGame:
    def __init__(self):
        self.player_name = ""
        self.difficulty = ""
        self.questions = []
        self.current_question_index = 0
        self.score = 0
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def generate_questions(self, num_questions):
        self.questions = []
        for _ in range(num_questions):
            question = MathQuestion(self.difficulty)
            self.questions.append(question)
    
    def get_current_question(self):
        return self.questions[self.current_question_index]
    
    def check_answer(self, answer):
        question = self.get_current_question()
        if question.correct_answer == int(answer):
            self.score += 1
    
    def next_question(self):
        self.current_question_index += 1
    
    def prev_question(self):
        self.current_question_index -= 1
        self.current_question_index = max(self.current_question_index, 0)  # Ensure index doesn't go below 0
    
    def is_game_over(self):
        return self.current_question_index >= len(self.questions)
    
    def save_score(self):
        with open(SCORE_FILE, "a") as file:
            file.write(f"{self.player_name}: {self.score}\n")

# GUI class for the math game
class MathGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.game = MathGame()
        self.root.title("Quiz Time")
        self.title_label = tk.Label(self.root, text="Quiz Time", font=("Helvetica", 20, "bold"))
        self.difficulty_label = tk.Label(self.root, text="Select difficulty:", font=("Helvetica", 16))
        self.summary_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.is_first_question = True  # Flag to track if player is on the first question
        
        # Difficulty buttons
        self.difficulty_buttons = {}
        for difficulty in DIFFICULTY_LEVELS:
            self.difficulty_buttons[difficulty] = tk.Button(
                self.root,
                text=difficulty,
                command=lambda d=difficulty: self.start_game(d),
                font=("Helvetica", 16),
                bg=DIFFICULTY_LEVELS[difficulty]["color"],
                activebackground=DIFFICULTY_LEVELS[difficulty]["color"]
            )
        
        # Set initial background color
        self.root.configure(bg="#FF5757")
    
    def start(self):
        self.root.geometry("600x400")
        self.title_label.pack(pady=10)
        self.difficulty_label.pack(pady=10)
        self.display_difficulty_buttons()
        self.root.mainloop()
    
    def display_difficulty_buttons(self):
        for button in self.difficulty_buttons.values():
            button.pack(pady=5)
    
    def start_game(self, difficulty):
        for button in self.difficulty_buttons.values():
            button.pack_forget()
        self.difficulty_label.pack_forget()
        self.root.configure(bg=DIFFICULTY_LEVELS[difficulty]["color"])
        self.game.set_difficulty(difficulty)
        self.game.generate_questions(10)  # 10 questions
        self.game.score = 0
        self.game.current_question_index = 0
        self.is_first_question = True  # Reset the flag to True when starting a new game
        self.display_question()
    
    def display_question(self):
        # Clear the previous answer selection
        self.choices_var = tk.IntVar()
        self.choices_var.set(-1)

        question = self.game.get_current_question()
        question_number = self.game.current_question_index + 1
        question_text = f"Question number {question_number}: {question.get_question()}"
        self.question_label = tk.Label(self.root, text=question_text, font=("Helvetica", 16))
        self.question_label.pack(pady=10)
        
        choices = question.get_choices()
        self.choices_buttons = []
        for i in range(4):
            button = tk.Radiobutton(self.root, text=str(choices[i]), variable=self.choices_var, value=i, font=("Helvetica", 14))
            self.choices_buttons.append(button)
            button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.check_answer_and_next, font=("Helvetica", 16))
        self.next_button.pack(pady=5, side=tk.BOTTOM, anchor=tk.SE)  # Place at the bottom right of the page
        self.back_button = tk.Button(self.root, text="Back", command=self.prev_question, font=("Helvetica", 16))
        self.back_button.pack(pady=5, side=tk.BOTTOM, anchor=tk.SW)  # Place at the bottom left of the page
    
    def check_answer_and_next(self):
        answer = self.choices_var.get()
        if answer != -1:
            self.game.check_answer(self.choices_buttons[answer].cget("text"))
            self.next_question()
    
    def next_question(self):
        self.game.next_question()
        if self.game.is_game_over():
            self.end_game()
        else:
            self.is_first_question = False  # Player is not on the first question anymore
            for button in self.choices_buttons:
                button.pack_forget()
            self.question_label.pack_forget()
            self.next_button.pack_forget()
            self.back_button.pack_forget()
            self.display_question()
    
    def prev_question(self):
        if self.is_first_question:
            self.go_to_home()
        else:
            self.game.prev_question()
            for button in self.choices_buttons:
                button.pack_forget()
            self.question_label.pack_forget()
            self.next_button.pack_forget()
            self.back_button.pack_forget()
            self.display_question()
    
    def end_game(self):
        for button in self.choices_buttons:
            button.pack_forget()
        self.question_label.pack_forget()
        self.next_button.pack_forget()
        self.back_button.pack_forget()
        self.summary_label.configure(text=f"Game over!\nYour score: {self.game.score}/{len(self.game.questions)}")
        self.summary_label.pack(pady=10)
        self.retry_button = tk.Button(self.root, text="Retry", command=self.retry_game, font=("Helvetica", 16))
        self.retry_button.pack(pady=5)
        self.home_button = tk.Button(self.root, text="Home", command=self.go_to_home, font=("Helvetica", 16))
        self.home_button.pack(pady=5)
    
    def retry_game(self):
        self.summary_label.pack_forget()
        self.retry_button.pack_forget()
        self.home_button.pack_forget()
        self.game.score = 0
        self.game.current_question_index = 0
        self.is_first_question = True  # Reset the flag to True when starting a new game
        self.display_question()

    def go_to_home(self):
        self.summary_label.pack_forget()
        self.retry_button.pack_forget()
        self.home_button.pack_forget()
        for button in self.choices_buttons:
            button.pack_forget()
        self.question_label.pack_forget()
        self.root.configure(bg="#FF5757")  # Set the background color back to red
        self.game.difficulty = ""
        self.is_first_question = True  # Reset the flag to True when going back to the home page
        self.display_difficulty_buttons()

# Main program
if __name__ == "__main__":
    game_gui = MathGameGUI()
    game_gui.start()
