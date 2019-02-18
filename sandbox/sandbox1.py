import tkinter
from tkinter import ttk
import math as ma

def main():
    root = tkinter.Tk()
    root.title("Shengjun's CSSE 120 Final Project")

    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()
    canvas = tkinter.Canvas(main_frame, width=480, height=520, bg='white')
    canvas.grid(row=0, column = 0)

main()