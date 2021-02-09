import sys, re

IDCounter = 1
TXTCounter = 1
IDArray = []
TXTArray = []
VALArray = []
words = ['SINO', 'FINSI', 'REPITE', 'VECES','PROGRAMA', 'FINPROG', 'SI', 'ENTONCES', 'FINREP', 'IMPRIME', 'LEE']
relation = ['>', '=', '<', '==']
aritmetic = ['+', '-', '*', '/']

def StrToArr(line):
  word = ''
  isString = False
  arr = []
  for character in line:
      if(isString):
          if(character == '"'):
              isString = False
              word = word + character
              arr.append(word)
              word = ''
          else:
              word = word + character
      else:
          if(character == '"'):
              isString = True
              word = word + character
          elif(character == ' '):
              if(word != ''):
                  arr.append(word)
                  word = ''
          else:
              word = word + character
  if(word != '' and word != '\n'):
      arr.append(word[0:-1])
      word = ''
  return arr

def lexTraduction(word, IDCounter, TXTCounter):
  result = ''
  IDFlag = False
  TXTFlag = False
  if(isWord(word) or isRelation(word)):
      result = word
  elif(isAritmetic(word)):
      result = '[op_ar]'
  elif(isNumeric(word)):
      if(VALArray == []):
          result = '[val]'
          VALArray.append([[word],[octalToDecimal(word)]])
      else:
          bandera = True
          aux = ''
          for i in VALArray:
              if(word == i[0][0]):
                  bandera = False
                  aux = i[1][0]
                  break
          if(bandera):
              result = '[val]'
              VALArray.append([[word],[octalToDecimal(word)]])
          else:
              result = '[val]'
  elif(isText(word)):
      if(TXTArray == []):
          result = '[txt] TX{0:0=2d}'.format(TXTCounter)
          TXTArray.append([[word],['TX{0:0=2d}'.format(TXTCounter)]])
          TXTFlag = True
      else:
          bandera = True
          aux = ''
          for i in TXTArray:
              if(word == i[0][0]):
                  bandera = False
                  aux = i[1][0]
                  break
          if(bandera):
              result = '[txt] TX{0:0=2d}'.format(TXTCounter)
              TXTArray.append([[word],['TX{0:0=2d}'.format(TXTCounter)]])
              TXTFlag = True
          else:
              result = '[id] ' + aux
  else:
      if(IDArray == []):
          result = '[id] ID{0:0=2d}'.format(IDCounter)
          IDArray.append([[word],['ID{0:0=2d}'.format(IDCounter)]])
          IDFlag = True
      else:
          bandera = True
          aux = ''
          for i in IDArray:
              if(word == i[0][0]):
                  bandera = False
                  aux = i[1][0]
                  break
          if(bandera):
              result = '[id] ID{0:0=2d}'.format(IDCounter)
              IDArray.append([[word],['ID{0:0=2d}'.format(IDCounter)]])
              IDFlag = True
          else:
              result = '[id] ' + aux
  return [result, IDFlag, TXTFlag]
  
def octalToDecimal(number):
  result = 0
  counter = 0
  for digit in number:
      result += int(digit) * pow(8, (len(number) -1) - counter)
      counter += 1
  return str(result)

def isAritmetic(word):
  flag = False
  for token in aritmetic:
      if(word == token):
          flag = True
  return flag
  
def isNumeric(word):
  flag = False
  if(re.fullmatch('[0-8]+', word)):
    flag = True
  return flag

def isID(word):
  aux = word
  flag = False
  if(re.fullmatch('[a-zA-Z][a-zA-Z0-9]+', aux)):
    flag = True
  if(len(aux) > 16):
      aux = aux[0:17]
  return [flag, aux]

def isRelation(word):
  flag = False
  for token in relation:
      if(word == token):
          flag = True
  return flag
    
def isWord(word):
  flag = False
  for token in words:
      if(word == token):
          flag = True
  return flag
    
def isText(word):
  flag = False
  if(re.fullmatch('"[a-zA-Z0-9\s]+"', word)):
    flag = True
  return flag
    
def isAnyToken(line):
  flag = True
  arr = StrToArr(line)
  for word in arr:
      if(not(isToken(word))):
          flag = False
  return [flag, arr]

def isToken(word):
  flag = False
  if(isWord(word) or isRelation(word) or isAritmetic(word) or isText(word) or isNumeric(word) or isID(word)[0]):
    flag = True
  return flag

# PROGRAMA 
if(sys.argv[1].split('.')[1] == 'mio'):
    sinFile = open(sys.argv[1].split('.')[0]+ '.sim', 'wt')
    mainFile = open(sys.argv[1])
    lexFile = open(sys.argv[1].split('.')[0] + '.lex', 'wt')
    for i in mainFile:
        if(i[0] == '#'):
          pass
        else:
            resultados = isAnyToken(i)
            if(resultados[0]):
                for palabra in resultados[1]:
                    respuesta = lexTraduction(palabra, IDCounter, TXTCounter)
                    if(respuesta[1] == True):
                        IDCounter += 1
                    elif(respuesta[2] == True):
                        TXTCounter += 1
                    lexFile.write(respuesta[0] + '\n')

            else:
                print('A word may be not be a token')
                break

    sinFile.write('IDS: \n')
    for i in IDArray:
        sinFile.write(i[0][0] + ', ' + i[1][0] + '\n')
    sinFile.write('\nTXT:\n')
    for i in TXTArray:
        sinFile.write(i[0][0] + ', ' + i[1][0] + '\n')
    sinFile.write('\nVAL:\n')
    for i in VALArray:
        sinFile.write(i[0][0] + ', ' + i[1][0] + '\n')

    lexFile.close()
    sinFile.close()
    mainFile.close()
else:
    print('ERROR')