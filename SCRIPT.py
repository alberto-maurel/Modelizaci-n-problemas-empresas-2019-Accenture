#--------------------------------------------
#-----------------Librerias------------------
#--------------------------------------------

import math
from collections import namedtuple
#from time import time #Para debuguear
import datetime

#--------------------------------------------
#-----------------Constantes-----------------
#--------------------------------------------

NOMBREARCHIVOENTRADA = 'TEST.txt'
NOMBREARCHIVOSALIDA = 'SCORE.txt'
NUMCASOS = 100        
 
SIGNOMULTIPLICACION = "*"
NOMBREEQUIPO = "NoTodoElMonteEsOregano"
CENTINELA = -15

OPSUMA = 0
OPREST = 1
OPMULT = 2
OPDIVI = 3

#--------------------------------------------
#------------Variables globales--------------
#--------------------------------------------
primos = [1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]


#--------------------------------------------
#-----------------Tipos----------------------
#--------------------------------------------

tDatos = namedtuple("tDatos", "numPasos num1 num2 operacion");
tCaso = namedtuple("tCaso", "idCaso target primo primosNec sol");

#--------------------------------------------
#---------------Operadores-------------------
#--------------------------------------------

def cmp1(caso):
    return int(caso.primo)
    
def cmp2(caso):
    return int(caso.idCaso)

#--------------------------------------------
#------------------Funciones-----------------
#--------------------------------------------
    
CENTINELA = -15
    
tDatos = namedtuple("tDatos", "numPasos num1 num2 operacion");

OPSUMA = 0
OPREST = 1
OPMULT = 2
OPDIVI = 3

#Para transformar cada numero con su operador asociado
def numToOperation(num):
    if num == OPSUMA:
        return "+"
    if num == OPREST:
        return "-"
    if num == OPMULT:
        return SIGNOMULTIPLICACION
    if num == OPDIVI:
        return "/"

def solucionPorNiveles(primoEvitar, maxNivel):
    global primos
    marcaje = dict()
    numsNivel = [set() for i in range(0, maxNivel + 1)]
    
    #Rellenamos los numeros de nivel 1
    for pr in primos:
        if pr != primoEvitar:
            datosIni = tDatos(1, pr, CENTINELA, OPSUMA)
            marcaje[pr] = datosIni
            (numsNivel[1]).add(pr)
           
    #Rellenamos los numeros hasta maxNivel
    nivelActual = 2
    while nivelActual <= maxNivel:        
        for i in range (1,math.floor((nivelActual + 2)/2)):
            nivel1 = i
            nivel2 = nivelActual - i
            
            for num1 in numsNivel[nivel1]:
                for num2 in numsNivel[nivel2]:
                    
                    #Probamos a sumar
                    nuevoNum = num1 + num2
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, num1, num2, OPSUMA)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum)
                    
                    #Probamos a restar
                    nuevoNum = max(num1, num2) - min(num1, num2)
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, max(num1, num2), min(num1, num2), OPREST)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum)
                    
                    #Probamos a multiplicar
                    nuevoNum = num1 * num2
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, num1, num2, OPMULT)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum) 
        
        nivelActual = nivelActual + 1
        
    clavesMarcaje = sorted(marcaje.keys())
    
    #Devolvemos tanto los datos de todos los niveles como las claves 
    #ordenadas (numeros que hemos podido conseguir)
    return (clavesMarcaje, marcaje)

#Idéntica a la función anterior pero devuelve un conjunto con SOLO los numeros en maxNivel
def numerosEnUnNivel(primoEvitar, maxNivel):
    global primos
    marcaje = dict()
    numsNivel = [set() for i in range(0, maxNivel + 1)]
    
    for pr in primos:
        if pr != primoEvitar:
            datosIni = tDatos(1, pr, CENTINELA, OPSUMA)
            marcaje[pr] = datosIni
            (numsNivel[1]).add(pr)
            
    nivelActual = 2
    while nivelActual <= maxNivel:        
        for i in range (1,math.floor((nivelActual + 2)/2)):
            nivel1 = i
            nivel2 = nivelActual - i
            
            for num1 in numsNivel[nivel1]:
                for num2 in numsNivel[nivel2]:
                    
                    #Probamos a sumar
                    nuevoNum = num1 + num2
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, num1, num2, OPSUMA)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum)
                    
                    #Probamos a restar
                    nuevoNum = max(num1, num2) - min(num1, num2)
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, max(num1, num2), min(num1, num2), OPREST)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum)
                    
                    #Probamos a multiplicar
                    nuevoNum = num1 * num2
                    if nuevoNum not in marcaje:
                        nuevoDatos = tDatos(nivelActual, num1, num2, OPMULT)
                        marcaje[nuevoNum] = nuevoDatos
                        numsNivel[nivelActual].add(nuevoNum)
           
        
        nivelActual = nivelActual + 1

    return numsNivel[maxNivel]

