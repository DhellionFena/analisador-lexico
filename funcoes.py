from tipos import tipos

def getAlgoritmo(nome_do_arquivo):
    with open(nome_do_arquivo, 'r', encoding='utf-8') as arq:
        texto = arq.read()
        #print(texto)
    return texto


def separador(palavra, caractere):
    i = palavra.find(caractere)
    palavra_nova = palavra[:i] + ' ' + palavra[i] + ' ' +palavra[i+1:]
    return palavra_nova


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

def analizador_lexico(texto):
    fluxo_codigo = []
    tabela_de_simbolos = []
    cont = 0
    for palavra in texto:
        if palavra in tipos:
            fluxo_codigo.append((palavra, tipos[palavra]))
        else:
            simbolo = get_simbolo(tabela_de_simbolos, palavra)
            if simbolo:
                fluxo_codigo.append((str(simbolo[1]), '99'))
            else:
                #TODO VERIFICAR SE A VARIAVEL PODE SER UMA VARIAVEL E SE NAO INFORMAR UM ERRO!!!!
                tabela_de_simbolos.append((palavra, cont))
                fluxo_codigo.append(cont, '99')
                cont += 1

    print("Fluxo de codigo:")
    print(fluxo_codigo)

    print("Tabela de Simbolos:")
    print(tabela_de_simbolos)

    #TODO Exportar esses prints como documentos de texto.