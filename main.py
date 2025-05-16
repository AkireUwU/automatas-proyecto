import tkinter as tk
from tkinter import ttk
from analizadores import analizar_lexico, analizar_sintaxis, analizar_semantico

#from analizador_sintactico import analizar_sintactico

root = tk.Tk()
root.title("Analizador Lexico, Sintactico y Semantico")
root.config(width=800, height=600)


#crear una ventana de texto para el codigo fuente
codigo_texto = tk.Text(root, height=10, width=60)
codigo_texto.pack(pady=10)

#Creacion de un boton para la ejecucion del analizador
def analizador_lexico():
    
    #Obtener codigo escrito en el area de texto
    codigo = codigo_texto.get("1.0", tk.END)
    #Realizar el analisis lexico
    tokens = analizar_lexico(codigo)

    #Mostrar resultados en el area de texto de resultados
    resultados_texto.delete("1.0", tk.END)  # Limpiar resultados anteriores
    
    if tokens:
        #Mostrar los tokens en una tabla simple
        for token in tokens:
            if token[0] == 'ERROR':
                resultados_texto.insert(tk.END, f"ERROR: {token[1]} en la línea {token[2]}, columna {token[3]}\n")
                return
            tipo, valor, linea, columna = token
            resultados_texto.insert(tk.END, f"{tipo:25} {valor:15} {linea: 5} {columna:5}\n")
    else:
        resultados_texto.insert(tk.END, "No se encontraron tokens")



def analizador_sintactico():
    codigo = codigo_texto.get("1.0", tk.END)
    errores = analizar_sintaxis(codigo)

    resultados_texto.delete("1.0", tk.END)

    if errores:
        for error in errores:
            resultados_texto.insert(tk.END, error + "\n")
    else:
        resultados_texto.insert(tk.END, "No se encontraron errores de sintaxis.\n")

def analizador_semantico():
    codigo = codigo_texto.get("1.0", tk.END)
    errores = analizar_semantico(codigo)

    resultados_texto.delete("1.0", tk.END)

    if errores:
        for err in errores:
            resultados_texto.insert(tk.END, err + "\n")
    else:
        resultados_texto.insert(tk.END, "No se encontraron errores semánticos.\n")

analizar_button1 = tk.Button(root, text="Analizador Léxico", command = analizador_lexico)
analizar_button2 = tk.Button(root, text="Analizador Sintactico", command = analizador_sintactico)
analizar_button3 = tk.Button(root, text="Analizador Semantico", command = analizador_semantico)
analizar_button1.pack(pady=10)
analizar_button2.pack(pady=10)
analizar_button3.pack(pady=10)

#Crear una area de texto para mostrar los resultados (tabla de tokens)
resultados_texto = tk.Text(root, height=40, width=60)
resultados_texto.pack(pady=10)

root.mainloop()
