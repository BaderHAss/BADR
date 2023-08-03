import tkinter as tk
import random

# Constants
DIFFICULTY_LEVELS = {
    "Easy": {"min_value": 1, "max_value": 10},
    "Medium": {"min_value": 10, "max_value": 100},
    "Hard": {"min_value": 100, "max_value": 1000}
}
SCORE_FILE = "scores.txt"

# Class for a math question
class MathQuestion:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.operator = random.choice(["+", "-"])
        self.num1 = random.randint(DIFFICULTY_LEVELS[difficulty]["min_value"], DIFFICULTY_LEVELS[difficulty]["max_value"])
        self.num2 = random.randint(DIFFICULTY_LEVELS[difficulty]["min_value"], DIFFICULTY_LEVELS[difficulty]["max_value"])
    
    def get_question(self):
        if self.operator == "+":
            question = f"What is {self.num1} + {self.num2}?"
        else:
            question = f"What is {self.num1} - {self.num2}?"
        return question
    
    def check_answer(self, answer):
        if self.operator == "+":
            correct_answer = self.num1 + self.num2
        else:
            correct_answer = self.num1 - self.num2
        return int(answer) == correct_answer

# Class for the math game
class MathGame:
    def __init__(self):
        self.player_name = ""
        self.difficulty = ""
        self.questions = []
        self.current_question_index = 0
        self.score = 0
    
    def set_player_name(self, name):
        self.player_name = name
    
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
        if question.check_answer(answer):
            self.score += 1
    
    def next_question(self):
        self.current_question_index += 1
    
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
        self.question_label = tk.Label(self.root, text="")
        self.answer_entry = tk.Entry(self.root)
        self.result_label = tk.Label(self.root, text="")
        self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
        self.score_label = tk.Label(self.root, text="")
    
    def start(self):
        self.root.title("Math Game")
        self.root.geometry("400x200")
        
        # Player name input
        player_name_label = tk.Label(self.root, text="Enter your name:")
        player_name_label.pack()
        player_name_entry = tk.Entry(self.root)
        player_name_entry.pack()
        
        # Difficulty selection
        difficulty_label = tk.Label(self.root, text="Select difficulty:")
        difficulty_label.pack()
        difficulty_var = tk.StringVar(self.root)
        difficulty_var.set("Easy")
        difficulty_optionmenu = tk.OptionMenu(self.root, difficulty_var, *DIFFICULTY_LEVELS.keys())
        difficulty_optionmenu.pack()
        
        def start_game():
            self.game.set_player_name(player_name_entry.get())
            self.game.set_difficulty(difficulty_var.get())
            self.game.generate_questions(5)  # 5 questions
            player_name_label.pack_forget()
            player_name_entry.pack_forget()
            difficulty_label.pack_forget()
            difficulty_optionmenu.pack_forget()
            start_button.pack_forget()
            self.ask_question()
        
        # Start button
        start_button = tk.Button(self.root, text="Start", command=start_game)
        start_button.pack()
        
        self.root.mainloop()
    
    def ask_question(self):
        if not self.game.is_game_over():
            question = self.game.get_current_question()
            self.question_label.configure(text=question.get_question())
            self.question_label.pack()
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.pack()
            self.result_label.configure(text="")
            self.next_button.pack_forget()
        else:
            self.end_game()
    
    def check_answer(self):
        answer = self.answer_entry.get()
        if answer.strip().isdigit():
            self.game.check_answer(answer)
            self.result_label.configure(text="Correct!" if self.game.check_answer(answer) else "Incorrect!")
            self.result_label.pack()
            self.next_button.pack()
        else:
            self.result_label.configure(text="Please enter a valid number.")
            self.result_label.pack()
    
    def next_question(self):
        self.game.next_question()
        self.ask_question()
    
    def end_game(self):
        self.score_label.configure(text=f"Game over!\nYour score: {self.game.score}")
        self.score_label.pack()
        self.game.save_score()

# Main program
if __name__ == "__main__":
    game_gui = MathGameGUI()
    game_gui.start()
