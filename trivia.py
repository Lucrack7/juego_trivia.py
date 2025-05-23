import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import os

class TriviaGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Trivia Game - Python Edition")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        self.score = 0
        self.current_q = 0

        self.load_questions()
        self.ask_category()

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 16), wraplength=500, justify="center")
        self.question_label.pack(pady=30)

        self.buttons = []
        for _ in range(4):
            btn = tk.Button(self.master, text="", font=("Helvetica", 14), width=30, command=lambda i=_: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.next_button = tk.Button(self.master, text="Siguiente", font=("Helvetica", 12), command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=20)

        self.display_question()

    def load_questions(self):
        try:
            base_path = os.path.dirname(__file__)
            file_path = os.path.join(base_path, "questions.json")
            with open(file_path, "r", encoding="utf-8") as file:
                self.all_questions = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las preguntas:\n{e}")
            self.master.destroy()

    def ask_category(self):
        categories = list(set(q.get("category", "General") for q in self.all_questions))
        categories.sort()

        selected = simpledialog.askstring("Categoría", f"Selecciona una categoría:\n{', '.join(categories)}\n(O deja vacío para todas)")
        
        if selected and selected in categories:
            self.questions = [q for q in self.all_questions if q.get("category", "General") == selected]
        else:
            self.questions = self.all_questions

        if not self.questions:
            messagebox.showerror("Error", "No hay preguntas disponibles en esta categoría.")
            self.master.destroy()

        random.shuffle(self.questions)

    def display_question(self):
        if self.current_q >= len(self.questions):
            self.show_score()
            return

        q = self.questions[self.current_q]
        self.correct_answer = q["answer"]

        self.question_label.config(text=q["question"])

        options = q["options"]
        random.shuffle(options)
        for i, option in enumerate(options):
            self.buttons[i].config(text=option, state=tk.NORMAL, bg="SystemButtonFace")

        self.next_button.config(state=tk.DISABLED)

    def check_answer(self, index):
        selected = self.buttons[index].cget("text")
        is_correct = selected == self.correct_answer

        if is_correct:
            self.buttons[index].config(bg="green")
            self.score += 1
        else:
            self.buttons[index].config(bg="red")
            for btn in self.buttons:
                if btn.cget("text") == self.correct_answer:
                    btn.config(bg="green")

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_q += 1
        self.display_question()

    def show_score(self):
        messagebox.showinfo("¡Juego Terminado!", f"Tu puntaje final es: {self.score}/{len(self.questions)}")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TriviaGame(root)
    root.mainloop()
