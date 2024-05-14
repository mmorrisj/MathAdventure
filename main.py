import tkinter as tk
import random

class MathChallengeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Challenge Adventure")
        self.score = 0
        self.time_left = 60  # Time for each challenge in seconds
        
        self.create_widgets()
        self.start_game()

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

    def start_game(self):
        self.next_problem()
        self.update_time()

    def next_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.correct_answer = num1 + num2
        self.problem_label.config(text=f"{num1} + {num2} = ?")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

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
        self.next_problem()

    def update_time(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_time)
        else:
            self.end_game()

    def end_game(self):
        self.problem_label.config(text="Game Over!")
        self.answer_entry.config(state=tk.DISABLED)
        self.feedback_label.config(text=f"Final Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = MathChallengeGame(root)
    root.mainloop()
