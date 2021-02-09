import sys
sys.path.append('src/')

from syntax import syn

file = open('{}.lex'.format(sys.argv[1]))


mainStack = []
stack=['#']
def isEmpty():
  return stack==['#']
def push(item):
  stack.append(item)
def pop():
  return stack.pop()
def inspect():
  return stack[len(stack)-1]
def size():
  return len(stack)

def checkOP_ARstructure(fPROG,fOP_AR,fREP):
  #Controlador de op_ar
  if (fOP_AR and '[op_ar]' in line) or (fOP_AR and '[op_ar]' in line and fREP and fPROG):
    push('ELEM')
    return True

#Checar siguiente linea
def checkNext(line):
  next = mainStack.index(line)+1
  if not(next >= len(mainStack)):
    if '[id]' in mainStack[next] or 'SI' in mainStack[next] or 'REPITE' in mainStack[next] or 'IMPRIME' in mainStack[next] or 'LEE' in mainStack[next]:
      push('SENTS')
  
#-------------------------------------------------------------------
#VARIABLES DEL PROGRAMA

def checkPROGstructure(line,fPROG,fERROR):
  #Estructura de PROGRAMA 
  if 'PROGRAMA' in line and not(fPROG) and isEmpty():
    fPROG=True
    push('FINPROG')  
    push('SENTS')
    push('[id]')
    return True
  #Comprobamos que no haya error para continuar
  if not(fPROG) and isEmpty():
    print('ERROR DE INICIO DE PROGRAMA')
    fERROR=True
    break
  if '[id]' in line and inspect()=='[id]' and fPROG:
    if not(fERROR):
      pop()
      return True
    else:
      print('ERROR DE COMPILACION')
      fERROR=True
      break
  if 'FINPROG' in line and fPROG and inspect()=='FINPROG':
    fPROG=False
    pop()
    return True  

def checkSENTSstructure():
  #Variable SENTS
  if inspect()=='SENTS':
    pop()
    push('SENT')    #Metemos variable  

def checkCOMPARAstructure(line,fOP_REL,fSI,fERROR):
  #Variable COMPARA
  if (inspect()=='COMPARA' and fSI) or fOP_REL:
    if '[id]' in line:      
      pop()
      fOP_REL=True
      push('[op_rel]')
      return True
    elif inspect()=='[op_rel]' and ('<' in line or '>' in line) and fSI and fOP_REL:    
      fOP_REL=False
      pop()
      push('ELEM')      
    else:
      print('ERROR DE COMPILACION')
      fERROR=True
      break

def checkSENTstructure(line,fSI,fREP,fIMP,fLEE,fID,fPROG,fERROR):
  #Variable SENT 
  if inspect()=='SENT' or fID or fSI or fREP or fIMP or fLEE:
    if ('=' in line and inspect()=='=' and fID and fPROG) or fID and inspect()=='SENT' and not(fIMP):
      pop()      
      fID=False
    elif ('[id]' in line and inspect()=='SENT') and not(fIMP):
      fID=True
      pop()      
      push('ELEM')
      push('=')
      return True
    elif 'SI' in line or fSI and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line) and not('REPITE' in line):      
      #Colocamos la estructura del SI #Estructruta de SI ENTONCES SINO FINSI
      if 'SI' in line and fPROG and inspect()=='SENT':
        pop()
        fSI=True
        push('FINSI')
        push('SENTS')     #Metemos variable
        push('ENTONCES')
        push('COMPARA')   #Metemos variable
        return True
      if inspect()=='ENTONCES' and fSI and fPROG:
        if 'ENTONCES' in line:          
          pop()
          return True
        else:
          print('ERROR DE COMPILACION')
      if 'SINO' in line and fSI and fPROG:    
        push('SENTS')     #Metemos variable 
        return True
      if fSI and inspect()=='FINSI' and fPROG:
        if 'FINSI' in line:
          pop()
          checkNext(line)
          if not('FINSI' in stack):
            fSI=False
            return True
          else:
            return True
        else:
          print('ERROR DE COMPILACION')
    elif 'REPITE' in line or fREP and not(fIMP) and not('IMPRIME' in line) and not('LEE' in line): 
      #Colocamos la estructura del REPITE #Estructura de REPITE VECES FINREP
      if 'REPITE' in line and fPROG and inspect()=='SENT':
        pop()
        fREP=True
        push('FINREP')
        push('SENTS')     #Metemos variable
        push('VECES')  
        push('ELEM')      #Metemos variable
        return True 
      if inspect()=='VECES' and fREP and fPROG:
        if 'VECES' in line:          
          pop()
          return True
        else:
          print('ERROR DE COMPILACION')
      if inspect()=='FINREP' and fREP and fPROG:
        if 'FINREP' in line:
          pop()
          checkNext(line)
          if not('FINREP' in stack):
            fREP=False
            return True
          else:
            return True
        else:
          print('ERROR DE COMPILACION')
          break
    elif 'IMPRIME' in line or fIMP:
      #Colocamos la estructura del IMPRIME #Estructura de IMPRIME
      if 'IMPRIME' in line and fPROG and inspect()=='SENT':
        pop()
        fIMP=True
        push('IMPRIME')
        return True
      if inspect()=='IMPRIME' and fIMP:
        if '[text]' in line:
          fIMP=False
          pop()
          checkNext(line)
          return True
        elif '[id]' in line or '[val]' in line:
          pop()
          push('ELEM')    #Metemos variable 
          fIMP=False
          pop()
          checkNext(line)
        else:
          print('ERROR DE COMPILACION')
          fERROR=True
          break
    elif 'LEE' in line or fLEE: 
      #Colocamos la estructura del LEE #Estructura de LEE
      if 'LEE' in line and fPROG and inspect()=='SENT':        
        pop()   
        fLEE=True
        push('LEE')
        return True
      if inspect()=='LEE' and fLEE:
        if '[id]' in line:              
          pop()
          fLEE=False                 
          checkNext(line)
          return True
        else:
          print('ERROR DE COMPILACION')
          fERROR=True
          break
    else:
      print(line)
      print(inspect())
      print('ERROR DE COMPILACION')      
      break  
  else:
    print('ERROR DE COMPILACION')
    break  

def checkELEMstructure(line,fSI,fPROG,fID,fERROR,mainStack,cont):
  #Variable ELEM
  if inspect()=='ELEM':
    if '[val]' in line or '[id]' in line:
      pop()
      if not(fSI):
        checkNext(line)      
      next = cont
      if '[op_ar]' in mainStack[next] and fPROG:   
        fOP_AR=True
        return True
      else:
        fID=False
        return True
    else:
      print('ERROR DE COMPILACION')
      fERROR=True
      break

fPROG=False
fID=False
fSI=False
fREP=False
fIMP=False
fLEE=False
fERROR=False
fOP_AR=False
fOP_REL=False

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

  if checkPROGstructure(line,fPROG,fERROR):
    continue
  if checkSENTSstructure():
    continue
  if checkCOMPARAstructure(line,fOP_REL,fSI,fERROR):
    continue
  if checkOP_ARstructure(fPROG,fOP_AR,fREP):
    continue
  if checkELEMstructure(line,fSI,fPROG,fID,fERROR,mainStack,cont):
    continue
  if checkSENTstructure(line,fSI,fREP,fIMP,fLEE,fID,fPROG,fERROR): 
    continue

if isEmpty() and not(fERROR):
  print('COMPILACION EXITOSA')
else:
  print(stack)
  print('ERROR DE COMPILACION')
