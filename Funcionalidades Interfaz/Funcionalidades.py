import os

raiz = Tk()

def salir(): #SALIR DEL PROGRAMA
    value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
    if value :
        raiz.destroy()

def cerrarDoc(): # CERRAR UN DOCUMENTO
    value = messagebox.askretrycancel("Reintentar", "No es posible cerrar el documento.")
    if value == False:
        raiz.destroy()

archivo = ""   #PATH DEL ARCHIVO EN MEMORIA

def nuevo():   #NUEVO ARCHIVO
    global archivo
    editor.delete(1.0, END)
    archivo = ""

def abrir():       #ABRIR ARCHIVO
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/")

    entrada = open(archivo)
    content = entrada.read()

    editor.delete(1.0, END)
    for s in recorrerInput(content):
        editor.insert(INSERT, s[1], s[0])
    entrada.close()
    lineas()

def guardarArchivo():   #GUARDAR 
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w")
        guardarc.write(editor.get(1.0, END))
        guardarc.close()

def guardarComo():      #GUARDAR COMO
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/")
    fguardar = open(guardar, "w+")
    fguardar.write(editor.get(1.0, END))
    fguardar.close()
    archivo = guardar

def openPDF():      #ABRIRI UN PDF
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'ast.pdf')
    os.startfile(direcc)

def lineas(*args):      #ACTUALIZAR LINEAS
    lines.delete("all")

    cont = editor.index("@1,0")
    while True :
        dline= editor.dlineinfo(cont)
        if dline is None: 
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        lines.create_text(2,y,anchor="nw", text=strline, font = ("Arial", 15))
        cont = editor.index("%s+1line" % cont)

def posicion(event):    #ACTUALIZAR POSICION
    pos.config(text = "[" + str(editor.index(INSERT)).replace(".",",") + "]" )




def recorrerInput(i):  #Funcion para obtener palabrvas reservadas, signos, numeros, etc
    lista = []
    val = ''
    counter = 0
    while counter < len(i):
        if re.search(r"[a-z0-9]", i[counter]):
            val += i[counter]
        elif i[counter] == "$":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = "$"
        elif i[counter] == "<" or i[counter] == ">" or i[counter] == "+" or i[counter] == "-" or i[counter] == "*" or i[counter] == "/" or i[counter] == "=" or i[counter] == "!" or i[counter] == "~" or i[counter] == "%" or i[counter] == "^" or i[counter] == "|":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            l = []
            l.append("operacion")
            l.append(i[counter])
            lista.append(l)
        elif i[counter] == "\"":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\"":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1
        elif i[counter] == "\'":
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            val = i[counter]
            counter += 1
            while counter < len(i):
                if i[counter] == "\'":
                    val += i[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += i[counter]
                counter += 1
        else:
            if len(val) != 0:
                l = []
                l.append("variable")
                l.append(val)
                lista.append(l)
                val = ''
            l = []
            l.append("signo")
            l.append(i[counter])
            lista.append(l)
        counter +=1
    for s in lista:
        if s[1] == 'int' or s[1] == 'float' or s[1] == 'char' or s[1] == 'print' or s[1] == 'main' or s[1] == 'goto' or s[1] == 'unset' or s[1] == 'exit' or s[1] == 'if' or s[1] == 'abs' or s[1] == 'xor' or s[1] == 'array' or s[1] == 'read':
            s[0] = 'reservada'
        elif s[1][0] != "$":
            if s[0] == 'variable':
                s[0] = 'etiqueta'
    return lista



#ELEMENTOS

frame = Frame(raiz, bg="gray60")
canvas = Canvas(frame, bg="gray60")
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollbar2 = Scrollbar(frame, orient=HORIZONTAL, command=canvas.xview)
scrollable_frame = Frame(canvas, bg="gray60")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, width = 1250, height = 700)



pos = ttk.Label(scrollable_frame, text = cont)
pos.grid(column = 1, row = 1)
editor = scrolledtext.ScrolledText(scrollable_frame, undo = True, width = 60, height = 15)
lines = Canvas(scrollable_frame, width = 30, height = 345, background = 'gray60')

#CAMBIO DE COLORES
editor.tag_config('reservada', foreground='red')
editor.tag_config('variable', foreground='maroon4')
editor.tag_config('string', foreground='green2')
editor.tag_config('operacion', foreground='gold')
editor.tag_config('etiqueta', foreground='purple')

# FUNCIONALIDADES EN EL TECLADO

editor.grid(column = 1, row = 3, pady = 25, padx = 0)
lines.grid(column = 0, row = 3)

editor.bind('<Return>', lineas)
editor.bind('<BackSpace>', lineas)
editor.bind('<<Change>>', lineas)
editor.bind('<Configure>', lineas)
editor.bind('<Motion>', lineas)
editor.bind('<KeyPress>', posicion)
editor.bind('<Button-1>', posicion)

frame.grid(sticky='news')
canvas.grid(row=0,column=1)
scrollbar.grid(row=0, column=2, sticky='ns')
scrollbar2.grid(row=1, column=1, sticky='ns')