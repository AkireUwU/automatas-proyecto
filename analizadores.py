# ANALIZADOR LEXICO
# se hara uso de expresiones regulares para la
# identificacion de tokens
#nota nueva ajsdjasd
import re
import ast
import builtins
#Expresiones regulares para los tokens
token_re = [
    ('COMENTARIO', r'#.*'),  # comentarios
    ('CADENA', r'(\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\')'),  # cadenas de texto
    ('INVALIDO', r'(:\s?=|\+\+|--|=>|<>|@|~|<<|>>|::|&|`)+'), # símbolos inválidos
    ('PALABRA_RESERVADA', r'\b(if|else|elif|while|for|in|def|return|import|from|try|except|finally|class|lambda|global|nonlocal|with|assert|print)\b'),
    ('BOOLEANO', r'\b(True|False)\b'),
    ('NULO', r'\b(None)\b'),
    ('IDENTIFICADOR', r'\b[_a-zA-Z][A-Za-z0-9_]*\b'),
    ('FLOTANTE', r'\b\d+\.\d+\b'),
    ('ENTERO', r'\b\d+\b'),
    ('OPERADOR_ARITMETICO', r'[+\-*/%<>=!&|^]'),
    ('DELIMITADOR', r'[\(\)\[\]\{\}\.,:;]'),
    ('ESPACIO', r'\s+'),
]


# Funcion que realiza el analisis lexico
def analizar_lexico(codigo):
    #Lista para almacenar los tokens
    tokens = []
    #print("Lista vacia ->", tokens)
    #Almacena una lista de subcadenas, divididas por un salto de linea
    lineas = codigo.split('\n')
    #print("Lista de lineas ->", lineas)

    #Se recorre cada elemento de la lista de lineas
    for i, linea in enumerate(lineas):
        #print("posicion -> ", i, "Linea de codigo -> ", linea)
        #Aqui comiensa el analisis lexico de cada linea.
        
        #Se inicializa una variable columna en 0. 
        #Esta variable rastrea la posicion del caracter actual
        #dentro de la linea que se esta analizando
        columna = 0
        while columna < len(linea):
            #print("columna -> ", columna,"tamanio -> ",len(linea), "linea -> ", linea[columna:])
            for tipo, patron in token_re:
                regex = re.match(patron, linea[columna:])
                #print("patron ->", patron, "linea -> ", linea[columna:], "regex -> ", regex)
                if regex:
                    valor = regex.group(0)
                    
                    if tipo != 'ESPACIO': #Ignorar espacios
                        tokens.append((tipo,valor,i + 1, columna + 1))
                        print("token -> ", tokens[-1])
                    columna += len(valor)
                    break
            else:
                #Si no se encuentra ningun token valido
                tokens.append(('ERROR', linea[columna], i + 1, columna + 1))
                columna += 1
    return tokens



def analizar_sintaxis(codigo):
    errores = []
    lineas = codigo.split('\n')

    #variable para almacenar variables definidas en el ciclo for
    for_vars = {}

    for num_linea, linea in enumerate(lineas, start=1):
        stripped = linea.strip()
        
        # Ignorar líneas vacías o comentarios
        if not stripped or stripped.startswith('#'):
            continue

        # Verifica si hay un "for" mal formado
        if stripped.startswith("for"):
            # Verifica si el ciclo 'for' está bien formado
            patron_for = r'^for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+.+:$'
            if not re.match(patron_for, stripped):
                errores.append(f"Error de sintaxis en línea {num_linea}: estructura 'for' inválida.")
            else:
                #extraer la variable del ciclo (la que esta antes del in)
                var_for = stripped.split()[1]
                #guardar la variable del ciclo en el diccionario
                for_vars[num_linea] = var_for
            

            # Verifica si contiene 'in' y termina con ':'
            if "in" not in stripped:
                errores.append(f"Error de sintaxis en línea {num_linea}: 'for' debe contener 'in'")
            if not stripped.endswith(":"):
                errores.append(f"Error de sintaxis en línea {num_linea}: 'for' debe terminar en ':'")
            # Verifica si el identificador después de 'for' es válido
            tokens = stripped.split()
            if len(tokens) < 4 or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tokens[1]):
                errores.append(f"Error de sintaxis en línea {num_linea}: identificador después de 'for' no válido.")
            
            # Verifica que haya algo después de 'in'
            if len(tokens) < 4 or tokens[3] == 'in':
                errores.append(f"Error de sintaxis en línea {num_linea}: falta un objeto iterable después de 'in'.")
                
        elif num_linea in for_vars:
            var_for = for_vars[num_linea]
            if var_for not in stripped and print in stripped:
                errores.append(f"Error de sintaxis en linea{num_linea}: Se esta utilizando una variable no definida")
        
            # Verifica llamadas a funciones como print()
        if '(' in linea or ')' in linea:
                if linea.count('(') != linea.count(')'):
                    errores.append(f"Línea {num_linea}: paréntesis no balanceado")


    return errores

def analizar_semantico(codigo):
   
      #Registra variables definidas en asignaciones.
      #Marca error si se usa una variable no declarada previamente.
      #Captura SyntaxError del parser AST.
    
    #Devuelve lista de cadenas con los errores semánticos encontrados.
    
    errores = []
    try:
        tree = ast.parse(codigo)
    except SyntaxError as e:
        errores.append(f"Error semántico (parsing) línea {e.lineno}: {e.msg}")
        return errores

    symbol_table = set()
    errores_sem = []

    class Semantico(ast.NodeVisitor):
        def visit_Assign(self, node):
            # sólo manejamos simples "x = ..." 
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbol_table.add(target.id)
            # procesar el resto del árbol para posibles usos
            self.generic_visit(node.value)

        def visit_Name(self, node):
            # si es lectura (Load), verificar definición previa
            if isinstance(node.ctx, ast.Load):
                if node.id not in symbol_table and node.id not in dir(builtins):
                    errores_sem.append(
                        f"Error semántico línea {node.lineno}: "
                        f"variable '{node.id}' no definida"
                    )
            # continuar el recorrido
            self.generic_visit(node)

    Semantico().visit(tree)
    return errores_sem
