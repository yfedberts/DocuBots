import tkinter as tk
from tkinter import ttk, filedialog, OptionMenu, HORIZONTAL
from tkinter.ttk import Progressbar
import docubot, doc_reader, os, time, threading
from docx import Document
import pandas as pd

#Font Settings
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
DISPLAY_FONT = ("Verdana", 8)

#Files temp storage
DOC_SOURCE = ""
DOC_SOURCE2 = ""

dbot = docubot.DocuBot()

#Button Actions
def upload_file(input_textbox, opt):
    filename = filedialog.askopenfilename()
    #ENABLE WRITING
    input_textbox.configure(state='normal')

    if(opt == 1):
        global DOC_SOURCE
        DOC_SOURCE = filename
    if(opt == 2):
        global DOC_SOURCE2
        DOC_SOURCE2 = filename

    print("Selected: ", filename)

    if(dbot.set_file_path(filename, opt)):
        input_textbox.delete(1.0, tk.END)

        doc = Document(filename)
        for p in doc.paragraphs:
            if p.text != '':
                input_textbox.insert(tk.END, p.text + '\n\n')

        input_textbox.configure(font = DISPLAY_FONT)
        print("File successfully uploaded")
    else:
        print("Error in uploading file")

    #DISABLE WRITING
    input_textbox.configure(state='disable')

def run_online_check(filesource, input_textbox, score_textbox, simi_links_textbox, loadingbar):
    #ENABLE WRITING
    loadingbar['value']=20
    score_textbox.configure(state='normal')
    simi_links_textbox.configure(state='normal')

    score, urls = dbot.analyze_simi_online()
    loadingbar['value']=50
    simi_score = round(score, 2)
    score_textbox.insert(tk.END, simi_score)
    loadingbar['value']=70

    cnt = 1
    for link in urls:
        simi_links_textbox.insert(tk.END, str(cnt) + ". " + link + "\n\n")
        cnt+=1

    loadingbar['value']=90

    #DISABLE WRITING
    score_textbox.configure(font = DISPLAY_FONT, state='disable')
    simi_links_textbox.configure(font = DISPLAY_FONT, state='disable')
    loadingbar['value']=100

def run_local_check(display, doc1, doc2, loadingbar):
    loadingbar['value'] = 20
    display.configure(state='normal')
    display.delete(1.0, tk.END)
    loadingbar['value'] = 40
    score = dbot.analyze_simi_local(doc1, doc2) * 100
    loadingbar['value'] = 70
    score = round(score, 2)
    loadingbar['value'] = 80
    display.insert(tk.END, score)
    loadingbar['value'] = 90
    display.configure(font = DISPLAY_FONT, state='disable')
    loadingbar['value'] = 100

class DocuBotApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "DocuBot: Document Plagiarism Checker")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = "True")

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (StartPage, OnlineChecker, LocalChecker):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class OnlineChecker(tk.Frame):
    DOC_SOURCE = ""

    def set_sens(self, varname):
        global dbot
        sens = int(varname.get())
        dbot.set_thresh(sens)
        print(dbot.get_thresh())

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Check for similarities with contents found online", font = LARGE_FONT)
        label.grid(row=0, columnspan=2,sticky="ns")

        #Display the uploaded file
        displayLlabel = ttk.Label(self, text="Uploaded File", font = MEDIUM_FONT)
        displayLlabel.grid(row=1,column=0, pady=0, sticky="nsew")

        docxDisplay = tk.Text(self, height = 25, width = 50)
        docxDisplay.grid(row=2, column =0, rowspan=4, pady=0, sticky="nsew")
        docxDisplay.configure(state='disable')

        #Results Display
        scoreLabel = ttk.Label(self, text="Similarity Score", font = MEDIUM_FONT)
        scoreLabel.grid(row=1, column=1, pady=0, sticky="nsew")

        scoreDisplay = tk.Text(self, height = 5, width = 50)
        scoreDisplay.grid(row=2,column=1,pady=0, sticky="nsew")
        scoreDisplay.configure(state='disable')

        #Similar Links
        similinksLabel = ttk.Label(self, text="Websites with similar content", font=MEDIUM_FONT)
        similinksLabel.grid(row=3, column=1,pady=0,sticky="nsew")

        simiLinksDisplay = tk.Text(self, height = 18, width = 50)
        simiLinksDisplay.grid(row=4, column=1,pady=0, ipady=0, sticky="nsew")
        simiLinksDisplay.configure(state='disable')

        #Sensitivity Option
        OptionList = ["1", "2", "3"]
        var = tk.StringVar(self)
        var.trace("w", lambda x,y,z: self.set_sens(var))
        var.set("2")

        sensLabel = ttk.Label(self, text="          Set Sensitivity \n(1: Low, 2: Medium, 3: High)",font=MEDIUM_FONT)
        sensLabel.grid(row=5, column=1,pady=0)

        sens_option = ttk.OptionMenu(self, var, OptionList[1], *OptionList)
        sens_option.grid(row=6, column=1,pady=0)

        progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='determinate')
        progress.grid(row=7, columnspan=2, pady=5,sticky="ew")

        checkButton = ttk.Button(self, text="Check Similarity", command= lambda: run_online_check(DOC_SOURCE, docxDisplay, scoreDisplay, simiLinksDisplay, progress))
        checkButton.grid(row=8,column=1,pady=0, sticky="nsew")

        uploadButton = ttk.Button(self, text="Upload File", command= lambda: upload_file(docxDisplay, 1))
        uploadButton.grid(row=8,column=0,pady=0, sticky="nsew")

        homeButton = ttk.Button(self, text="Home", command= lambda: controller.show_frame(StartPage))
        homeButton.grid(row=9, columnspan=2,pady=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

class LocalChecker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Check for similarities with documents on your computer", font = LARGE_FONT)
        label.grid(row=0, columnspan=2)

        #Display 1st Document
        LabelDisplay1 = ttk.Label(self, text="File 1", font=MEDIUM_FONT)
        LabelDisplay1.grid(row=1,column=0, sticky="nsew")

        docxDisplay = tk.Text(self, height = 25, width = 50)
        docxDisplay.grid(row=2, column =0, rowspan=3, sticky="nsew")
        docxDisplay.configure(state='disable')

        #Results Display
        scoreLabel = tk.Label(self, text="Similarity Score", font=MEDIUM_FONT)
        scoreLabel.grid(row=1, column=1, sticky="nsew")

        scoreDisplay = tk.Text(self, height = 4, width = 50)
        scoreDisplay.grid(row=2,column=1,sticky="nsew")
        scoreDisplay.configure(state='disable')

        #Display 2nd Doc (for comparison)
        LabelDisplay2 = ttk.Label(self, text="File 2 (Comparison)", font=MEDIUM_FONT)
        LabelDisplay2.grid(row=3, column=1, sticky="nsew")

        docxDisplay2 = tk.Text(self, height = 20, width = 50)
        docxDisplay2.grid(row=4, column=1, sticky="nsew")
        docxDisplay2.configure(state='disable')

        progress = Progressbar(self, orient=HORIZONTAL,length=100,  mode='determinate')
        progress.grid(row=5, columnspan=2, pady=5,sticky="ew")

        checkButton = ttk.Button(self, text="Check Similarity", command= lambda: run_local_check(scoreDisplay, DOC_SOURCE, DOC_SOURCE2, progress))
        checkButton.grid(row=6, columnspan=2, sticky="nsew")

        uploadButton1 = ttk.Button(self, text="Upload File 1", command= lambda: upload_file(docxDisplay, 1))
        uploadButton1.grid(row=7,column=0, sticky="nsew")

        uploadButton2 = ttk.Button(self, text="Upload File 2", command= lambda: upload_file(docxDisplay2, 2))
        uploadButton2.grid(row=7,column=1, sticky="nsew")

        homeButton = ttk.Button(self, text="Home", command= lambda: controller.show_frame(StartPage))
        homeButton.grid(row=8, columnspan=2, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label2 = tk.Label(self, text="By: Yulius Faustinus Edbert (201769990185) & Justin Anthony Nolan (201769990135)", font = MEDIUM_FONT)
        label2.grid(row=0, columnspan=2, sticky="n")

        label = tk.Label(self, text="Document Plagiarism Checker", font = ("Verdana", 15))
        label.grid(row=1, columnspan=2,sticky="n")

        button = ttk.Button(self, text="Check for similarities online", command= lambda: controller.show_frame(OnlineChecker))
        button.grid(row=2, column = 0, pady=15, padx=15)

        button1 = ttk.Button(self, text="Check for similarities with local files", command= lambda: controller.show_frame(LocalChecker))
        button1.grid(row = 2, column = 1, pady=15, padx=15)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

app = DocuBotApp()
app.mainloop()