import sys, re

tokens = {
  'words': ['PROGRAMA', 'FINPROG', 'SI', 'ENTONCES', 'SINO', 'FINSI', 'REPITE', 'VECES', 'FINREP', 'IMPRIME', 'LEE']
  'relation': ['>', '<', '==', '=']
  'aritmetic': ['+', '-', '*', '/']
}

contadorID = 1
contadorTXT = 1

arregloID = []
arregloTXT = []
arregloVAL = []

def dividirString(linea):
    # Creamos un arreglo
    arr = []

    # Creamos el contenedor para las palabras
    palabra = ''

    # Creamos las banderas
    esString = False

    # Iteramos letra por letra de la linea
    for letra in linea:
        if(esString):
            if(letra == '"'):
                esString = False
                palabra = palabra + letra
                arr.append(palabra)
                palabra = ''
            else:
                palabra = palabra + letra
        else:
            if(letra == '"'):
                esString = True
                palabra = palabra + letra
            elif(letra == ' '):
                if(palabra != ''):
                    arr.append(palabra)
                    palabra = ''
            else:
                palabra = palabra + letra

    if(palabra != '' and palabra != '\n'):
        arr.append(palabra[0:-1])
        palabra = ''

    # Retornamos el arreglo
    return arr

def esReservada(palabra):
    # Creamos la bandera 
    default = False

    # Verificamos si no es un token
    for token in palabrasReservadas:
        if(token == palabra):
            default = True

    # Retornamos la bandera
    return default

def esRelacional(palabra):
    # Creamos la bandera 
    default = False

    # Verificamos si no es un token
    for token in operadoresRelacionales:
        if(token == palabra):
            default = True

    # Retornamos la bandera
    return default
    
def esAritmetico(palabra):
    # Creamos la bandera 
    default = False

    # Verificamos si no es un token
    for token in operadoresAritmeticos:
        if(token == palabra):
            default = True

    # Retornamos la bandera
    return default
    
def esLiteralTexto(palabra):
    # Verificamos si es token con la expresión regular
    default = True if re.fullmatch('"[a-zA-Z0-9\s]+"', palabra) else False

    # Retornamos la bandera
    return default

def esLiteralNumerica(palabra):
    # Verificamos si es token con la expresión regular
    default = True if re.fullmatch('[0-8]+', palabra) else False

    # Retornamos la bandera
    return default

def esIdentificador(palabra):
    # Creamos una copia de la palabra
    palabraFinal = palabra

    # Verificamos si es token con la expresión regular, que dice que debe empezar con alguna letra
    default = True if re.fullmatch('[a-zA-Z][a-zA-Z0-9]+', palabraFinal) else False

    # Verificamos si no es mayor a 16 caracteres
    if(len(palabraFinal) > 16):
        palabraFinal = palabraFinal[0:17]

    # Retornamos la bandera
    return [default, palabraFinal]

def esToken(palabra):
    # Creamos nuestra bandera
    default = False

    # Verificamos si la palabra es token
    if(
        esReservada(palabra) or 
        esRelacional(palabra) or 
        esAritmetico(palabra) or 
        esLiteralTexto(palabra) or 
        esLiteralNumerica(palabra) or 
        esIdentificador(palabra)[0]
    ):
        default = True

    # Retornamos la bandera
    return default
    
def verificarTokens(linea):
    # Se declara la bandera por defecto
    default = True

    # Dividimos el string en un arreglo de palabras
    arr = dividirString(linea)

    # Checa palabra por palabra para ver si todas son tokens
    for palabra in arr:
        # Checar si no es un token
        if(not(esToken(palabra))):
            default = False

    # Se retorna la bandera
    return [default, arr]
    

def aDecimal(numero):
    resultado = 0
    contador = 0

    # Convertimos a decimal
    for digito in numero:
        resultado += int(digito) * pow(8, (len(numero) -1) - contador)
        contador += 1

    # Retornamos el resultado
    return str(resultado)