#Función que recompone la solucion optima de los elementos en marcaje
def recomponerSol(nAct, marcaje):
    datosAux = marcaje[int(nAct)]
    
    if datosAux.num2 == CENTINELA:
        return str(datosAux.num1)
    else:
        s1 = "(" + recomponerSol(datosAux.num1, marcaje)
        s2 = recomponerSol(datosAux.num2, marcaje) + ")"
        solucion = s1 + numToOperation(datosAux.operacion) + s2
        return solucion
    
#Busqueda binaria de buscado en v, en el intervalo [ini, fin]
#Si el elemento está devuelve el índice y si no donde deberia ir
def busBin(ini, fin, buscado, v):
    if ini > fin:
        return ini
    elif ini == fin:
        if buscado < v[ini]:
            return ini
        else: 
            return ini + 1
    else:
        mitad = int((ini + fin - 1)/2)
        if(v[mitad] == buscado):
            return mitad
        elif v[mitad] < buscado:
            return busBin(mitad + 1, fin, buscado, v)
        else:
            return busBin(ini, mitad -1, buscado, v)

#Dados un n1 y n2 en nuestra solucion canonica resuelve el caso   
def resolverCasoGreedy(target, n1, n2, marcaje, mSolAct):
    mSol = 100
    solucion = ""
    
    resto = abs(target - n1 * n2)
    
    if resto == 0:
        mSol = marcaje[n1].numPasos + marcaje[n2].numPasos
        if mSolAct > mSol:
            solucion = "(" + recomponerSol(n1, marcaje) + ")" + SIGNOMULTIPLICACION + "(" + recomponerSol(n2, marcaje) + ")"
    else:
        if resto in marcaje:
            if n1 == 1:
                mSol = marcaje[resto].numPasos + marcaje[n2].numPasos
                if mSolAct > mSol:
                    if (n2 + resto) == target:
                        solucion = "(" + recomponerSol(n2, marcaje) + ")+(" + recomponerSol(resto, marcaje) + ")"
                    else:
                        solucion = "(" + recomponerSol(n2, marcaje) + ")-(" + recomponerSol(resto, marcaje) + ")"
            else:
                mSol = marcaje[n1].numPasos + marcaje[n2].numPasos + marcaje[resto].numPasos
                if mSolAct > mSol:
                    if (n1 * n2) > target:
                        solucion = "(" + recomponerSol(n1, marcaje) + ")" + SIGNOMULTIPLICACION + "(" + recomponerSol(n2, marcaje) + ")-(" + recomponerSol(resto, marcaje) + ")"
                    else:
                        solucion = "(" + recomponerSol(n1, marcaje) + ")" + SIGNOMULTIPLICACION + "(" + recomponerSol(n2, marcaje) + ")+(" + recomponerSol(resto, marcaje) + ")"
            
    return (mSol, solucion)
        
    
