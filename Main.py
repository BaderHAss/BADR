import tkinter as tk
import random
import tkinter.font as font
import sys

# Constants
DIFFICULTY_LEVELS = {
    "Easy": {"min_value": 1, "max_value": 10, "color": "#C1FF72"},
    "Medium": {"min_value": 10, "max_value": 50, "color": "#FFDE59"},
    "Hard": {"min_value": 50, "max_value": 100, "color": "#5CE1E6"}
}


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
    
    def is_game_over(self):
        return self.current_question_index >= len(self.questions)
    
    def save_score(self):
        with open(SCORE_FILE, "a") as file:
            file.write(f"{self.player_name}: {self.score}\n")
# Class for the Entry screen
class EntryScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Entry Screen")
        # Add a background color
        self.root.configure(bg="#5CE1E6")
        
        # Updated font and font sizes
        self.title_label = tk.Label(self.root, text="Quiz Time", font=("Arial", 36, "bold"),  bg=self.root.cget("bg"))
        self.age_label = tk.Label(self.root, text="Please enter your age:", font=("Arial", 18), bg=self.root.cget("bg"))
        self.age_entry = tk.Entry(self.root, font=("Arial", 18))
        self.continue_button = tk.Button(self.root, text="Continue", command=self.show_menu, font=("Arial", 18))
        self.age_limit_label = tk.Label(self.root, text="You must be over 4 years old to play the game.", font=("Helvetica", 16), fg="red")
        self.invalid_age_label = tk.Label(self.root, text="Invalid age. This game is designed for kids aged between 5-16 only.", font=("Helvetica", 16), fg="red")
        self.age_limit_visible = False  # Track the visibility state

    def start(self):
        self.title_label.pack(pady=20)
        self.age_label.pack(pady=10)
        self.age_entry.pack(pady=3)
        self.continue_button.pack(pady=10)
        self.age_limit_label.pack_forget()
        self.invalid_age_label.pack_forget()

    def show_menu(self):
        age = self.age_entry.get()
    
        if not age.isdigit():
            self.show_invalid_age_message()
            self.hide_age_limit_message()  # Hide the age limit message
            return
        
        age = int(age)
        
        if age <= 4:
            self.show_age_limit_message()
            self.hide_invalid_age_message()  # Hide the invalid age message
            return
        elif age > 16:
            self.show_invalid_age_message()
            self.hide_age_limit_message()  # Hide the age limit message
            return
        
        self.clear_widgets()
        self.hide_age_limit_message()
        self.hide_invalid_age_message()
        game_gui = MathGameGUI(self.root)
        game_gui.start()

    def show_invalid_age_message(self):
        self.invalid_age_label.pack(pady=10)

    def hide_invalid_age_message(self):
        if self.invalid_age_label.winfo_manager():  # Check if the label is currently packed
            self.invalid_age_label.pack_forget()

    def show_age_limit_message(self):
        self.age_limit_label.pack(pady=10)
        self.age_limit_visible = True

    def hide_age_limit_message(self):
        if self.age_limit_visible:
            self.age_limit_label.pack_forget()
            self.age_limit_visible = False

    def clear_widgets(self):
        self.age_label.pack_forget()
        self.age_entry.pack_forget()
        self.continue_button.pack_forget()
        self.title_label.pack_forget()
