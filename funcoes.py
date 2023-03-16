from tipos import tipos
import re

def getAlgoritmo(nome_do_arquivo):
    with open(nome_do_arquivo, 'r', encoding='utf-8') as arq:
        texto = arq.read()
        #print(texto)
    return texto


def separador(palavra, caractere):
    index = encontrar_indices(palavra, caractere)
    cont = 0
    for i in index:
        palavra = palavra[:i+cont] + ' ' + palavra[i+cont] + ' ' +palavra[i+cont+1:]
        cont += 2
        
    return palavra

def encontrar_indices(palavra, caractere):
    indices = []
    for i in range(len(palavra)):
        if palavra[i] == caractere:
            indices.append(i)
    return indices


def separar_texto(lista):
    caracteres = [
                ';', '"', '(', ')', '.', '>',  '<',  '~', '=', '+', '-',
                '*', '/', '[', ']', '&',  '%',  '$', '@',  '!',  '?', ',', 
                ':', '{', '}'
                ]

    texto_separado = []
    for palavra in lista:
        nova_lista = []
        for c in caracteres:
            if c in palavra:
                palavra = separador(palavra, c)
        p = palavra.split()
        for item in p:
            texto_separado.append(item)

    return texto_separado

def get_simbolo(tabela_de_simbolos, simbolo):
    for s in tabela_de_simbolos:
        if s[0] == simbolo:
            return (s[0], s[1])
    return None

def gerar_fluxo_lexico(fluxo):
    arq = open("fluxo_lexico.txt", "w")

    for item in fluxo:
        arq.write(f"({item[0]},{item[1]})\n")
    
    arq.close()

def gerar_tabela_de_simbolos(tabela):
    arq = open("tabela_de_simbolos.csv", "w")

    arq.write("nome;chave\n")
    for item in tabela:
        arq.write(f"{item[0]};{item[1]}\n")
    
    arq.close()

def verificar_variavel(palavra):
    print(palavra)
    padrao_de_rotulo = r'^[A-Za-z_][A-Za-z]*[0-9]?$'
    if re.match(padrao_de_rotulo, palavra):
        return True
    else:
        return False

def analizador_lexico(texto):
    fluxo_codigo = []
    tabela_de_simbolos = []
    cont = 0
    aspas = 0
    for palavra in texto:
        if palavra in tipos and aspas == 0:
            if palavra == '"' and aspas == 0:
                aspas = 1
            elif palavra == '"' and aspas == 1:
                aspas = 0

            fluxo_codigo.append((palavra, tipos[palavra]))
        else:
            if aspas == 1:
                fluxo_codigo.append((palavra, '97'))
            else:
                simbolo = get_simbolo(tabela_de_simbolos, palavra)
                if simbolo:
                    fluxo_codigo.append((str(simbolo[1]), '99'))
                else:
                    if verificar_variavel(palavra):
                        tabela_de_simbolos.append((palavra, cont))
                        fluxo_codigo.append((cont, '99'))
                        cont += 1
                    elif palavra.isdigit():
                        fluxo_codigo.append((cont, '98'))
                    else:
                        print("> ERRO LÉXICO!! POR FAVOR VERIFIQUE A PALAVRA: " + palavra)
                        return

    print("> Gerando Documento de Fluxo Léxico...")
    gerar_fluxo_lexico(fluxo_codigo)

    print("> Gerando Tabela de Simbolos...")
    gerar_tabela_de_simbolos(tabela_de_simbolos)
