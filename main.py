import tkinter as tk
import random
import json
import os

class MathChallengeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Challenge Adventure")
        self.username = ""
        self.score = 0
        self.time_left = 60  # Time for each challenge in seconds
        self.scores_file = "top_scores.json"
        self.top_scores = self.load_top_scores()
        self.problem_type = "addition"  # Default problem type
        
        self.create_widgets()
        self.prompt_username()  # Prompt username at the beginning

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Solve the Math Problem!", font=("Helvetica", 16))
        self.label.pack(pady=20)
        
        self.problem_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.problem_label.pack(pady=10)
        
        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)
        
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=10)

        self.time_label = tk.Label(self.root, text="Time Left: 60s", font=("Helvetica", 12))
        self.time_label.pack(pady=10)
        
        self.status_bar = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.status_bar.pack(pady=10)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.prompt_problem_type)
        self.new_game_button.pack(pady=10)

    def prompt_username(self):
        self.username_prompt = tk.Toplevel(self.root)
        self.username_prompt.title("Enter Username")
        self.username_prompt.geometry("300x150")
        self.username_prompt.transient(self.root)
        self.username_prompt.grab_set()
        self.username_prompt.focus_set()
        self.username_prompt.lift()

        tk.Label(self.username_prompt, text="Enter your username:").pack(pady=10)
        self.username_entry = tk.Entry(self.username_prompt, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", self.set_username)
        
        submit_button = tk.Button(self.username_prompt, text="Submit", command=self.set_username)
        submit_button.pack(pady=10)

    def set_username(self, event=None):
        self.username = self.username_entry.get()
        if self.username:  # Ensure username is not empty
            self.username_prompt.destroy()
            self.prompt_problem_type()

    def prompt_problem_type(self):
        self.problem_type_prompt = tk.Toplevel(self.root)
        self.problem_type_prompt.title("Choose Problem Type")
        self.problem_type_prompt.geometry("300x200")
        self.problem_type_prompt.transient(self.root)
        self.problem_type_prompt.grab_set()
        self.problem_type_prompt.focus_set()
        self.problem_type_prompt.lift()

        tk.Label(self.problem_type_prompt, text="Choose Problem Type:").pack(pady=10)
        
        addition_button = tk.Button(self.problem_type_prompt, text="Addition and Subtraction", command=lambda: self.set_problem_type("addition_subtraction"))
        addition_button.pack(pady=10)

        multiplication_button = tk.Button(self.problem_type_prompt, text="Multiplication", command=lambda: self.set_problem_type("multiplication"))
        multiplication_button.pack(pady=10)

    def set_problem_type(self, problem_type):
        self.problem_type = problem_type
        self.problem_type_prompt.destroy()
        self.start_game()

    def start_game(self):
        self.score = 0
        self.time_left = 60
        self.score_label.config(text=f"Score: {self.score}")
        self.time_label.config(text=f"Time Left: {self.time_left}s")
        self.status_bar.config(text="")
        self.answer_entry.config(state=tk.NORMAL)
        self.next_problem()
        self.update_time()
        self.answer_entry.focus_set()  # Focus the answer entry field

    def next_problem(self):
        if self.problem_type == "multiplication":
            num1 = random.choice([random.randint(1, 9), 10, 11])
            num2 = random.randint(1, 9)
            operation = random.choice(["multiply","missing_1","missing_2"])
            if operation == "multiply":
                self.correct_answer = num1 * num2
                self.problem_label.config(text=f"{num1} * {num2} = ?")
            elif operation == "missing_1":
                self.correct_answer = num1
                self.problem_label.config(text=f"? * {num2} = {num1 * num2}")
            elif operation == "missing_2":
                self.correct_answer = num2
                self.problem_label.config(text=f"{num1} * ? = {num1 * num2}")
        else:  # addition_subtraction
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = random.choice(["addition", "subtraction", "missing_addition", "missing_subtraction"])
            
            if operation == "addition":
                self.correct_answer = num1 + num2
                self.problem_label.config(text=f"{num1} + {num2} = ?")
            elif operation == "subtraction":
                if num1 < num2:  # Ensure no negative answers
                    num1, num2 = num2, num1
                self.correct_answer = num1 - num2
                self.problem_label.config(text=f"{num1} - {num2} = ?")
            elif operation == "missing_addition":
                self.correct_answer = num1
                self.problem_label.config(text=f"? + {num2} = {num1 + num2}")
            elif operation == "missing_subtraction":
                self.correct_answer = num1
                self.problem_label.config(text=f"{num1 + num2} - ? = {num2}")

        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.answer_entry.focus_set()  # Ensure focus is set to the answer entry field

    def check_answer(self, event=None):
        try:
            answer = int(self.answer_entry.get())
            if answer == self.correct_answer:
                self.score += 1
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                self.feedback_label.config(text="Try Again!", fg="red")
        except ValueError:
            self.feedback_label.config(text="Please enter a number", fg="red")
        
        self.score_label.config(text=f"Score: {self.score}")
        self.update_status_bar()
        self.next_problem()

    def update_time(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_time)
        else:
            self.end_game()

    def update_status_bar(self):
        category_scores = self.top_scores.get(self.problem_type, {})
        top_scores = sorted(category_scores.values(), reverse=True)[:10]
        if top_scores:
            top_score = top_scores[0]
            self.status_bar.config(text=f"Your Score: {self.score}, Top Score: {top_score}")
        else:
            self.status_bar.config(text=f"Your Score: {self.score}")

    def end_game(self):
        self.problem_label.config(text="Game Over!")
        self.answer_entry.config(state=tk.DISABLED)
        self.feedback_label.config(text=f"Final Score: {self.score}")
        self.save_score()
        self.show_top_scores()

    def load_top_scores(self):
        if os.path.exists(self.scores_file):
            with open(self.scores_file, "r") as file:
                return json.load(file)
        else:
            return {"addition_subtraction": {}, "multiplication": {}}

    def save_score(self):
        category_scores = self.top_scores.get(self.problem_type, {})
        category_scores[self.username] = max(self.score, category_scores.get(self.username, 0))
        self.top_scores[self.problem_type] = category_scores
        
        with open(self.scores_file, "w") as file:
            json.dump(self.top_scores, file)
        
        top_scores = sorted(category_scores.values(), reverse=True)[:10]
        if self.score >= top_scores[0]:
            self.status_bar.config(text="Congrats! You're the new Champion!")
        elif self.score in top_scores[:3]:
            self.status_bar.config(text="Congrats! You're in the top three!")

    def show_top_scores(self):
        top_scores_window = tk.Toplevel(self.root)
        top_scores_window.title("Champions")
        
        tk.Label(top_scores_window, text="Champions", font=("Helvetica", 16)).pack(pady=10)
        for category, scores in self.top_scores.items():
            tk.Label(top_scores_window, text=category.capitalize(), font=("Helvetica", 14)).pack(pady=5)
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
            for username, score in sorted_scores:
                tk.Label(top_scores_window, text=f"{username}: {score}", font=("Helvetica", 14)).pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathChallengeGame(root)
    root.mainloop()
