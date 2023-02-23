from copy import copy,deepcopy
tabla=[]
prvi ="Covek"
def zapocniIgru():
    print("Igra pocinje kada uneste dimenzije table")
    height=int(input("unesite visinu table: "))
    weidth=int(input("unesite sirinu table: "))
    for i in range(0,height):
        tmp=[]
        for j in range(0,weidth):
            tmp.append(" ")
        tabla.append(tmp)
    print(height,"x",weidth)
    stampanjeTable([height,weidth])
    return [height,weidth]  #dimenzije cemo da pamtimo kao tuple i prosledjujemo funkcijama kojima trebaju

def odigrajPotez(igrac,dimenzije):
    print("unesite koordinate poteza:")

    inpY=input("unesite kolonu: ")
    inpX=int(input("unesite vrstu: "))

    #trnasformacija u nase koordinate
    x=dimenzije[0]-inpX
    y=ord(inpY)-ord('A')

    if validanPotez(igrac,x,y,dimenzije):
        stampanjeTable(dimenzije)
        return True
    else:
        print("Nemoguc potez, pokusajte opet.")
        return False

    

def validanPotez(igrac,x,y,dimenzije):
    height=dimenzije[0]
    weidth=dimenzije[1]
    validan = False
    if(igrac=='X'):
        if(x>0 and x<height and y>=0 and y<weidth and tabla[x-1][y]==" " and tabla[x][y]==" "):
            tabla[x][y]=igrac
            tabla[x-1][y]=igrac
            validan = True
    else:
        if(x>=0 and x<height and y>=0 and y<weidth-1 and tabla[x][y]==' ' and tabla[x][y+1]==' '):
            tabla[x][y]=igrac
            tabla[x][y+1]=igrac
            validan = True
    return validan

def operatorPrelaza(igrac,dimenzije,trenutnoStanje):
    potencijalniPotezi=[]
    listaStanja=[]
    if igrac=='X':
        for i in range(1,dimenzije[0]):
            for j in range(0,dimenzije[1]):
                if trenutnoStanje[i-1][j]==" " and trenutnoStanje[i][j]==" ":
                    potencijalniPotezi.append([i,j])
                    stanje=deepcopy(trenutnoStanje)
                    stanje[i][j]='X'
                    stanje[i-1][j]='X'
                    listaStanja.append(stanje)
    else:
        for i in range(0,dimenzije[0]):
            for j in range(0,dimenzije[1]-1):
                if trenutnoStanje[i][j]==" " and trenutnoStanje[i][j+1]==" ":
                    potencijalniPotezi.append([i,j])
                    stanje=deepcopy(trenutnoStanje)
                    stanje[i][j]='O'
                    stanje[i][j+1]='O'
                    listaStanja.append(stanje)
    #funckija vraca sve potencijalne poteze koje sl igrac moze da odigra.
    #u obliku liste stanje i, pod komentarom, liste poteza

    return listaStanja
    #return potencijalniPotezi

def krajIgre(igrac,dimenzije):
    brPoteza = 0
    height = dimenzije[0]
    weidth = dimenzije[1]
    if igrac == 'X':
        for i in range(1,height):
            for j in range(0,weidth):
                if(tabla[i-1][j] == " " and tabla[i][j] == " "):
                    brPoteza+=1
    else:
        for i in range(0,height):
            for j in range(0,weidth-1):
                if(tabla[i][j] == " " and tabla[i][j+1] == " "):
                    brPoteza+=1

    return brPoteza

def stampanjeTable(dimenzije):
    redSlova="  "
    redJednako="  "
    for i in range(dimenzije[1]):
        redSlova+=chr(ord('A')+i)+" "
        redJednako+="= "

    print(redSlova)
    print(redJednako)

    #ovom petljom stampa se vrsta po vrsta table u zeljenom formatu 
    brVrste = dimenzije[0]
    for i in range(0,dimenzije[0]):
        redTabele=str(brVrste)+"ǁ"
        for j in range(0,dimenzije[1]):
            if(j!=dimenzije[1]-1):
                redTabele+=tabla[i][j]+"|"
            if(j==dimenzije[1]-1):
                redTabele+=tabla[i][j]+"ǁ"+str(brVrste)
        print(redTabele)
        brVrste-=1
        
    print(redJednako)
    print(redSlova)

