from tkinter import *
from tkinter import messagebox
import json
import random
from pathlib import Path

words_list = []
wrong_list = []
questions = []
max_time = 5

retry = False

base = Tk()
base.wm_state('iconic')
base.iconify()

class Question():
    word = {}
    answers_list = []
    selected_ans_index = -1
    correct_ans_index = -1
    wrong = False

    def __init__(self, word, answers):
        self.word = word
        self.answers_list = answers
        self.correct_ans_index = self.answers_list.index(word)

    def __repr__(self):
        return f"<Question word:{self.word} answers_list:{self.answers_list} correct_ans_index:{self.correct_ans_index} selected_ans_index:{self.selected_ans_index}>"

    def __str__(self):
        return f"From str method of Question: word is {self.word}, answers_list is {self.answers_list}"

    def vaildation(self, i):
        self.selected_ans_index = i

        if i != self.correct_ans_index:
            self.wrong = True
            wrong_list.append(self)
            return [self.word]

        return []
    
    def changeAnswers(self):
        self.answers_list = random.choices(words_list, k = 5)

        self.answers_list.append(self.word)

        random.shuffle(self.answers_list)

        self.correct_ans_index = self.answers_list.index(self.word)
    
    def to_dict(self):
        return {
            "word": self.word,
            "answers": self.answers_list,
            "selected_ans_index": self.selected_ans_index,
            "correct_ans_index": self.correct_ans_index
        }

def createQuestion():
    word = random.choice(words_list)
    idx = words_list.index(word)
    words_list.remove(word)

    answers = random.choices(words_list, k = 3)

    rad = idx+random.randint(1, 10)*random.choice([1, -1])
    if(rad > len(words_list)-1 or rad < 0):
        rad = idx
    
    answers.append(words_list[rad])


    rad = idx+random.randint(1, 10)*random.choice([1, -1])
    if(rad > len(words_list)-1 or rad < 0):
        if rad == 0:
            rad = idx+1
        else:
            rad = idx-1
    
    answers.append(words_list[rad])

    answers.append(word)
    random.shuffle(answers)

    return Question(
        word = word,
        answers = answers
    )

class Setup():
    amount_of_questions = IntVar(value=15)
    levels = StringVar(value="3,4,5")
    time_limit = IntVar(value=10)

    def start():
        pass

    def __init__(self):
        self.root = Toplevel()
        self.root.title("Word Test Setup")
        self.root.geometry('300x300')
        self.root.config(bg="skyblue")
        self.root.resizable(False, False)

        Label(self.root, text="amount of questions").pack()
        Entry(self.root, textvariable=self.amount_of_questions).pack()

        Label(self.root, text="levels").pack()
        Entry(self.root, textvariable=self.levels).pack()

        Label(self.root, text="time limit per question").pack()
        Entry(self.root, textvariable=self.time_limit).pack()

        Button(self.root, text="Start", command=self.start).pack()

    def loop(self):
        self.root.mainloop()

    def start(self):
        self.root.quit()
        self.root.destroy()

class Test():
    def sendAnswer(): pass

    def key_handler(): pass
        
    def __init__(self):
        self.question_word_var = StringVar(value = "")
        self.answers_list = [StringVar(value = i) for i in range(0, 6)]
        self.answers_btn_list = []
        self.question_idx = IntVar(value= 0)
        self.timeLeft = DoubleVar(value= max_time)

        self.cancel_id = 0

        self.question_word_var = StringVar(value = "")

        self.root = Toplevel()
        self.root.title("Word Test")
        self.root.geometry('1000x700')
        self.root.config(bg="skyblue")
        self.root.resizable(False, False)

        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=3)
        Grid.rowconfigure(self.root, 2, weight=3)
        Grid.columnconfigure(self.root, 0, weight=1)

        self.timeLeft.set(max_time)

        Label(self.root, textvariable=self.timeLeft, font=('JetBrainsMono', 20, 'bold'), fg="#FFF", bg="red", padx=5, pady=3).grid(row=0, column=0, sticky=N+E+W)

        # 問題
        question_frame = Frame(self.root)
        question_frame.grid(row=1, column=0, sticky=N+E+W)

        question_text = Label(question_frame, textvariable=self.question_word_var, font=('JetBrainsMono', 40, 'bold'), pady=8)
        question_text.pack()

        Label(self.root, textvariable=self.question_idx, font=('JetBrainsMono', 30, 'bold'), fg="#FFF", bg="blue", padx=5, pady=3).place(x=0, y=0)

        # 答案
        answer_frame = Frame(self.root)
        answer_frame.grid(row=2, column=0, sticky=E+W)

        self.root.bind("<Key>", self.key_handler)

        for i in range(0, 6):
            Grid.rowconfigure(answer_frame, int(i/2), weight=1)
            Grid.columnconfigure(answer_frame, i%2, weight=1)

            self.answers_btn_list.append(Button(
                answer_frame,
                textvariable=self.answers_list[i],
                command=(lambda n=i: self.sendAnswer(n)),
                padx=10,
                pady=30,
                borderwidth=0,
                font=('jf-openhuninn-2.0', 22)
            ))
            
            self.answers_btn_list[-1].grid(row=int(i/2), column=i%2, sticky=N+S+E+W)

    def setQuestion(self, q: Question):
        self.question = q

        self.question_word_var.set(q.word["word"])
        for i in range(0, 6):
            self.answers_list[i].set(f"({i+1}){q.answers_list[i]['definition']}")
        
        self.timer()
        self.root.focus_force()

    def next(self):
        if self.question_idx.get() == len(questions):
            self.root.quit()
            self.root.destroy()
            return

        self.question_idx.set(self.question_idx.get()+1)
        self.setQuestion(questions[self.question_idx.get()-1])

    def loop(self):
        self.root.mainloop()

    def timer(self):
        if self.timeLeft.get() <= 0:
            self.timer_reset()
            res = (self.question).vaildation(-2)
            messagebox.showerror(message="TIME OUT, ans: "+res[0]["definition"])
            self.next()
            return
        
        self.timeLeft.set(self.timeLeft.get()-0.1)
        
        self.cancel_id = self.root.after(100, self.timer)

    def timer_reset(self):
        self.root.after_cancel(self.cancel_id)
        self.timeLeft.set(max_time)

    def sendAnswer(self, n):
        self.timer_reset()

        res = (self.question).vaildation(n)

        if len(res) == 0:
            messagebox.showinfo(message="CORRECT")
        else:
            messagebox.showerror(message="WRONG, ans: "+res[0]["definition"])

        self.next()

    def key_handler(self, event):
        if "1" <= event.char <= "6":
            self.answers_btn_list[(ord(event.char)-49)].invoke()

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all('<MouseWheel>', self.on_vertical)

    def on_vertical(self, event):
        self.canvas.yview_scroll(-1 * event.delta, 'units')

