import sys, re

file = open('{}'.format(sys.argv[1]))

syn = {
  'RES': ['PROGRAMA', 'FINPROG', 'SI', 'ENTONCES', 'SINO', 'FINSI', 'REPITE', 'VECES', 'FINREP', 'IMPRIME', 'LEE'],
  'REL': ['>', '<', '==', '='],
  'ARI': ['+', '-', '*', '/']
}

def toArr(str):
  arr = []
  currStr = '' 
  flag = False
  for i in str:
    if(i == '\n'):
      if(currStr != ''):
        arr.append(currStr)
    elif(i != ' ' and i != '"'):
      currStr = currStr + i
    else:
      if(flag):
        if(i != '"'):
          currStr = currStr + i
        else:
          flag = False
          currStr = currStr + i
          arr.append(currStr)
          currStr = ''
      else:
        if(i == ' '):
          if(currStr != ''):
            arr.append(currStr)
            currStr = ''
        else:
          flag = True
          currStr = currStr + i
  return arr

def isRES(word):
  flag = False
  for i in syn['RES']:
    if(word == i):
      flag = True
  return flag

def isREL(word):
  flag = False
  for i in syn['REL']:
    if(word == i):
      flag = True
  return flag

def isARI(word):
  flag = False
  for i in syn['ARI']:
    if(word == i):
      flag = True
  return flag

def isLine(arr):
  flag = True
  for i in arr:
    # Check if it is any of the reserved words
    if(not(isAny(i))):
      flag = False
  return flag

def isDefault(word):
  flag = isRES(word) or isREL(word) or isARI(word)
  return flag

def isAny(word):
  flag = isRES(word) or isREL(word) or isARI(word) or word == '=' or isID(word) or isNumeric(word) or isText(word)
  return flag

def isID(word):
  pattern = '[A-Za-z][A-Za-z0-9]+'
  flag = re.match(pattern, word)  
  return flag

def isNumeric(word):  
  pattern = '[0-8]+'
  flag = re.match(pattern, word) 
  return flag

def isText(word):
  pattern = ('"[\sA-Za-z0-9]+"')
  flag = re.match(pattern, word)
  return flag

def octalToDecimal(octal):
  decimal = 0
  position = 0
  octal = octal[::-1]
  for digit in octal:
    value = int(digit)
    num = int(8 ** position)
    equivalence = int(num * value)
    decimal += equivalence
    position += 1
  return decimal
#------------------------------------------------------------------------------------------------

stack=['#']
def isEmpty():
  return stack==['#']
def push(item):
  stack.append(item)
def pop():
  return stack.pop()
def lastItem():
  return stack[len(stack)-1]

def checkOP_ARstructure(fPROG,fOP_AR,fREP):
  if (fOP_AR and '[op_ar]' in line) or (fOP_AR and '[op_ar]' in line and fREP and fPROG):
    push('ELEM')
    return True

def checkNext(line,mainStack):
  next = mainStack.index(line)+1
  if not(next >= len(mainStack)):
    if '[id]' in mainStack[next] or 'SI' in mainStack[next] or 'REPITE' in mainStack[next] or 'IMPRIME' in mainStack[next] or 'LEE' in mainStack[next]:
      push('SENTS')
  
#-------------------------------------------------------------------
#VARIABLES DEL PROGRAMA

def checkPROGstructure(line,fPROG,fERROR):
  if 'PROGRAMA' in line and not(fPROG) and isEmpty():
    fPROG=True
    push('FINPROG')  
    push('SENTS')
    push('[id]')
    return True
  if not(fPROG) and isEmpty():
    print('COMPILACION ERRONEA')
    fERROR=True
    return False
  if '[id]' in line and lastItem()=='[id]' and fPROG:
    if not(fERROR):
      pop()
      return True
    else:
      print('COMPILACION ERRONEA')
      fERROR=True
      return False
  if 'FINPROG' in line and fPROG and lastItem()=='FINPROG':
    fPROG=False
    pop()
    return True  

def checkSENTSstructure():
  if lastItem()=='SENTS':
    pop()
    push('SENT')      

def checkCOMPARAstructure(line,fOP_REL,fSI,fERROR):
  if (lastItem()=='COMPARA' and fSI) or fOP_REL:
    if '[id]' in line:      
      pop()
      fOP_REL=True
      push('[op_rel]')
      return True
    elif lastItem()=='[op_rel]' and ('<' in line or '>' in line) and fSI and fOP_REL:    
      fOP_REL=False
      pop()
      push('ELEM')      
    else:
      print('COMPILACION ERRONEA')
      fERROR=True
      return False

