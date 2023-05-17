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

def verificar_gramatica(entrada, gerador='<expressao>'):
    gramatica = {
        '<expressao>': [
            ('01', '<declaracao>'),
            ('03', '<declaracao>'),
            ('13', '<condicional>'),
            ('21', '<loop>'),
            ('19', '<imprimir>'),
            ('99', '<atribuicao>')
        ],
        '<declaracao>': [
            ('01', '<tipo> <variavel> 04'),
            ('03', '<tipo> <variavel> 04'),
        ],
        '<tipo>': [
            ('01', '01'),
            ('03', '03'),
        ],
        '<variavel>': [
            ('99', '99'),
        ],
        '<atribuicao>': [
            ('99', '<variavel> 05 <entrada>'),
        ],
        '<entrada>': [
            ('17', '<expressaoaritimetica> 04'),
            ('20', '20 <string> 20 04'),
            ('98', '<expressaoaritimetica> 04'),
            ('99', '<expressaoaritimetica> 04'),
        ],
        '<expressaoaritimeticalinha>': [
            ('04', 'vazio'),
            ('05', 'vazio'),
            ('06', '<somaousub> <expressaoaritimeticalinha>'),
            ('07', '<somaousub> <expressaoaritimeticalinha>'),
            ('10', 'vazio'),
            ('11', 'vazio'),
            ('12', 'vazio'),
            ('18', 'vazio'),
            ('24', 'vazio'),
            ('25', 'vazio'),
        ],
        '<expressaoaritimetica>': [
            ('17', '<termo> <expressaoaritimeticalinha>'),
            ('99', '<termo> <expressaoaritimeticalinha>'),
            ('98', '<termo> <expressaoaritimeticalinha>'),
        ],
        '<somaousub>': [
            ('06', '06 <termo>'),
            ('07', '07 <termo>'),
        ],
        '<termolinha>': [
            ('04', 'vazio'),
            ('05', 'vazio'),
            ('06', 'vazio'),
            ('07', 'vazio'),
            ('08', '<multoudiv> <termolinha>'),
            ('09', '<multoudiv> <termolinha>'),
            ('10', 'vazio'),
            ('11', 'vazio'),
            ('12', 'vazio'),
            ('18', 'vazio'),
            ('24', 'vazio'),
            ('25', 'vazio'),
        ],
        '<multoudiv>': [
            ('08', '08 <fator>'),
            ('09', '09 <fator>'),
        ],
        '<termo>': [
            ('17', '<fator> <termolinha>'),
            ('98', '<fator> <termolinha>'),
            ('99', '<fator> <termolinha>'),
        ],
        '<fator>': [
            ('17', '17 <expressaoaritimetica> 18'),
            ('98', '<valor>'),
            ('99', '<valor>'),
        ],
        '<condicional>': [
            ('13', '13 17 <comparacao> 18 27 <escopo> 28 <condicionalinverso>')
        ],
        '<condicionalinversoescopo>': [
            ('13', '<condicional>'),
            ('27', '27 <escopo> 28')
        ],
        '<condicionalinverso>': [
            ('15', '15 <condicionalinversoescopo>'),
            ('$', 'vazio')
        ],
        '<comparacao>': [
            ('12', '<expressaologica>'),
            ('17', '<expressaologica>'),
            ('98', '<expressaologica>'),
            ('99', '<expressaologica>')
        ],
        # '<sinalcomparacaoigual>': [
        #     ('05', '05'),
        #     ('17', 'vazio'),
        #     ('98', 'vazio'),
        #     ('99', 'vazio')
        # ],
        '<sinalcomparacao>': [
            ('05', '05 05'),
            ('10', '10 05'),
            ('11', '11 05'),
            ('12', '12 05')
        ],
        '<valor>': [
            ('98', '98'),
            ('99', '<variavel>'),
        ],
        '<expressaologicalinha>': [
            ('04', 'vazio'),
            ('18', 'vazio'),
            ('24', '<andouor> <expressaologicalinha>'),
            ('25', '<andouor> <expressaologicalinha>'),
        ],
        '<andouor>': [
            ('24', '24 24 <expressaologica>'),
            ('25', '25 25 <expressaologica>'),
        ],
        '<expressaologica>': [
            ('12', '12 <expressaologicalinha>'),
            ('17', '<comparador> <expressaologicalinha>'),
            ('98', '<comparador> <expressaologicalinha>'),
            ('99', '<comparador> <expressaologicalinha>'),
        ],
        '<comparador>': [
            ('17', '<expressaoaritimetica> <sinalcomparacao> <expressaoaritimetica>'),
            ('98', '<expressaoaritimetica> <sinalcomparacao> <expressaoaritimetica>'),
            ('99', '<expressaoaritimetica> <sinalcomparacao> <expressaoaritimetica>'),
        ],
        '<escopo>': [
            ('01', '<expressao> <escopo>'),
            ('03', '<expressao> <escopo>'),
            ('13', '<expressao> <escopo>'),
            ('19', '<expressao> <escopo>'),
            ('21', '<expressao> <escopo>'),
            ('28', 'vazio'),
            ('99', '<expressao> <escopo>')
        ],
        '<loop>': [
            ('21', '21 17 <variavel> 04 <comparacao> 04 <pulo> 18 27 <escopo> 28'),
        ],
        '<pulo>': [
            ('99', '<variavel> <sinal> 05 <valor>'),
        ],
        '<sinal>': [
            ('06', '06'),
            ('07', '07'),
            ('08', '08'),
            ('09', '09'),
        ],
        '<stringnum>': [
            ('20', '20 <string> 20 04'),
            ('98', '<valor> 04'),
            ('99', '<valor> 04'),
        ],
        '<imprimir>': [
            ('19', '19 <stringnum>')
        ],
        '<string>': [
            ('20', 'vazio'),
            ('97', '97 <string>'),
        ]
    }

    for producao in gramatica[gerador]:
        if producao[0] == entrada:
            return producao[1]
    return False
    

