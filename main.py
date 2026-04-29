import customtkinter as ctk
import random, json, os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── DATA: List of country-capital pairs (manages complexity) ──────────────────
ALL_COUNTRIES = [
    {"country": "Afghanistan", "capital": "Kabul"}, {"country": "Albania", "capital": "Tirana"},  
    {"country": "Algeria", "capital": "Algiers"},  {"country": "Argentina", "capital": "Buenos Aires"},
    {"country": "Armenia", "capital": "Yerevan"}, {"country": "Australia", "capital": "Canberra"},
    {"country": "Austria", "capital": "Vienna"}, {"country": "Azerbaijan", "capital": "Baku"},
    {"country": "Belarus", "capital": "Minsk"},{"country": "Belgium", "capital": "Brussels"},
    {"country": "Brazil", "capital": "Brasilia"},{"country": "Canada", "capital": "Ottawa"},
    {"country": "Chile", "capital": "Santiago"}, {"country": "China", "capital": "Beijing"},
    {"country": "Czech Republic", "capital": "Prague"},{"country": "Denmark", "capital": "Copenhagen"},
    {"country": "Egypt", "capital": "Cairo"}, {"country": "Finland", "capital": "Helsinki"},
    {"country": "France", "capital": "Paris"}, {"country": "Georgia", "capital": "Tbilisi"},
    {"country": "Germany", "capital": "Berlin"}, {"country": "Greece", "capital": "Athens"},
    {"country": "Hungary", "capital": "Budapest"}, {"country": "India", "capital": "New Delhi"},
    {"country": "Indonesia", "capital": "Jakarta"}, {"country": "Iran", "capital": "Tehran"},
    {"country": "Iraq", "capital": "Baghdad"}, {"country": "Italy", "capital": "Rome"},
    {"country": "Japan", "capital": "Tokyo"}, {"country": "Kazakhstan", "capital": "Astana"},
    {"country": "Kyrgyzstan", "capital": "Bishkek"}, {"country": "Mexico", "capital": "Mexico City"},
    {"country": "Mongolia", "capital": "Ulaanbaatar"},  {"country": "Netherlands", "capital": "Amsterdam"},
    {"country": "Norway", "capital": "Oslo"}, {"country": "Pakistan", "capital": "Islamabad"},
    {"country": "Poland", "capital": "Warsaw"}, {"country": "Portugal", "capital": "Lisbon"},
    {"country": "Russia", "capital": "Moscow"},  {"country": "Saudi Arabia", "capital": "Riyadh"},
    {"country": "South Korea", "capital": "Seoul"}, {"country": "Spain", "capital": "Madrid"},
    {"country": "Sweden", "capital": "Stockholm"}, {"country": "Turkey", "capital": "Ankara"},
    {"country": "UAE", "capital": "Abu Dhabi"}, {"country": "Ukraine", "capital": "Kyiv"},
    {"country": "United Kingdom", "capital": "London"}, {"country": "United States", "capital": "Washington D.C."},
    {"country": "Uzbekistan", "capital": "Tashkent"},
]

SCORE_FILE = "highscore.json"



def buildAnswerChoices(countryList, correctCapital):
    wrongCapitals = []
    for entry in countryList:                       
        if entry["capital"] != correctCapital:       
            wrongCapitals.append(entry["capital"])
    choices = random.sample(wrongCapitals, 3) + [correctCapital]
    random.shuffle(choices)
    return choices


class CapitalGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Capital Quiz: Survival Mode")
        self.geometry("600x550")

        # Game state stored as simple variables
        self.currentScore = 0
        self.starCount    = 0
        self.highScore    = self._loadScore()
        self.choices      = []
        self.country      = {}
        self.buttons      = []

        self._buildUI()
        self.bind("<Key>", lambda e: self._onAnswerClicked(int(e.char) - 1)
                  if self.btnFrame.winfo_manager() and e.char in "1234" else None)
        self._nextQuestion()

    # ── UI: build all widgets once ────────────────────────────────────────────
    def _buildUI(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=20)
        self.scoreLabel  = ctk.CTkLabel(top, text="Score: 0", font=("Arial", 18, "bold"))
        self.scoreLabel.pack(side="left")
        self.starLabel   = ctk.CTkLabel(top, text="Stars: 0 ⭐", text_color="#FFD700", font=("Arial", 18, "bold"))
        self.starLabel.pack(side="right")
        self.bestLabel   = ctk.CTkLabel(self, text=f"Best: {self.highScore}", font=("Arial", 14), text_color="#5294e2")
        self.bestLabel.pack()
        self.questionLabel = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"), wraplength=500)
        self.questionLabel.pack(pady=30)

        self.btnFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.btnFrame.pack(pady=5)
        for i in range(4):                           # ITERATION: create 4 buttons from a loop
            btn = ctk.CTkButton(self.btnFrame, text="", width=240, height=55,
                                font=("Arial", 15, "bold"),
                                command=lambda i=i: self._onAnswerClicked(i))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=8)
            self.buttons.append(btn)                 # store in list

        self.feedbackLabel  = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.feedbackLabel.pack(pady=15)
        self.restartBtn = ctk.CTkButton(self, text="Play Again", width=200, height=50,
                                        fg_color="#e74c3c", hover_color="#c0392b",
                                        font=("Arial", 18, "bold"), command=self._restart)


    def _nextQuestion(self):
        self.country = random.choice(ALL_COUNTRIES)

        self.choices = buildAnswerChoices(ALL_COUNTRIES, self.country["capital"])

        self.questionLabel.configure(
            text=f"What is the capital of\n'{self.country['country']}'?",
            text_color="white")
        for i in range(len(self.buttons)):          
            self.buttons[i].configure(text=f"{i+1}. {self.choices[i]}", state="normal")
        self.restartBtn.pack_forget()

    # ── Check answer and update game state ────────────────────────────────────
    # 3c: Selection — correct path vs wrong path; calls checkIfNewRecord.
    def _onAnswerClicked(self, idx):
        if not (0 <= idx <= 3): return
        correct = self.choices[idx] == self.country["capital"]  # SELECTION
        if correct:
            self.currentScore += 1
            if self.currentScore % 10 == 0: self.starCount += 1
            self.feedbackLabel.configure(text="Correct! ✅", text_color="#46cc71")
            self._updateDisplay()
            self.after(500, self._nextQuestion)
        elif self.starCount > 0:
            self.starCount -= 1
            self.feedbackLabel.configure(text="Wrong! A star saved you! 🛡️", text_color="orange")
            self._updateDisplay()
            self.after(800, self._nextQuestion)
        else:
            self.btnFrame.pack_forget()
            self.questionLabel.configure(
                text=f"GAME OVER! ❌\nYour Score: {self.currentScore}", text_color="#e74c3c")
            self.feedbackLabel.configure(text=f"All-time Best: {self.highScore}", text_color="white")
            self.restartBtn.pack(pady=20)

    # ── Update score labels and save record if beaten ─────────────────────────
    def _updateDisplay(self):
        self.highScore = self.currentScore if self.currentScore > self.highScore else self.highScore
        self.scoreLabel.configure(text=f"Score: {self.currentScore}")
        self.starLabel.configure(text=f"Stars: {self.starCount} ⭐")
        self.bestLabel.configure(text=f"Best: {self.highScore}")
        self._saveScore()

    def _restart(self):
        self.currentScore = self.starCount = 0
        self.btnFrame.pack(pady=5)
        self._updateDisplay()
        self._nextQuestion()

    def _loadScore(self):
        try:
            with open(SCORE_FILE) as f: return json.load(f).get("high_score", 0)
        except Exception: return 0

    def _saveScore(self):
        with open(SCORE_FILE, "w") as f: json.dump({"high_score": self.highScore}, f)


if __name__ == "__main__":
    CapitalGame().mainloop()