def checkSENTstructure(line,fSI,fREP,fIMP,fLEE,fID,fPROG,fERROR,mainStack):
  if lastItem()=='SENT' or fID or fSI or fREP or fIMP or fLEE:
    if ('=' in line and lastItem()=='=' and fID and fPROG) or fID and lastItem()=='SENT' and not(fIMP):
      pop()      
      fID=False
    elif ('[id]' in line and lastItem()=='SENT') and not(fIMP):
      fID=True
      pop()      
      push('ELEM')
      push('=')
      return True
    elif 'SI' in line or fSI and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line) and not('REPITE' in line):      
      if 'SI' in line and fPROG and lastItem()=='SENT':
        pop()
        fSI=True
        push('FINSI')
        push('SENTS')     
        push('ENTONCES')
        push('COMPARA')   
        return True
      if lastItem()=='ENTONCES' and fSI and fPROG:
        if 'ENTONCES' in line:          
          pop()
          return True
        else:
          print('COMPILACION ERRONEA')
      if 'SINO' in line and fSI and fPROG:    
        push('SENTS')      
        return True
      if fSI and lastItem()=='FINSI' and fPROG:
        if 'FINSI' in line:
          pop()
          checkNext(line,mainStack)
          if not('FINSI' in stack):
            fSI=False
            return True
          else:
            return True
        else:
          print('COMPILACION ERRONEA')
    elif 'REPITE' in line or fREP and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line): 
      if 'REPITE' in line and fPROG and lastItem()=='SENT':
        pop()
        fREP=True
        push('FINREP')
        push('SENTS')     
        push('VECES')  
        push('ELEM')      
        return True 
      if lastItem()=='VECES' and fREP and fPROG:
        if 'VECES' in line:          
          pop()
          return True
        else:
          print('COMPILACION ERRONEA')
      if lastItem()=='FINREP' and fREP and fPROG:
        if 'FINREP' in line:
          pop()
          checkNext(line,mainStack)
          if not('FINREP' in stack):
            fREP=False
            return True
          else:
            return True
        else:
          print('COMPILACION ERRONEA')
          return False
    elif 'IMPRIME' in line or fIMP:
      if 'IMPRIME' in line and fPROG and lastItem()=='SENT':
        pop()
        fIMP=True
        push('IMPRIME')
        return True
      if lastItem()=='IMPRIME' and fIMP:
        if '[text]' in line:
          fIMP=False
          pop()
          checkNext(line,mainStack)
          return True
        elif '[id]' in line or '[val]' in line:
          pop()
          push('ELEM')     
          fIMP=False
          pop()
          checkNext(line,mainStack)
        else:
          print('COMPILACION ERRONEA')
          fERROR=True
          return False
    elif 'LEE' in line or fLEE: 
      if 'LEE' in line and fPROG and lastItem()=='SENT':        
        pop()   
        fLEE=True
        push('LEE')
        return True
      if lastItem()=='LEE' and fLEE:
        if '[id]' in line:              
          pop()
          fLEE=False                 
          checkNext(line,mainStack)
          return True
        else:
          print('COMPILACION ERRONEA')
          fERROR=True
          return False
    else:
      print(line)
      print(lastItem())
      print('COMPILACION ERRONEA')      
      return False  
  else:
    print('COMPILACION ERRONEA')
    return False  

def checkELEMstructure(line,fSI,fPROG,fID,fERROR,mainStack,cont):  
  if lastItem()=='ELEM':
    if '[val]' in line or '[id]' in line:
      pop()
      if not(fSI):
        checkNext(line,mainStack)      
      next = cont
      if '[op_ar]' in mainStack[next] and fPROG:   
        fOP_AR=True
        return True
      else:
        fID=False
        return True
    else:
      print('COMPILACION ERRONEA')
      fERROR=True
      return False

fPROG=False
fID=False
fSI=False
fREP=False
fIMP=False
fLEE=False
fERROR=False
fOP_AR=False
fOP_REL=False

mainStack = []
for item in file:
  print(item, end = '')
  item = item.split()
  mainStack.append(item)
print()

cont=0
for item in mainStack:
  cont+= 1
  print(item)
  print(stack)
  print()

  if checkPROGstructure(item,fPROG,fERROR):
    continue
  else:
    break

  if checkSENTSstructure():
    continue
  else:
    break

  if checkCOMPARAstructure(line,fOP_REL,fSI,fERROR):
    continue
  else:
    break

  if checkOP_ARstructure(fPROG,fOP_AR,fREP):
    continue
  else:
    break

  if checkELEMstructure(line,fSI,fPROG,fID,fERROR,mainStack,cont):
    continue
  else:
    break

  if checkSENTstructure(line,fSI,fREP,fIMP,fLEE,fID,fPROG,fERROR): 
    continue
  else:
    break

if isEmpty() and not(fERROR):
  print('COMPILACION EXITOSA')
else:
  print(stack)
  print('COMPILACION ERRONEA')
