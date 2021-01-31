import tkinter
import os
from tkinter import *

from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:
  # * Rook tkinter instance
  __root = Tk()

  # ? Main Window Dimensions
  __windowWidth = 300
  __windowHeight = 300

  # ? Components
  __textArea = Text(__root)
  __menuBar = Menu(__root)
  __fileMenu = Menu(__menuBar, tearoff=0)
  __editMenu = Menu(__menuBar, tearoff=0)
  __helpMenu = Menu(__menuBar, tearoff=0)
  __scrollBar = Scrollbar(__textArea)

  # ? Current file
  __file = None

  def __init__(self, **kwargs):
    # * Set application icon
    try:
      self.__root.wm_iconbitmap("notepad.ico")
    except:
      pass

    # * Set window sizing
    try:
      self.__windowWidth = kwargs['width']
      self.__windowHeight = kwargs['height']
    except KeyError:
      pass

    # * Set window title
    self.__root.title("Untitled - Moonrise Editor")

    # * Centering window on screen
    screenWidth = self.__root.winfo_screenwidth()
    screenHeight = self.__root.winfo_screenheight()

    left = (screenWidth / 2) - (self.__windowWidth / 2)
    top = (screenHeight / 2) - (self.__windowHeight / 2)

    self.__root.geometry('%dx%d+%d+%d' % (
      self.__windowWidth, self.__windowHeight, left, top
    ))

    # * Responsive textarea sizing
    self.__root.grid_rowconfigure(0, weight=1)
    self.__root.grid_columnconfigure(0, weight=1)

    # * Adding controls to textarea
    self.__textArea.grid(sticky=N + E + S + W)
    
    # ? File Controls
    self.__fileMenu.add_command(label="New", command=self.__newFile)
    self.__fileMenu.add_command(label="Open", command=self.__openFile)
    self.__fileMenu.add_command(label="Save", command=self.__saveFile)
    self.__fileMenu.add_separator()
    self.__fileMenu.add_command(label="Exit", command=self.__quitApplication)

    # ? Edit Controls
    self.__editMenu.add_command(label="Cut", command=self.__cut)
    self.__editMenu.add_command(label="Copy", command=self.__copy)
    self.__editMenu.add_command(label="Paste", command=self.__paste)

    # ? About Controls
    self.__helpMenu.add_command(label="About", command=self.__showAbout)

    # * Adding features to menu bar
    self.__menuBar.add_cascade(label="File", menu=self.__fileMenu)
    self.__menuBar.add_cascade(label="Edit", menu=self.__editMenu)
    self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)

    # * Setting menubar as root menu
    self.__root.config(menu=self.__menuBar)

    # * Configuring scrollbar
    self.__scrollBar.pack(side=RIGHT, fill=Y)
    self.__scrollBar.config(command=self.__textArea.yview)
    self.__textArea.config(yscrollcommand=self.__scrollBar.set)

  # * Commands
  def __newFile(self):
    self.__root.title("Untitled - Notepad")
    self.__file = None
    self.__textArea.delete(1.0, END)

  def __openFile(self):
    self.__file = askopenfilename(
      defaultextension=".txt",
      filetypes=[ ("All Files", "*"), ("Text Documents", ".txt") ]
    )

    if self.__file == "":
      # ? No file to open
      self.__file = None
    else:
      # ? Try to open the file and update window title
      self.__root.title(os.path.basename(self.__file) + " - Notepad")
      self.__textArea.delete(1.0, END)

      # ? Read file text and input to textarea
      file = open(self.__file, "r")
      self.__textArea.insert(1.0, file.read())
      file.close()

  def __saveFile(self):
    if self.__file == None:
      # ? Save as new file
      self.__file = asksaveasfilename(
        initialfile="Untitled.txt",
        defaultextension=".txt",
        filetypes=[ ("All Files", "*"), ("Text Documents", ".txt") ]
      )

      if self.__file == "":
        # ? User canceled save
        self.__file = None
      else:
        # ? If file was created, try to save in file
        file = open(self.__file, "w")
        file.write(self.__textArea.get(1.0, END))
        file.close()

        # ? Update window title
        self.__root.title(os.path.basename(self.__file) + " - Notepad")
    else:
      # ? If file exists, save in file
      file = open(self.__file, "w")
      file.write(self.__textArea.get(1.0, END))
      file.close()

  def __cut(self):
    self.__textArea.event_generate("<<Cut>>")

  def __copy(self):
    self.__textArea.event_generate("<<Copy>>")

  def __paste(self):
    self.__textArea.event_generate("<<Paste>>")

  def __quitApplication(self):
    self.__root.destroy()

  def __showAbout(self):
    showinfo("Notepad", "Made with TKinter by MDJ")

  # * Run main application
  def run(self):
    self.__root.mainloop()

notepad = Notepad(width=600, height=400)
notepad.run()
