import PySimpleGUI as sg
import re
from tkinter import *
from tkinter import filedialog
import os
variables = []
tokens = [[]]
save = False
number = False
real = False
def check(string):
    global save
    global number
    global real
    if(string in resWord or string in resSimb):
        state = True
    elif(re.search("^[a-zA-Z]\d{1,3}$", string)):
        state = True
        save = True
    elif(re.search("^\d{1,5}$", string)):
        state = True
        number = True
    elif(re.search("^\d{1,5}\.\d{1,3}$", string)):
        state = True
        real = True
        number = False
    else:
        number = False
        save = False
        real = False
        state = False
    return state
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    return filename
def saveFiles():
    filename = filedialog.asksaveasfilename(initialdir = "/", title = "Guardar Archivo", filetypes = (("Text files", "*.txt"),("all files", "*.*")))
    return filename


layout = [[sg.Text("Analizador Lexico")],[sg.Button("Explorar...")], [sg.Multiline(key="texto", size=(70, 40), horizontal_scroll=True), sg.Multiline(key="texto2", size=(70, 40), disabled=True), sg.Table(key="texto3", size=(70, 40), headings=["Token", "ID", "Tipo", "Valor"],auto_size_columns=False,values=variables, max_col_width=20), sg.Table(key="texto4", size=(70, 40), headings=["Token", "ID"],auto_size_columns=False, values=tokens, max_col_width=20)],[sg.Button("Analizaaaar :)"), sg.Button("Guardar ;)")]]
window = sg.Window("Analizador Lexico", layout,size=(1800, 800))
resWord = ("INICIO", "FIN", "ENTERO", "FLOTANTE", "LEER", "IMPRIMIR", "SUM", "RES", "MUL", "DIV")
resSimb = ("(",")","{","}",";", ",", "=")
tknWord = {'INICIO':'tknInicio', 'FIN':'tknFin', 'ENTERO':'tknInt', 'FLOTANTE':'tknFloat', 'LEER':'tknLeer','IMPRIMIR':'tknPrint', 'SUM':'tknSum', 'RES': 'tknRes', 'MUL': 'tknMul', 'DIV': 'tknDiv'}
tknSimb = {'(':'tknParenA', ')':'tknParenB', '{':'tknCorA', '}':'tknCorB', ';': 'tknSemicolon', ',':'tknComa', '.':'tknPunto', '=':'tknAsig'}

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
    elif event == "Analizaaaar :)":
        linea = 1
        variables = []
        tokens = []
        codigo = values["texto"] + "\n"
        print(codigo)
        buffer = ""
        iterator = iter(codigo)
        condition = False
        errOut = ""
        simbolState = False
        count = 0
        for x in iterator:
            if((x != "\n" and x != " " and x not in resSimb and x != "\t")):
                buffer += x
                condition = check(buffer)
            else:
                condition = check(buffer)
                if(condition):
                    if(save):
                        allow = True
                        for c in variables:
                            if(c[1] == buffer):
                                allow = False
                        if(allow):
                            variables.append(["tknVar",buffer,"",""])
                            
                            save = False
                        tokens.append(["tknVar", buffer])
                        save = False
                    elif(number):
                        if(x != "."):
                            tokens.append(["tknNum", buffer])
                            number = False
                        else:
                            buffer += x
                            continue
                        number = False
                    elif(real):
                        tokens.append(["tknReal", buffer])
                        real = False
                    else:
                        tokens.append([tknWord[buffer], buffer])
                    buffer = ""
                else:
                    if(buffer != ""):
                        errOut += ("Error en la linea " + str(linea) +": " + buffer + "\n")
                        buffer = ""
                if(x in resSimb):
                    tokens.append([tknSimb[x], x])
                if(x == "\n"):
                    linea += 1
        window["texto2"].update(errOut,text_color="red")
        errOut =""
        window["texto3"].update(values=variables)
        window["texto4"].update(values=tokens)
    elif(event == "Explorar..."):
        window['texto'].update("")
        route = browseFiles()
        file = open(route,"r")
        try:
            window['texto'].update(file.read())
        except FileNotFoundError:
            None
        file.close()
    elif(event == "Guardar ;)"):
        codigo = ""
        try:
            for x in tokens:
                codigo += "Token: " + x[0] + " Lexema: " + x[1] + "\n"
        except Exception:
            print("")
        #codigo = values["texto"] + "\n"
        ruta = saveFiles()
        file = None
        try:
            file = open(ruta, "w")
        except Exception:
            print('error de apertura')
        # try:
        #     file = open(ruta, "w")
        # except Exception:
        #     print("error de apertura 2")
        file.write(codigo)
        file.close()
        print(os.path.isfile(ruta))
        
window.close()