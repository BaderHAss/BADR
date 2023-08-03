import tkinter as tk
import random

# Constants
DIFFICULTY_LEVELS = {
    "Easy": {"min_value": 1, "max_value": 10, "color": "green"},
    "Medium": {"min_value": 10, "max_value": 100, "color": "yellow"},
    "Hard": {"min_value": 100, "max_value": 1000, "color": "blue"}
}

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
        self.difficulty = ""
        self.questions = []
        self.current_question_index = 0
        self.score = 0
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    
    def generate_questions(self, num_questions):
        self.questions = []
        for i in range(num_questions):
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
    
    def is_game_over(self):
        return self.current_question_index >= len(self.questions)

# GUI class for the math game
class MathGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.game = MathGame()
        self.root.title("Quiz Time")
        self.title_label = tk.Label(self.root, text="Quiz Time", font=("Helvetica", 20, "bold"))
        self.difficulty_label = tk.Label(self.root, text="Select difficulty:", font=("Helvetica", 16))
        self.summary_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.home_button = tk.Button(self.root, text="Home", command=self.go_to_home, font=("Helvetica", 16))
        self.home_page = None  # Will hold the new home page window
        self.question_page = None  # Will hold the question page window

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
        self.root.configure(bg="red")
    
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
        self.display_question()
    
    def display_question(self):
        if self.question_page:
            self.question_page.destroy()  # Destroy the previous question page if exists

        self.question_page = tk.Toplevel(self.root)
        self.question_page.title("Question Page")
        self.question_page.geometry("600x400")
        self.question_page.configure(bg=DIFFICULTY_LEVELS[self.game.difficulty]["color"])

        question = self.game.get_current_question()
        question_text = question.get_question()
        self.question_label = tk.Label(self.question_page, text=question_text, font=("Helvetica", 16))
        self.question_label.pack(pady=10)
        
        self.choices_var = tk.IntVar()
        self.choices_var.set(-1)  # Initialize to an invalid value
        choices = question.get_choices()
        self.choices_buttons = []
        for i in range(4):
            button = tk.Radiobutton(self.question_page, text=str(choices[i]), variable=self.choices_var, value=i, font=("Helvetica", 14))
            self.choices_buttons.append(button)
            button.pack(pady=5)
        
        self.next_button = tk.Button(self.question_page, text="Next", command=self.check_answer_and_next, font=("Helvetica", 16))
        self.next_button.pack(pady=5)
        
        if self.game.current_question_index == 0:
            self.back_button = tk.Button(self.question_page, text="Back", command=self.go_to_home, font=("Helvetica", 16))
        else:
            self.back_button = tk.Button(self.question_page, text="Back", command=self.prev_question, font=("Helvetica", 16))
        self.back_button.pack(pady=5)
    
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
            for button in self.choices_buttons:
                button.pack_forget()
            self.question_label.pack_forget()
            self.next_button.pack_forget()
            self.back_button.pack_forget()
            self.display_question()
    
    def prev_question(self):
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
        self.retry_button = tk.Button(self.question_page, text="Retry", command=self.retry_game, font=("Helvetica", 16))
        self.retry_button.pack(pady=5)
        self.home_button.pack(pady=5)
    
    def retry_game(self):
        self.summary_label.pack_forget()
        self.retry_button.pack_forget()
        self.home_button.pack_forget()
        self.game.score = 0
        self.game.current_question_index = 0
        self.display_question()

    def go_to_home(self):
        if self.question_page:
            self.question_page.destroy()  # Destroy the question page if exists

        if self.home_page:
            self.home_page.destroy()  # Destroy the previous home page if exists
        
        self.home_page = tk.Toplevel(self.root)
        self.home_page.title("Home Page")
        self.home_page.geometry("600x400")
        self.home_page.configure(bg="red")
        
        title_label = tk.Label(self.home_page, text="Quiz Time", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)
        
        self.difficulty_label.pack(pady=10)
        self.display_difficulty_buttons()
        
        self.summary_label.pack_forget()
        self.retry_button.pack_forget()
        self.home_button.pack_forget()
        self.game.difficulty = ""
    
# Main program
if __name__ == "__main__":
    game_gui = MathGameGUI()
    game_gui.start()