def heuristika(comp,dimenzije,stanje):
    brPotezaX=0
    brPotezaO=0
    for i in range(1,dimenzije[0]):
        for j in range(0,dimenzije[1]):
            if(stanje[i-1][j] == " " and stanje[i][j] == " "):
                brPotezaX+=1
    for i in range(0,dimenzije[0]):
        for j in range(0,dimenzije[1]-1):
            if(stanje[i][j] == " " and stanje[i][j+1] == " "):
                brPotezaO+=1
    if comp=='X':
        return brPotezaX-brPotezaO
    if comp=='O':
        return brPotezaO-brPotezaX
    #mozda treba u zavisnosti od igraca, ali moze i bez

def minimax(comp,igrac,dimenzije,stanje, dubina,alfa=-30,beta=30):
    lista_poteza = operatorPrelaza(igrac, dimenzije, stanje)
    best_stanje=[]
    #min_max_stanje = max_stanje if moj_potez else min_stanje
    if dubina == 0 or lista_poteza is None or len(lista_poteza)==0:
        return(stanje, heuristika(comp,dimenzije,stanje))
    if igrac=='X':
        igrac='O'
    else: igrac='X'
    if(igrac!=comp):
        best=-1000
        for s in lista_poteza:
            val = minimax(comp,igrac,dimenzije,s,dubina-1,alfa,beta)
            if val[1]>best:
                best=val[1]
                best_stanje=deepcopy(s)
            alfa=max(alfa,best)
            if beta<=alfa:
                break
        return (best_stanje,best)
    else:
        best=1000
        for s in lista_poteza:
            val = minimax(comp,igrac,dimenzije,s,dubina-1,alfa,beta)
            if val[1]<best:
                best=val[1]
                best_stanje=deepcopy(s)
            beta=min(beta,best)
            if beta<=alfa:
                break
        return (best_stanje,best)
    
def igraPvP():
    igrac='X' #prvi igrac je X, ovo se lako menja, po potrebi
    dimenzije=zapocniIgru()
    while krajIgre(igrac,dimenzije):  #f-ja krajIgre vraca broj mogucih poteza, pa kada je 0 tada je kraj
        #print(heuristika(dimenzije,deepcopy(tabla)))
        if(odigrajPotez(igrac,dimenzije)==True):
            if(igrac == 'X'):
                igrac = 'O'
            else:
                igrac = 'X'
    print("Kraj igre, nema mesta za igraca: ",igrac)

def igraPvAI():
    global tabla
    igrac='X'
    inp=input("Unesite da li zelite da budete X ili O: ")
    if(inp=='X'): 
        player='X' 
        comp='O'
    if(inp=='O'): 
        player='O'
        comp='X'
    dimenzije=zapocniIgru()
    while krajIgre(igrac,dimenzije):  #f-ja krajIgre vraca broj mogucih poteza, pa kada je 0 tada je kraj
        if(igrac==player):
            if(odigrajPotez(igrac,dimenzije)==True):
                igrac=comp
        else:            
            #ovde ide minmax, u zavisnosti od toga sta je comp se menja heuristika, operator prelaza i vrv jos nesto
            #onda se tabla izmeni da bude novo stanje i onda..
            val=minimax(comp,igrac,dimenzije,deepcopy(tabla),3)
            #print(val[1])
            tabla=deepcopy(val[0])
            stampanjeTable(dimenzije)
            igrac=player
    print("Kraj igre, nema mesta za igraca: ",igrac)

def igra():
    inp=input("Upisite <PvP> za igru sa drugim igracem ili <PvAI> za igru protiv racunara: ")
    if(inp=="PvP"): 
        igraPvP()
    elif(inp=="PvAI"): 
        igraPvAI()
    else: 
        print("Doslo je do greske")

igra()