#Funcion que obtiene la solucion canonica de nuestro caso
def greedy(target, marcaje, primoAEvitar, clavesMarcaje):
    #Si tenemos precalculada la solucion optima la devolvemos
    if target in marcaje:
        return (marcaje[target].numPasos, recomponerSol(target, marcaje))
    
    mSol = 100
    sMSol = ""
    n1 = 1
    raiz = int(math.sqrt(target)) + 5
    
    while n1 <= raiz:
        if n1 in marcaje:
            #Hacemos una búsqueda binaria para encontrar el n2
            n2 = math.floor(target/n1)
            
            indice = busBin(0, len(clavesMarcaje) - 1, n2 ,clavesMarcaje)
            indiceAux = indice
            
            #Probamos con los restos de nivel 1 y 2
            if(indice >= 0 and indice <= len(clavesMarcaje) - 1):
                resto = abs(target - n1 * clavesMarcaje[indice])
                while resto < 8000:
                    (auxSol, auxSSol) = resolverCasoGreedy(target, n1, clavesMarcaje[indice], marcaje, mSol)
                    if auxSol < mSol:
                            mSol = auxSol
                            sMSol = auxSSol
                    if indice < len(clavesMarcaje):
                        indice = indice + 1
                    else:
                        break
                    resto = abs(target - n1 * clavesMarcaje[indice])
                    
                indice = indiceAux
                while resto < 8000:
                    (auxSol, auxSSol) = resolverCasoGreedy(target, n1, clavesMarcaje[indice], marcaje, mSol)
                    if auxSol < mSol:
                            mSol = auxSol
                            sMSol = auxSSol
                    if indice > 0:
                        indice = indice - 1
                    else:
                        break
                    resto = abs(target - n1 * clavesMarcaje[indice])
            
            indice = indiceAux
            #Probamos con los restos mas cercanos a los numeros obtenidos
            #No es parte de la solucion canonica pero en ocasiones mejora los resultados
            if(indice >= 0 and indice <= len(clavesMarcaje) - 1):
                (auxSol, auxSSol) = resolverCasoGreedy(target, n1, clavesMarcaje[indice], marcaje, mSol)
                if auxSol < mSol:
                        mSol = auxSol
                        sMSol = auxSSol
               
            if(indice > 0 and indice <= len(clavesMarcaje) - 1):
                (auxSol, auxSSol) = resolverCasoGreedy(target, n1, clavesMarcaje[indice - 1], marcaje, mSol)
                if auxSol < mSol:
                        mSol = auxSol
                        sMSol = auxSSol
                    
            if(indice >= 0 and indice < len(clavesMarcaje) - 1):
                (auxSol, auxSSol) = resolverCasoGreedy(target, n1, clavesMarcaje[indice + 1], marcaje, mSol)
                if auxSol < mSol:
                        mSol = auxSol
                        sMSol = auxSSol
            
        n1 = n1 + 1
        
    return(mSol, sMSol)

#Funcion que cubre los casos de nivel 6 que no estan cubiertos por la solucion canonica
#Es decir, optimiza el nivel 7 para tratar de bajar las soluciones a nivel 6
#target - Numero objetivo
#primoAEvitar - Primo excluido
#marcaje - diccionario con toda la informacion hasta el nivel 4
#clavesMarcaje2 - lista con las claves ordenadas de nivel 1 y 2
#setNivel3 - conjunto con solo los numeros de nivel 3
def opt7(target, primoAEvitar, marcaje, clavesMarcaje2, setNivel3):
    #Buscamos si hay soluciones con la estructura de los casos A y B
    for a in primos:
        if a != int(primoAEvitar) and int(target) % a == 0:
            for b in clavesMarcaje2:
                
                #target = a x (c + b)
                #target = n1 x (n4 + n1) caso A
                #target = n1 x (n3 + n2) caso B
                c = (int(target) / a) - b
                if c > 0 and c in marcaje:
                    nPasos = 1 + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 7:
                        solucion = "("+str(a)+SIGNOMULTIPLICACION+"("+recomponerSol(c, marcaje)+"+"+recomponerSol(b, marcaje)+"))"
                        return (nPasos,solucion)
                    
                #target = a x (c - b)
                #target = n1 x (n4 - n1) caso A
                #target = n1 x (n3 - n2) caso B
                c = (int(target) / a) + b
                if c > 0 and c in marcaje:
                    nPasos = 1 + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 7:
                        solucion = "("+str(a)+SIGNOMULTIPLICACION+"("+recomponerSol(c, marcaje)+"-"+recomponerSol(b, marcaje)+"))"
                        return (nPasos,solucion)
                    
                #target = a x (b - c)
                #target = n1 x (n1 - n4) caso A
                #target = n1 x (n2 - n3) caso B
                c = b - (int(target) / a) 
                if c > 0 and c in marcaje:
                    nPasos = 1 + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 7:
                        solucion = "("+str(a)+SIGNOMULTIPLICACION+"("+recomponerSol(b, marcaje)+"-"+recomponerSol(c, marcaje)+"))"
                        return (nPasos,solucion)  
       
    #Buscamos si hay soluciones con la estructura del caso C             
    for a in setNivel3:
        num = target - a
        if num > 0 and num in marcaje:
            nPasos = marcaje[a].numPasos + marcaje[num].numPasos
            if(nPasos < 7):
                solucion = "("+recomponerSol(a,marcaje)+"+"+recomponerSol(num,marcaje)+")"
                return (nPasos, solucion)
        
        num = target + a
        if num > 0 and num in marcaje:
            nPasos = marcaje[a].numPasos + marcaje[num].numPasos
            if(nPasos < 7):
                solucion = "("+recomponerSol(num,marcaje)+"-"+recomponerSol(a,marcaje)+")"
                return (nPasos, solucion)
            
    #Si no hemos encontrado una solucion devolvemos un caso arbitrariamente grande.
    return (100,"")

