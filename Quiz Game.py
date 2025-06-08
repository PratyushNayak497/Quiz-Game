import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
import random

# Define quiz questions
quiz_data = {
    "Science": [
        {
            "question": "What planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Mars"
        },
        {
            "question": "What gas do plants absorb from the atmosphere?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
            "answer": "Carbon Dioxide"
        },
        {
            "question": "What is the process by which plants convert sunlight into energy?",
            "options": ["Photosynthesis", "Respiration", "Digestion", "Evaporation"],
            "answer": "Photosynthesis"
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H2O", "CO2", "O2", "NaCl"],
            "answer": "H2O"
        },
        {
            "question": "What is the boiling point of water?",
            "options": ["100°C", "212°F", "0°C", "32°F"],
            "answer": "100°C"
        },
        {
            "question": "Which among the following metals is the hardest metal?",
            "options": ["Platinum", "Gold", "Iron", "Tungsten"],
            "answer": "Tungsten"
        }
    ],
    "History": [
        {
            "question": "Who was the first President of the United States?",
            "options": ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"],
            "answer": "George Washington"
        },
        {
            "question": "In which year did World War II end?",
            "options": ["1942", "1945", "1939", "1948"],
            "answer": "1945"
        },
        {
            "question": "Who is known as the 'Iron Man of India' for his role in integrating the Indian states into the Indian Union?",
            "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel", "Subhas Chandra Bose"],
            "answer": "Sardar Vallabhbhai Patel"
        },
        {
            "question": "In which year did India gain independence from British rule?",
            "options": ["1947", "1935", "1950", "1920"],
            "answer": "1947"
        },
        {
            "question": "Who was the first President of India?",
            "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Dr. Rajendra Prasad", "Sardar Vallabhbhai Patel"],
            "answer": "Dr. Rajendra Prasad"
        },
        {
            "question": "Who is the father of the Indian Constitution?",
            "options" : ["B. R. Ambedkar", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel"],
            "answer": "B. R. Ambedkar"
        }

    ]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.total_score = 0
        self.total_questions = 0
        self.completed_categories = []
        self.category = None

        self.title_label = tk.Label(root, text="Welcome to the Quiz Game!", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.selection_frame = tk.Frame(root)
        self.selection_frame.pack(pady=20)

        self.category_label = tk.Label(self.selection_frame, text="Choose a Subject:", font=("Arial", 14))
        self.category_label.pack()

        self.category_buttons = {}
        for category in quiz_data:
            btn = tk.Button(self.selection_frame, text=category, font=("Arial", 12), command=lambda c=category: self.start_quiz(c))
            btn.pack(pady=5)
            self.category_buttons[category] = btn

        self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=550)
        self.buttons_frame = tk.Frame(root)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", font=("Arial", 12), width=50, command=lambda idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next", font=("Arial", 12), command=self.next_question, state=tk.DISABLED)
        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=self.root.quit)

    def start_quiz(self, category):
        self.category = category
        self.selection_frame.pack_forget()
        self.questions = quiz_data[category][:]
        random.shuffle(self.questions)
        self.question_index = 0
        self.score = 0
        self.current_question = {}

        self.question_label.pack(pady=20)
        self.buttons_frame.pack()
        for i, btn in enumerate(self.option_buttons):
            btn.grid(row=i, column=0, pady=5)
        self.next_button.pack(pady=20)
        self.exit_button.pack(pady=10)

        self.load_question()

    def load_question(self):
        self.next_button.config(state=tk.DISABLED)
        for btn in self.option_buttons:
            btn.config(bg="SystemButtonFace", state=tk.NORMAL)

        if self.question_index < len(self.questions):
            self.current_question = self.questions[self.question_index]
            q_text = f"Q{self.question_index + 1}: {self.current_question['question']}"
            self.question_label.config(text=q_text)
            options = self.current_question['options'][:]
            random.shuffle(options)
            for i in range(4):
                self.option_buttons[i].config(text=options[i])
            self.correct_answer = self.current_question['answer']
        else:
            self.completed_categories.append(self.category)
            self.total_score += self.score
            self.total_questions += len(self.questions)
            if len(self.completed_categories) < len(quiz_data):
                remaining = [c for c in quiz_data if c not in self.completed_categories][0]
                self.show_custom_popup("Next Subject", f"Now you'll take the {remaining} quiz.", lambda: self.start_quiz_wrapper(remaining))
            else:
                self.show_result()

    def check_answer(self, idx):
        selected = self.option_buttons[idx].cget("text")
        for i, btn in enumerate(self.option_buttons):
            btn.config(state=tk.DISABLED)
            if btn.cget("text") == self.correct_answer:
                btn.config(bg="green")
            elif i == idx:
                btn.config(bg="red")

        if selected == self.correct_answer:
            self.score += 1
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.question_index += 1
        self.load_question()

    def reset_quiz(self):
        self.question_label.config(text="")
        for btn in self.option_buttons:
            btn.config(text="", state=tk.NORMAL, bg="SystemButtonFace")
        self.next_button.config(state=tk.DISABLED)

    def start_quiz_wrapper(self, category):
        self.reset_quiz()
        self.start_quiz(category)

    def show_result(self):
        percent = (self.total_score / self.total_questions) * 100 if self.total_questions > 0 else 0
        msg = f"Quiz Over!\n\nTotal Score: {self.total_score}/{self.total_questions}\nPercentage: {percent:.2f}%"
        self.show_custom_popup("Final Result", msg)

    def show_custom_popup(self, title, message, callback=None):
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        popup.resizable(False, False)
        popup.configure(bg="white")
    
        # Remove window decorations to prevent moving and closing with X button
        popup.overrideredirect(True)
    
        # Center the popup on the root window
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (400 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (200 // 2)
        popup.geometry(f"+{x}+{y}")
    
        if message is None:
            message = "No message provided."
    
        msg_label = tk.Label(popup, text=message, font=("Arial", 14), wraplength=350, bg="white")
        msg_label.pack(pady=30)
    
        def on_ok():
            popup.destroy()
            if callback:
                callback()
    
        ok_button = tk.Button(popup, text="OK", font=("Arial", 12), width=10, command=on_ok)
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
