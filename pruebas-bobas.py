# # ANALIZADOR LEXICO
# # se hara uso de expresiones regulares para la
# # identificacion de tokens

# import re

# #Expresiones regulares para los tokens
# token_re = [
#         #tipo                  #patron
#     ('PALABRA_RESERVADA', r'\b(if|else|elif|while|for|in|def|return|import|from|try|except|finally|class|lambda|global|nonlocal|with|assert)\b'), #palabras reservadas de python
#     ('IDENTIFICADOR', r'\b[_a-zA-Z][A-Za-z0-9_]*\b'), #identificadores 
#     ('ENTERO', r'\b\d+\b'), #numeros enteros
#     ('FLOTANTE', r'\b\d+\.\d+\b'), #numeros flotantes
#     ('OPERADOR_ARITMETICO', r'[+\-*/%<>=!&|^]'), #operadores
#     ('DELIMITADOR', r'[\(\)\[\]\{\}\.,;]'), #delimitadores
#     ('COMENTARIO', r'#.*'), #comentarios
#     ('ESPACIO', r'\s+'), #espacios en blanco
# ]

# # Funcion que realiza el analisis lexico
# def analizar_lexico(codigo):
#     #Lista para almacenar los tokens
#     tokens = []
#     print("Lista vacia ->", tokens)
#     #Almacena una lista de subcadenas, divididas por un salto de linea
#     lineas = codigo.split('\n')
#     print("Lista de lineas ->", lineas)

#     #Se recorre cada elemento de la lista de lineas
#     for i, linea in enumerate(lineas):
#         print("posicion -> ", i, "Linea de codigo -> ", linea)
#         #Aqui comiensa el analisis lexico de cada linea.
        
#         #Se inicializa una variable columna en 0. 
#         #Esta variable rastrea la posicion del caracter actual
#         #dentro de la linea que se esta analizando
#         columna = 0
#         while columna < len(linea):
#             print("columna -> ", columna,"tamanio -> ",len(linea), "linea -> ", linea[columna:])
#             for tipo, patron in token_re:
#                 regex = re.match(patron, linea[columna:])
#                 print("patron ->", patron, "linea -> ", linea[columna:], "regex -> ", regex)
#                 if regex:
#                     valor = regex.group(0)
                    
#                     if tipo != 'ESPACIO': #Ignorar espacios
#                         tokens.append(("\n\nTipo de token -> ", tipo, "lexema ->", valor,"patron -> ",patron, "Fila -> ",i + 1, "columna ->", columna + 1))
#                         print("token -> ", tokens[-1])
#                     columna += len(valor)
#                     break
#             else:
#                 #Si no se encuentra ningun token valido
#                 tokens.append(('ERROR', linea[columna], i + 1, columna + 1))
#                 columna += 1
#     return tokens

# codigo = "a = 1\nb = 2.5"
# analizar_lexico(codigo)


for x in (5):
    print(i)