class Result():
    def export(): pass
    def retry(): pass

    def __init__(self):
        self.root = Toplevel()
        self.root.title("Result")
        self.root.geometry('650x700')
        self.root.config(bg="skyblue")
        self.root.resizable(True, True)

        Label(self.root, text="Accuracy: {:.2f}%".format(((len(questions)-len(wrong_list))/len(questions))*100), font=('JetBrainsMono', 20, 'bold'), fg="#FFF", bg="blue", padx=5, pady=3).pack(fill="x")
        Button(
            self.root,
            text="export as xlsx",
            command=self.export,
            padx=10,
            pady=10,
            borderwidth=0,
            font=('jf-openhuninn-2.0', 18),
            bg="lightblue",
            fg="#000"
        ).pack(fill="x")

        self.frame = ScrollableFrame(self.root)

        for q in questions:
            self.addQuestion(q)

        self.frame.pack(fill="both", expand=1)

        Button(
            self.root,
            text="retry",
            command=self.retry,
            padx=10,
            pady=10,
            borderwidth=0,
            font=('jf-openhuninn-2.0', 18),
            bg="lightblue",
            fg="#000"
        ).pack(fill="x")

    def addQuestion(self, question: Question):
        frame = Frame(self.frame.scrollable_frame, background="lightblue", padx=10, pady=10, bd=2, relief=SOLID)
        frame.pack(fill="x", expand=1, pady=5)

        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)

        Label(frame, text=f"{question.word['word']} ({question.word['definition']})", font=('Helvetica', 16, 'bold'), bg="lightblue", fg="#000").grid(row=0, column=0, columnspan=2, sticky=N, pady=5)

        for idx in range(0, 6):
            Grid.rowconfigure(frame, int(idx/2)+1, weight=1)
            ans = question.answers_list[idx]
            bg_color = "lightgreen" if idx == question.correct_ans_index else ("lightcoral" if idx == question.selected_ans_index and idx != question.correct_ans_index else "white")
            Label(frame, text=f"{ans['word']} ({ans['definition']})", font=('Helvetica', 14), fg="#000", bg=bg_color, padx=5, pady=5, bd=1, relief=SOLID).grid(row=int(idx/2)+1, column=idx%2, padx=5, pady=5, sticky=N+S+E+W)

    def export(self):
        messagebox.showinfo(message="this feature is unavailable currently")

    def loop(self):
        self.root.mainloop()

    def retry(self):
        self.root.quit()
        self.root.destroy()
        global retry
        retry = True

if __name__ == "__main__":

    setup = Setup()
    setup.loop()

    max_time = setup.time_limit.get()

    p = Path(__file__)

    with open(str(p.parent) + "/all.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        
        for level in str.split(setup.levels.get(), ','):
            for word in data[level]:
                words_list.append(word)
        
        words_list = sorted(words_list, key=lambda x: x['word'])

    for i in range(0, setup.amount_of_questions.get()):
        questions.append(createQuestion())

    test = Test()
    test.next()
    test.loop()

    result = Result()
    result.loop()
    
    while retry:
        del test
        del result

        if len(wrong_list) == 0:
            questions = []
            for i in range(0, setup.amount_of_questions.get()):
                questions.append(createQuestion())
        else:
            questions = wrong_list

        for q in questions:
            q.changeAnswers()
        
        wrong_list = []

        test = Test()
        test.next()
        test.loop()

        result = Result()
        result.loop()