#Funcion que cubre los casos de nivel 7 que no estan cubiertos por la solucion canonica
#Es decir, optimiza el nivel 8 para tratar de bajar las soluciones a nivel 7
#target - Numero objetivo
#primoAEvitar - Primo excluido
#marcaje - diccionario con toda la informacion hasta el nivel 4
#clavesMarcaje2 - lista con las claves ordenadas de nivel 1 y 2
#setNivel3 - conjunto con solo los numeros de nivel 3
def opt8(target, primoAEvitar, marcaje, clavesMarcaje2, setNivel3):
    #Buscamos si hay soluciones con la estructura de los casos A y B
    for a in clavesMarcaje2:
        if a != 0 and target % a == 0:
            for b in clavesMarcaje2:
                #target = a x (c + b)
                #target = n2 x (n4 + n1) caso A
                #target = n2 x (n3 + n2) caso B
                c = (target / a) - b
                if c > 0 and c in marcaje:
                    nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 8:
                        solucion = "("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+recomponerSol(b, marcaje)+"+"+recomponerSol(c, marcaje)+"))"
                        return (nPasos, solucion)
                    
                #target = a x (c - b)
                #target = n2 x (n4 - n1) caso A
                #target = n2 x (n3 - n2) caso B    
                c = (target / a) + b
                if c > 0 and c in marcaje:
                    nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 8:
                        solucion = "("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+recomponerSol(c, marcaje)+"-"+recomponerSol(b, marcaje)+"))"
                        return (nPasos, solucion)
                
                #target = a x (b - c)
                #target = n2 x (n1 - n4) caso A
                #target = n2 x (n2 - n3) caso B
                c = b - (target / a)
                if c > 0 and c in marcaje:
                    nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                    if nPasos < 8:
                        solucion = "("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+recomponerSol(b, marcaje)+"-"+recomponerSol(c, marcaje)+"))"
                        return (nPasos, solucion)
                    
    #Buscamos si hay soluciones con la estructura de los casos C y D
    for a in primos:
        if a != primoAEvitar:
            
            num = target - a
            if num >= 0:
                for b in primos:
                    if b != primoAEvitar and num % b == 0:
                        num2 = num / b
                        for c in clavesMarcaje2:
                            
                            d = num2 - c
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(c,marcaje)+"+"+recomponerSol(d,marcaje)+"))"+"+"+str(a)+")"
                                    return (nPasos, solucion)
                                
                            d = c - num2
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(c,marcaje)+"-"+recomponerSol(d,marcaje)+"))"+"+"+str(a)+")"
                                    return (nPasos, solucion)
                                
                            d = c + num2
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(d,marcaje)+"-"+recomponerSol(c,marcaje)+"))"+"+"+str(a)+")"
                                    return (nPasos, solucion)
                            
            num = target + a
            if num >= 0:
                for b in primos:
                    if b != primoAEvitar and num % b == 0:
                        num2 = num / b
                        for c in clavesMarcaje2:
                            
                            d = num2 - c
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(c,marcaje)+"+"+recomponerSol(d,marcaje)+"))"+"-"+str(a)+")"
                                    return (nPasos, solucion)
                                
                            d = c - num2
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(c,marcaje)+"-"+recomponerSol(d,marcaje)+"))"+"-"+str(a)+")"
                                    return (nPasos, solucion)
                                
                            d = c + num2
                            if d > 0 and d in marcaje:
                                nPasos = 2 + marcaje[c].numPasos + marcaje[d].numPasos
                                if nPasos < 8:
                                    solucion = "(("+str(b)+SIGNOMULTIPLICACION+"("+recomponerSol(d,marcaje)+"-"+recomponerSol(c,marcaje)+"))"+"-"+str(a)+")"
                                    return (nPasos, solucion)
                    
    #Buscamos si hay soluciones con la estructura del caso E      
    for a in setNivel3:
        num = target - a
        if num > 0 and num in marcaje:
            nPasos = marcaje[a].numPasos + marcaje[num].numPasos
            if(nPasos < 8):
                solucion = "("+recomponerSol(a,marcaje)+"+"+recomponerSol(num,marcaje)+")"
                
        num = target + a
        if num > 0 and num in marcaje:
            nPasos = marcaje[a].numPasos + marcaje[num].numPasos
            if(nPasos < 8):
                solucion = "("+recomponerSol(num,marcaje)+"-"+recomponerSol(a,marcaje)+")"
                return (nPasos, solucion)
                
                
            
    return (100,"")