def traducirALex(palabra, cID, cTXT):
    # Creamos la variable para guardar la traducción
    traduccion = ''

    # Creamos las banderas por si usamos el cID o el cTXT
    bID = False
    bTXT = False

    if(esReservada(palabra) or esRelacional(palabra)):
        traduccion = palabra
    elif(esAritmetico(palabra)):
        traduccion = '[op_ar]'
    elif(esLiteralNumerica(palabra)):
        if(arregloVAL == []):
            traduccion = '[val]'
            arregloVAL.append([[palabra],[aDecimal(palabra)]])
        else:
            # Creamos una bandera
            bandera = True
            aux = ''

            # Checamos si la palabra es única
            for i in arregloVAL:
                if(palabra == i[0][0]):
                    bandera = False
                    aux = i[1][0]
                    break
            
            if(bandera):
                traduccion = '[val]'
                arregloVAL.append([[palabra],[aDecimal(palabra)]])
            else:
                traduccion = '[val]'
    elif(esLiteralTexto(palabra)):
        if(arregloTXT == []):
            traduccion = '[txt] TX{0:0=2d}'.format(contadorTXT)
            arregloTXT.append([[palabra],['TX{0:0=2d}'.format(contadorTXT)]])
            bTXT = True
        else:
            # Creamos una bandera
            bandera = True
            aux = ''

            # Checamos si la palabra es única
            for i in arregloTXT:
                if(palabra == i[0][0]):
                    bandera = False
                    aux = i[1][0]
                    break

            if(bandera):
                traduccion = '[txt] TX{0:0=2d}'.format(contadorTXT)
                arregloTXT.append([[palabra],['TX{0:0=2d}'.format(contadorTXT)]])
                bTXT = True
            else:
                traduccion = '[id] ' + aux
    else:
        if(arregloID == []):
            traduccion = '[id] ID{0:0=2d}'.format(contadorID)
            arregloID.append([[palabra],['ID{0:0=2d}'.format(contadorID)]])
            bID = True
        else:
            # Creamos una bandera
            bandera = True
            aux = ''

            # Checamos si la palabra es única
            for i in arregloID:
                if(palabra == i[0][0]):
                    bandera = False
                    aux = i[1][0]
                    break
            
            if(bandera):
                traduccion = '[id] ID{0:0=2d}'.format(contadorID)
                arregloID.append([[palabra],['ID{0:0=2d}'.format(contadorID)]])
                bID = True
            else:
                traduccion = '[id] ' + aux

    # Retornamos la traducción
    return [traduccion, bID, bTXT]

if(sys.argv[1].split('.')[1] == 'mio'):
    # Abrir el archivo y creamos el '.lex' y el '.sim'
    arch = open(sys.argv[1])
    archLex = open('./output/' + sys.argv[1].split('.')[0] + '.lex', 'wt')
    archSim = open('./output/' + sys.argv[1].split('.')[0]+ '.sim', 'wt')

    # Leemos cada linea del archivo
    for i in arch:
        # Verificamos que no sea un comentario
        if(i[0] != '#'):
            # Verificamos que todas las palabras de la linea, sean un token
            resultados = verificarTokens(i)
            if(resultados[0]):
                # Escribe en el archivo '.lex'
                for palabra in resultados[1]:
                    respuesta = traducirALex(palabra, contadorID, contadorTXT)
                    if(respuesta[1] == True):
                        contadorID += 1
                    elif(respuesta[2] == True):
                        contadorTXT += 1
                    archLex.write(respuesta[0] + '\n')

            else:
                print('ERROR: Se encontró una palabra que no es un token')
                break

    archSim.write('IDS \n')
    for i in arregloID:
        archSim.write(i[0][0] + ', ' + i[1][0] + '\n')
    archSim.write('\nTXT\n')
    for i in arregloTXT:
        archSim.write(i[0][0] + ', ' + i[1][0] + '\n')
    archSim.write('\nVAL\n')
    for i in arregloVAL:
        archSim.write(i[0][0] + ', ' + i[1][0] + '\n')

    # Cerramos los archivos
    archLex.close()
    archSim.close()
    arch.close()
else:
    print('Formato de archivo erróneo.')