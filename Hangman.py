# coding=utf-8
from collections import Counter
from string import ascii_lowercase
from tkinter import *


class Back(object):
    ENG = "ENG.txt"
    PL = "PL.txt"
    LANGS = (PL, ENG)

    def __init__(self):
        self.list_wrong_latter = []
        self.dic_words_in_file = {}

    def give_good_word(self, enter):
        self.corect_word(enter)
        self.check_words(len(enter))
        result = Back.stats(" ".join(self.dic_words_in_file[self.name_file]),
                                list(self.dic_letter.keys()) + self.list_wrong_latter)
        self.result=result

    def good_letter_in_good_postion_in_word(self, word):
        if len(list(self.dic_letter.keys())) > 0:
            for letter in list(self.dic_letter.keys()):
                if letter not in word:
                    return False
                else:
                    for postion in self.dic_letter[letter]:
                        if not word[postion] == letter:
                            return False
        return True

    # liczy liczbe wtstepowania jakiejs litery
    @staticmethod
    def stats(string, letter):
        string = string.lower()
        chars_stats = Counter(string).most_common()
        chars_stats_clean = []
        for l, c in chars_stats:
            if l.isalpha():
                if l not in letter and l != " " and l != "\n":
                    chars_stats_clean.append((l, c))
        return chars_stats_clean

    def check_for_bad_letter(self, word):
        for letter in self.list_wrong_latter:
            if letter in word:
                return False
        return True

    def check_words(self, length):
        listWord = []
        for word in self.dic_words_in_file[self.name_file]:
            if length + 1 == len(word):
                if self.good_letter_in_good_postion_in_word(word):
                    if self.check_for_bad_letter(word):
                        listWord.append(word)
        self.dic_words_in_file[self.name_file] = listWord

    # zapisuje litery wystepujace w podanym ciagu i ich pozyje
    def corect_word(self, word):
        self.dic_letter = {}
        for n, s in enumerate(word):
            if s.isalpha():
                if self.dic_letter.get(s):
                    self.dic_letter[s].append(n)
                elif not self.dic_letter.get(s):
                    self.dic_letter[s] = [n]
            elif s.isdigit():
                print("corect_word#1")
            else:
                pass

    @staticmethod
    def check_change(new, old):
        print(1)
        if old == new:
            return False
        else:
            print(2)
            return True

    def add_file(self, file=PL):
        self.name_file = file
        if not self.dic_words_in_file.get(file):
            with open(file=file, mode="r", encoding="utf-8") as self.words:
                self.dic_words_in_file[file] = self.words.readlines()

    def change_stat_letter(self, letter):
        if letter in self.list_wrong_latter:
            self.list_wrong_latter.remove(letter)
            self.add_file(self.name_file)
        else:
            self.list_wrong_latter.append(letter)

    def take_ent1(self, ent1):
        self.ent1 = ent1


class Config_Win(object):
    def __init__(self, logic, parent=None):
        self.config = Tk(parent)
        self.config.title("Config")
        self.config.grid()

        self.back_logic = logic
        self.logic()

        self.config_win()

    def logic(self):
        self.back_logic.add_file()

    def make_enter(self):
        self.ent1 = Entry(self.config, width=20)
        self.ent1.grid(row=1, column=0, columnspan=1)
        self.ent1.focus()
        self.back_logic.ent1 = self.ent1

    def config_win(self):
        tmp = IntVar()
        for n, lang in enumerate(Back.LANGS):
            Radiobutton(self.config, text=lang, value=lang, variable=tmp,
                        command=lambda x=lang: self.back_logic.add_file(x)).grid(row=0, column=n)
        tmp.set(0)

        self.make_enter()

        Button(self.config, text="Show", command=lambda x=self.back_logic: App_Win(x)).grid(row=1, column=1)


class App_Win(object):
    def __init__(self, logic):
        self.back_logic = logic
        self.main_win_frame = Tk(None)
        self.main_win_frame.title("Main")
        self.main_win_frame.grid()
        self.main_win()
        self.back_logic.add_file()
        self.back_logic.list_wrong_latter = []



    def second_part_win(self):
        self.back_logic.give_good_word(self.ent2.get())
        for n,result in enumerate(self.back_logic.result[:6],1):
            Label(self.main_win_frame,text=result).grid(row=n,column=8)


    def main_win(self):
        number = self.back_logic.ent1.get()
        self.ent2 = Entry(self.main_win_frame)
        if number.isdigit():
            number = int(number)
            self.ent2.insert(0, "*" * number)
        else:
            print("main_win#1")
        self.ent2.grid(row=0, column=0, columnspan=4)
        self.ent2.focus()

        butt = Button(self.main_win_frame, text="Help me", command=(lambda:self.second_part_win()))
        butt.grid(row=0, column=5)

        c = 0
        for n, l in enumerate(ascii_lowercase):
            chk = Checkbutton(self.main_win_frame, text=l, command=lambda x=l: self.back_logic.change_stat_letter(x))
            r = n % 6
            if r == 0:
                c += 1
            chk.grid(row=1 + r, column=c)


class Start(object):
    def __init__(self):
        self.logic = Back()
        self.firstWindow = Config_Win(self.logic).config
        self.firstWindow.mainloop()


Start()