#Funcion que cubre los casos de nivel 8 que no estan cubiertos por la solucion canonica
#Es decir, optimiza el nivel 9 para tratar de bajar las soluciones a nivel 8
#target - Numero objetivo
#primoAEvitar - Primo excluido
#marcaje - diccionario con toda la informacion hasta el nivel 4
#clavesMarcaje2 - lista con las claves ordenadas de nivel 1 y 2
#setNivel3 - conjunto con solo los numeros de nivel 3
def opt9(target, primoAEvitar, marcaje, clavesMarcaje2, setNivel3):
    #Buscamos si hay solucines con la estructura del caso A
    for a in clavesMarcaje2:
        if a != 0 and target % a == 0:
            
            num = target / a
            for b in setNivel3:
                if b != 0 and num % b == 0:
    
                    num2 = num / b
                    if num2 in marcaje:
                        nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[num2].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+recomponerSol(b,marcaje)+
                                          SIGNOMULTIPLICACION+recomponerSol(num2, marcaje)+")")
                            return (nPasos, solucion)
                        
    #Buscamos si hay solucines con la estructura del caso B
    for a in clavesMarcaje2:
        if a != 0 and target % a == 0:
            num = target / a
            
            for b in clavesMarcaje2:
                num2 = num - b
                
                if num2 > 0:
                    c = num - b
                    if c in marcaje:
                        nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(b,marcaje)+"+"+recomponerSol(c,marcaje)+"))")
                            return (nPasos, solucion)
                    
                    c = b - num
                    if c in marcaje:
                        nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(b,marcaje)+"-"+recomponerSol(c,marcaje)+"))")
                            return (nPasos, solucion)
                        
                    c = b + num
                    if c in marcaje:
                        nPasos = marcaje[a].numPasos + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(c,marcaje)+"-"+recomponerSol(b,marcaje)+"))")
                            return (nPasos, solucion)
                        
    #Buscamos las soluciones con estructuras C o D
    for a in setNivel3:
        if a != 0 and target % a == 0:
            num = target / a
            
            for b in clavesMarcaje2:
                num2 = num - b
                
                if num2 > 0:
                    c = num - b
                    if c in marcaje:
                        nPasos = 3 + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(b,marcaje)+"+"+recomponerSol(c,marcaje)+"))")
                            return (nPasos, solucion)
                    
                    c = b - num
                    if c in marcaje:
                        nPasos = 3 + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(b,marcaje)+"-"+recomponerSol(c,marcaje)+"))")
                            return (nPasos, solucion)
                        
                    c = b + num
                    if c in marcaje:
                        nPasos = 3 + marcaje[b].numPasos + marcaje[c].numPasos
                        if(nPasos < 9):
                            solucion = ("("+recomponerSol(a,marcaje)+SIGNOMULTIPLICACION+"("+
                                          recomponerSol(c,marcaje)+"-"+recomponerSol(b,marcaje)+"))")
                            return (nPasos, solucion)
    
    return (100,"")            

