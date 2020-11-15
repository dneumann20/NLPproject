import tkinter as tk
from tkinter import *
import pandas as pd
#from tkinter.ttk import Progressbar

from implementation import sim, wordnet_sim, sim_snippets1
from implementation import google_snippets, sim_snippets2
#import sys

from pandastable import Table

def get_values():
    word1, word2 = entry1.get(), entry2.get()
    
    if len(word1) ==0:
        tk.messagebox.showinfo('Error', 'Please Enter First Word before finding similarity')
        return None, word2
        
    if len(word2) ==0:
        tk.messagebox.showinfo('Error','Please Enter Second Word before finding similarity')
        word2=None
    
    return word1, word2
    
    
def wordsim(event=None):
    
    word1, word2 = get_values()
    if word1 and word2:
        value = sim(word1, word2, 5)
        tk.messagebox.showinfo('Similarity', 'Word Sim Score : ', round(value, 3))


def net_sim(event=None):
     
    word1, word2 = get_values()
    if word1 and word2:
        a,b,c = wordnet_sim(word1, word2)
        tk.messagebox.showinfo('Wordnet Similarity','WUp: {} , Path: {} , Chod: {}'.
                           format(a,b,c))

def snippet1(event=None):

    word1, word2 = get_values()        
    if word1 and word2:
        snip_p = google_snippets(word1)
        snip_q = google_snippets(word2)
        
        value = sim_snippets1(snip_p, snip_q)
        tk.messagebox.showinfo('Snippet Similarity','Sim SNippet 1 Score: {}'.
                           format(round(value, 2)))
     


def snippet2(event=None):

    word1, word2 = get_values()        
    if word1 and word2:
        snip_p = google_snippets(word1)
        snip_q = google_snippets(word2)
        value = sim_snippets2(snip_p, snip_q)
        tk.messagebox.showinfo('Snippet Similarity','Sim SNippet 2 Score: {}'.
                           format(round(value, 2)))



def exit():
    root.destroy()
    


def gui():
    global root, entry1, entry2
    
    root = tk.Tk()

    lbl=Label(root, text="Simantic Similarity", fg='#37251F', font=("Helvetica", 20))
    lbl.place(x=130, y=30)
    
    lb_e1=Label(root, text="First Word: ", fg='#37251F', font=("Helvetica", 10))
    lb_e1.place(x=90,y=90)
    
    entry1 = tk.Entry(root) 
    entry1.place(x=165, y=90, height=30, width=200)



    lb_e2=Label(root, text="Second Word: ", fg='#37251F', font=("Helvetica", 10))
    lb_e2.place(x=70,y=140)    
    entry2 = tk.Entry(root)
    entry2.place(x=165, y=140, height=30, width=200)
    
    
    
    x=172
    button1 = tk.Button(root, text='Web Sim', command=wordsim, fg='white',bg='black', activebackground='#4F2619', height=3,
                  width = 25)
    button1.place(x=x, y=190)
    
    button2 = tk.Button(root, text='Wordnet Sim', command=net_sim, fg='white',bg='black', activebackground='#4F2619', height=3,
                  width = 25)
    button2.place(x=x, y=260)
    
    button3 = tk.Button(root, text='Sim Snippet 1', command=snippet1, fg='white',bg='black', activebackground='#4F2619', height=3,
                  width = 25)
    button3.place(x=x, y=330)
    
    button4 = tk.Button(root, text='Sim Snippet 2', command=snippet2, fg='white',bg='black', activebackground='#4F2619', height=3,
                  width = 25)
    button4.place(x=x, y=400)

    button5 = tk.Button(root, text='Exit', command=exit, fg='white',bg='black', activebackground='#4F2619', height=3,
                  width = 25)
    button5.place(x=x, y=470)
    
    root.title('Application')
    root.geometry("500x650+300+20")
    root.mainloop()


if __name__ == '__main__':

    gui()