def analisador_sintatico(tokens):
    pilha = ['<expressao>']
    entrada = []
    for token in tokens:
        entrada.append(token[1])
        while len(entrada) > 0:
            print(f"-=-=-=-= VERIFICANDO A PALAVRA {token[0]} -=-=-=-=")
            print(pilha)
            print()
            
            if len(pilha) == 0:
                pilha = ['<expressao>']

            if pilha[0].isnumeric():
                saida = pilha.pop(0)
                if saida == entrada[0]:
                    entrada.pop()
                else:
                    print(f"ERRO DE SINTAXE!!! Recebeu: {saida}, Esperava: {entrada[0]}.")
                    return
            elif pilha[0] == 'vazio':
                pilha.pop(0)
            else:
                producao = verificar_gramatica(entrada[0], pilha[0])
                if producao:
                    print(f"Encontrei o gerador {pilha[0]} e produzi '{producao}'")
                    producao = producao.split()
                    saida = pilha.pop(0)
                    print('retirando da pilha: ', saida)

                    if saida != entrada[0]:
                        producao.reverse()
                        for item in producao:
                            print('inserindo na pilha: ', item)
                            pilha.insert(0, item)
                    else:
                        entrada.pop()
    print("Nenhum erro de sintaxe, parabens!! :D")


def analisador_lexico(texto):
    fluxo_codigo = []
    tabela_de_simbolos = []
    cont = 0
    aspas = 0
    for palavra in texto:
        if palavra in tipos:
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
                    elif palavra.isnumeric():
                        fluxo_codigo.append((palavra, '98'))
                    else:
                        print("> ERRO LÉXICO!! POR FAVOR VERIFIQUE A PALAVRA: " + palavra)
                        return

    print("> Gerando Documento de Fluxo de Tokens...")
    gerar_fluxo_lexico(fluxo_codigo)

    print("> Gerando Tabela de Simbolos...")
    gerar_tabela_de_simbolos(tabela_de_simbolos)

    return fluxo_codigo