def main():
    #Leemos y escribimos el tiempo
    now = datetime.datetime.now()
    #tiempo_inicial = time() #Para debuguear
    
    archSalida = open(NOMBREARCHIVOSALIDA,'w')
    archSalida.write(now.strftime("%Y-%m-%d-%H:%M:%S.") + str(math.floor(now.microsecond/100)).zfill(4) + "\n")
   
    #En primer lugar leemos el archivo 
    casos = [];
    with open(NOMBREARCHIVOENTRADA, 'r') as f:
        for linea in f:
            lineaTrim = linea.split('|')
            if lineaTrim[0] == "ID":
                continue
            m = tCaso(lineaTrim[0], lineaTrim[1], lineaTrim[2], -1, "")
            casos.append(m)
            
    #Ordenamos los casos, para resolver todos los que tengan el mismo primo excluido juntos
    casos.sort(key = cmp1)
           
    contCasoAct = 0
    #Para cada caso calculamos la solución
    while contCasoAct < NUMCASOS:
        #print('Primo: ' + str(casos[contCasoAct].primo)); #Para debuguear
        
        #Hacemos los precálculos necesarios
        (clavesMarcaje2, marcaje2) = solucionPorNiveles(int(casos[contCasoAct].primo), 2)
        setNivel3 = numerosEnUnNivel(int(casos[contCasoAct].primo), 3);
        (clavesMarcaje, marcaje) = solucionPorNiveles(int(casos[contCasoAct].primo), 4)
        contCasoAux = contCasoAct
        
        #Resolvemos juntos todos los casos para un mismo primo excluido
        while (contCasoAux < NUMCASOS and casos[contCasoAct].primo == casos[contCasoAux].primo):
            #print("Caso: " + str(contCasoAux) + " iniciado") #Para debuguear
            
            #Sacamos la solución canonica de nuestro caso (mas informacion en la documentacion)
            (msol, solucion) = greedy(int(casos[contCasoAux].target), marcaje, int(casos[contCasoAux].primo), clavesMarcaje)
            
            #Realizamos las optimizaciones en los casos pertinentes
            if msol >= 7:
                (msol7, solucion7) = opt7(int(casos[contCasoAux].target), int(casos[contCasoAux].primo), marcaje, clavesMarcaje2, setNivel3)
                if msol7 < msol:
                    msol = msol7
                    solucion = solucion7
            
            if msol >= 8:
                (msol8, solucion8) = opt8(int(casos[contCasoAux].target), int(casos[contCasoAux].primo), marcaje, clavesMarcaje2, setNivel3)
                if msol8 < msol:
                    msol = msol8
                    solucion = solucion8
                   
            if msol >= 9:
                (msol9, solucion9) = opt9(int(casos[contCasoAux].target), int(casos[contCasoAux].primo), marcaje, clavesMarcaje2, setNivel3)
                if msol9 < msol:
                    msol = msol9
                    solucion = solucion9
                 
            #Guardamos la informacion de los casos
            casos[contCasoAux] = casos[contCasoAux]._replace(primosNec=msol)
            casos[contCasoAux] = casos[contCasoAux]._replace(sol=solucion)
            
            #tiempo_final = time()                 #Para debuguear
            #print(tiempo_final - tiempo_inicial)  #Para debuguear
            
            #Escribimos en la salida en cuanto podemos para no perder casos por escribirlos todos al final
            archSalida.write(NOMBREEQUIPO + "|" + str(casos[contCasoAux].idCaso) + "|" + 
                             str(casos[contCasoAux].primosNec) + "|" + casos[contCasoAux].sol + '\n')
            
            contCasoAux = contCasoAux + 1
            
        #Hemos acabado con todos los casos que tienen el mismo numero primo    
        contCasoAct = contCasoAux
        
    #Escribimos al terminar el tiempo que hemos tardado
    now = datetime.datetime.now()
    archSalida.write(now.strftime("%Y-%m-%d-%H:%M:%S.") + str(math.floor(now.microsecond/100)).zfill(4) + "\n")
    archSalida.close()

if __name__== "__main__":   
    main()
            
            