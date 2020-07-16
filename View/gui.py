import tkinter as tk
from tkinter import ttk, filedialog, OptionMenu
import docubot, doc_reader, os
from docx import Document
import pandas as pd

#Settings
LARGE_FONT = ("Verdana", 12)
DISPLAY_FONT = ("Verdana", 10)

#Folder Paths
PATH1 = os.path.dirname(__file__)
MODEL_FOLDER = os.path.dirname(os.path.abspath("Model"))
DATA_FOLDER = os.path.dirname(os.path.abspath("Data"))
DOCX_FOLDER = os.path.dirname(os.path.abspath("docxFiles"))

#Files pathing
DOC_SOURCE = ""
DOC_SOURCE2 = ""

DOC_TEXTS = os.path.join(PATH1, MODEL_FOLDER, DATA_FOLDER, "doc_texts.csv")
LINKS_LIST = os.path.join(PATH1, MODEL_FOLDER, DATA_FOLDER, "linksToScrape.csv")
SCRAPE_RESULTS_CSV = os.path.join(PATH1, MODEL_FOLDER, DATA_FOLDER, "scrape_results.csv")
SCRAPE_RESULTS_JSON = os.path.join(PATH1, MODEL_FOLDER, DATA_FOLDER, "scraped_results.json")
SIMI_RESULT = os.path.join(PATH1, MODEL_FOLDER, DATA_FOLDER, "simi_results.csv")

dbot = docubot.DocuBot()

#Button Actions

def upload_file(input_textbox, opt):
    filename = filedialog.askopenfilename()
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

def run_check(filesource, input_textbox, score_textbox, simi_links_textbox):
    score = dbot.analyze_simi_online()
    data = pd.read_csv(r"B:\docubot\DocuBots\Model\Data\simi_results.csv")
    print(score)
    simi_score = round(score, 2)
    score_textbox.insert(tk.END, simi_score)

    cnt = 1
    links = data['simi_links']
    for link in links:
        simi_links_textbox.insert(tk.END, str(cnt) + ". " + link + "\n\n")
        cnt+=1

def run_local_check(display, doc1, doc2):
    display.delete(1.0, tk.END)
    score = dbot.analyze_simi_local(doc1, doc2) * 100
    score = round(score, 2)
    display.insert(tk.END, score)

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
        label.grid(row=0, columnspan=2)

        #TODO: Find a way to set the position of the textbox
        docxDisplay = tk.Text(self, height = 25, width = 50)
        docxDisplay.grid(row=1, column =0, rowspan=2)

        #Results Display
        scoreDisplay = tk.Text(self, height = 5, width = 50)
        scoreDisplay.grid(row=1,column=1)

        #Similar Links
        simiLinksDisplay = tk.Text(self, height = 20, width = 50)
        simiLinksDisplay.grid(row=2, column=1)

        #Sensitivity Option
        OptionList = ["1", "2", "3"]
        var = tk.StringVar(self)
        var.trace("w", lambda x,y,z: self.set_sens(var))
        var.set("2")

        sens_option = ttk.OptionMenu(self, var, OptionList[1], *OptionList)
        sens_option.config(width = 5)
        sens_option.grid(row=3, column=1)

        checkButton = ttk.Button(self, text="Check Similarity", command= lambda: run_check(DOC_SOURCE, docxDisplay, scoreDisplay, simiLinksDisplay))
        checkButton.grid(row=4,column=1)

        uploadButton = ttk.Button(self, text="Upload File", command= lambda: upload_file(docxDisplay, 1))
        uploadButton.grid(row=4,column=0)

        homeButton = ttk.Button(self, text="Home", command= lambda: controller.show_frame(StartPage))
        homeButton.grid(row=4, columnspan=2)

class LocalChecker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Check for similarities with documents on your computer", font = LARGE_FONT)
        label.grid(row=0, columnspan=2)

        #TODO: Find a way to set the position of the textbox
        docxDisplay = tk.Text(self, height = 25, width = 50)
        docxDisplay.grid(row=1, column =0, rowspan=2)

        #Results Display
        scoreDisplay = tk.Text(self, height = 4, width = 50)
        scoreDisplay.grid(row=1,column=1)

        #Similar Links
        docxDisplay2 = tk.Text(self, height = 20, width = 50)
        docxDisplay2.grid(row=2, column=1)

        uploadButton1 = ttk.Button(self, text="Upload File 1", command= lambda: upload_file(docxDisplay, 1))
        uploadButton1.grid(row=4,column=0)

        uploadButton2 = ttk.Button(self, text="Upload File 2", command= lambda: upload_file(docxDisplay2, 2))
        uploadButton2.grid(row=4,column=1)

        checkButton = ttk.Button(self, text="Check Similarity", command= lambda: run_local_check(scoreDisplay, DOC_SOURCE, DOC_SOURCE2))
        checkButton.grid(row=4, columnspan=2)

        homeButton = ttk.Button(self, text="Home", command= lambda: controller.show_frame(StartPage))
        homeButton.grid(row=5, columnspan=2)

        #Other todo: Optimize the search engine, fix the scrapy bug, set output to be limited to have no digits, scroll bar, and progress bar

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        button = ttk.Button(self, text="Check for similarities online", command= lambda: controller.show_frame(OnlineChecker))
        button.pack(pady=30, padx=30)

        button1 = ttk.Button(self, text="Check for similarities ", command= lambda: controller.show_frame(LocalChecker))
        button1.pack(pady=30, padx=30)

app = DocuBotApp()
app.mainloop()