class MathGameGUI:
    def __init__(self, root):
        self.root = root
        self.game = MathGame()
        self.root.title("Quiz Time")
        
        
        # Updated font and font sizes
        self.title_label = tk.Label(self.root, text="Quiz Time", font=("Arial", 36, "bold"))
        self.difficulty_label = tk.Label(self.root, text="Select difficulty:", font=("Arial", 24))
        self.summary_label = tk.Label(self.root, text="", font=("Arial", 24))
        # Difficulty buttons
        self.difficulty_buttons = {}
        for difficulty in DIFFICULTY_LEVELS:
            self.difficulty_buttons[difficulty] = tk.Button(
                self.root,
                text=difficulty,
                command=lambda d=difficulty: self.start_game(d),
                font=("Arial", 20),
                bg=DIFFICULTY_LEVELS[difficulty]["color"],
                activebackground=DIFFICULTY_LEVELS[difficulty]["color"]
            )
        
        # Set initial background color
        self.root.configure(bg="#FF5757")

    def start(self):
        self.root.geometry("600x400")
        self.title_label = tk.Label(self.root, text="Quiz Time", font=("Helvetica", 40, "bold"), bg=self.root.cget("bg"))
        self.title_label.pack(pady=30)
        self.info_box = tk.Label(
            self.root,
            text="Challenge your math skills with this multiple choices math quiz",
            font=("Arial", 24),
            wraplength=350,
            bg="white"
        )
        self.info_box.place(relx=0.5, y=180, anchor="center")
        self.difficulty_label = tk.Label(self.root, text="Select difficulty:", font=("Arial", 24),bg=self.root.cget("bg"))
        self.difficulty_label.pack(pady=(130, 10))
        self.display_difficulty_buttons()
        self.root.mainloop()

    def display_difficulty_buttons(self):
        for button in self.difficulty_buttons.values():
            button.pack(pady=10)
    
    def start_game(self, difficulty):
        for button in self.difficulty_buttons.values():
            button.pack_forget()
        self.difficulty_label.pack_forget()
        self.title_label.configure(bg=DIFFICULTY_LEVELS[difficulty]["color"])
        self.hide_info_box()
        self.root.configure(bg=DIFFICULTY_LEVELS[difficulty]["color"])
        self.game.set_difficulty(difficulty)
        self.game.generate_questions(10)  # 10 questions
        self.game.score = 0
        self.game.current_question_index = 0
        self.is_first_question = True  # Reset the flag to True when starting a new game
        self.display_question()

    def hide_info_box(self):
        self.info_box.place_forget()
    
    def display_question(self):
        # Clear the previous answer selection
        self.choices_var = tk.IntVar()
        self.choices_var.set(-1)

        question = self.game.get_current_question()
        question_number = self.game.current_question_index + 1
        question_text = f"Question number {question_number}: {question.get_question()}"
        self.question_label = tk.Label(self.root, text=question_text, font=("Helvetica", 30))
        self.question_label.pack(pady=10)
        
        choices = question.get_choices()
        self.choices_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text=str(choices[i]), command=lambda i=i: self.check_answer_and_next(i), font=("Helvetica", 24))
            self.choices_buttons.append(button)
            button.pack(pady=10)
        
        self.next_button = tk.Button(self.root, text="Skip", command=self.next_question, font=("Helvetica", 24))
        self.next_button.pack(pady=2, padx=20, side="right")
        
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_game, font=("Helvetica", 24))
        self.exit_button.pack(pady=2, padx=20, side="left")
        self.info_box.pack_forget()
    
    def check_answer_and_next(self, choice_index):
        answer = self.choices_buttons[choice_index].cget("text")
        self.game.check_answer(answer)
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
            self.exit_button.pack_forget()
            self.display_question()
    
    def exit_game(self):
        self.root.destroy()
        sys.exit()

    def end_game(self):
        for button in self.choices_buttons:
         button.pack_forget()
        self.question_label.pack_forget()
        self.next_button.pack_forget()  
        self.exit_button.pack_forget()  
        self.summary_label = tk.Label(self.root, text=f"Game over!\nYour score: {self.game.score}/{len(self.game.questions)}", font=("Helvetica", 24))
        self.summary_label.pack(pady=10)
        self.retry_button = tk.Button(self.root, text="Retry", command=self.retry_game, font=("Helvetica", 24))
        self.retry_button.pack(pady=10)
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_game, font=("Helvetica", 24))
        self.exit_button.pack(pady=10)

    def retry_game(self):
        self.summary_label.pack_forget()
        self.retry_button.pack_forget()
        self.exit_button.pack_forget()
        self.game.score = 0
        self.game.current_question_index = 0
        self.is_first_question = True  # Reset the flag to True when starting a new game
        self.display_question()
# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.wm_state('zoomed')
    root.wm_attributes('-fullscreen', False)
    root.wm_attributes('-topmost', True)
    entry_screen = EntryScreen(root)
    entry_screen.start()
    root.mainloop()