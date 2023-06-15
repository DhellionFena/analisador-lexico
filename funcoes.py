from tipos import tipos
import re
import os

# Função para ler o .txt
def getAlgoritmo(nome_do_arquivo):
    with open(nome_do_arquivo, 'r', encoding='utf-8') as arq:
        texto = arq.read()
        #print(texto)
    return texto


# Função que pertence ao separador de texto e separa as palavras dos caracteres especiais com espaços
def separador(palavra, caractere):
    index = encontrar_indices(palavra, caractere)
    cont = 0
    for i in index:
        palavra = palavra[:i+cont] + ' ' + palavra[i+cont] + ' ' +palavra[i+cont+1:]
        cont += 2
        
    return palavra

# Função para encontrar o indice dos caracteres especiais
def encontrar_indices(palavra, caractere):
    indices = []
    for i in range(len(palavra)):
        if palavra[i] == caractere:
            indices.append(i)
    return indices


# Função que separa as palavras dos caracteres especiais
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

# Função que realiza uma busca na tabela de símbolos a partir do nome
def get_simbolo(tabela_de_simbolos, simbolo):
    for s in tabela_de_simbolos:
        if s['nome'] == simbolo:
            return (s)
    return None

# Função que realiza uma busca na tabela de símbolos a partir da chave/ID
def get_simbolo_chave(tabela_de_simbolos, chave):
    for s in tabela_de_simbolos:
        if s['chave'] == chave:
            return (s)
    return None

# Função que cria um txt do fluxo de tokens do analizador léxico
def gerar_fluxo_lexico(fluxo):
    arq = open("fluxo_lexico.txt", "w")

    for item in fluxo:
        arq.write(f"({item[0]},{item[1]})\n")
    
    arq.close()

# Função que cria um csv da tabela de simbolos
def gerar_tabela_de_simbolos(tabela):
    arq = open("tabela_de_simbolos.csv", "w")

    arq.write("nome;chave;tipo\n")
    for item in tabela:
        arq.write(f"{item['nome']};{item['chave']};{item['tipo']}\n")
    
    arq.close()

# Função que verifica se a palavra/rótulo pertence a linguagem.
def verificar_variavel(palavra):
    print(palavra)
    padrao_de_rotulo = r'^[A-Za-z_][A-Za-z]*[0-9]?$'
    if re.match(padrao_de_rotulo, palavra):
        return True
    else:
        return False

# Função que guarda a Árvore Sintática e realiza a produção do respectivo gerador
def verificar_gramatica(entrada, gerador='<expressao>'):
    gramatica = {
        '<expressao>': [
            ('30', '<declarar>'),
            ('13', '<condicional>'),
            ('21', '<loop>'),
            ('19', '<imprimir>'),
            ('29', '<break>'),
            ('99', '<atribuicao>')
        ],
        '<declaracao>': [
            ('01', '<tipo> <variavel> 04'),
            ('03', '<tipo> <variavel> 04'),
        ],
        '<declaracaolinha>': [
            ('01', '<declaracao> <declaracaolinha>'),
            ('03', '<declaracao> <declaracaolinha>'),
            ('28', 'vazio'),
            ('10', 'vazio'),
            ('11', 'vazio'),
            ('12', 'vazio'),
            ('18', 'vazio'),
            ('24', 'vazio'),
            ('25', 'vazio'),
            ('99', 'vazio'),
            ('04', 'vazio'),
            ('05', 'vazio'),
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
            ('99', 'vazio'),
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
            ('99', 'vazio'),
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
            ('13', '13 17 <comparacao> 18 27 <escopo> <condicionallinha>'),
            # ('13', '13 17 <comparacao> 18 27 <escopo> 28 <condicionalinverso>'),
        ],
        '<condicionallinha>': [
            ('28', '28 <condicionalinverso>'),
        ],
        '<condicionalinversoescopo>': [
            ('13', '<condicional>'),
            ('27', '27 <escopo> 28')
        ],
        '<condicionalinverso>': [
            ('15', '15 <condicionalinversoescopo>'),
            ('$', 'vazio'),
        ],
        '<comparacao>': [
            ('12', '<expressaologica>'),
            ('17', '<expressaologica>'),
            ('98', '<expressaologica>'),
            ('99', '<expressaologica>')
        ],
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
            ('15', 'vazio'),
            ('19', '<expressao> <escopo>'),
            ('21', '<expressao> <escopo>'),
            ('28', 'vazio'),
            ('29', '<expressao> <escopo>'),
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
        '<break>': [
            ('29', '29 04')
        ],
        '<declarar>': [
            ('30', '30 27 <declaracaolinha> 28')
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
    
# Função que compara os tipos de atribuição e retorna a compatibilidade
def match_tipo(simbolo_tipo, atribuicao):
    if simbolo_tipo == atribuicao:
        return True
    return False

# Função que retorna o tipo do token solicitado
def get_tipo(token, tabela_de_simbolos):
    if token[1] == '97':
        return '03'
    if token[1] == '98':
        return '01'
    if token[1] == '99':
        tipo = get_simbolo_chave(tabela_de_simbolos, token[0])
        return tipo['tipo']

# Função principal que coordena as análises sintáticas do compilador
def analisador_sintatico(tokens, tabela_de_simbolos):
    # Pilha de geradores e de produção.
    pilha = ['<expressao>']

    # Pilha de entrada dos tokens para serem analisados
    entrada = []                

    # (SEMÂNTICO) tipo do rótulo para realizar análise de atribuição
    tipo_simbolo = ''     

    # (SEMÂNTICO) registra se está dentro de um Loop   
    isPara = False

    # (SEMÂNTICO) Estado de alerta para comparação semantica de tipos
    esperar_proximo = False

    # Lógica de análise sintática
    for token in tokens:
        entrada.append(token)
        while len(entrada) > 0:
            
            if len(pilha) == 0:
                pilha = ['<expressao>']

            if pilha[0].isnumeric():
                # Retirando da pilha o terminal gerado pela produção
                saida = pilha.pop(0)

                if saida == entrada[0][1]:

                    # (SEMÂNTICO) Registra se está dentro de um LOOP
                    if saida == '21':
                        isPara = True

                    # (SEMÂNTICO) Analisa se BREAK; está dentro do escopo do LOOP
                    if saida == '29':
                        if not isPara:
                            print("ERRO SEMANTICO!! Função break pode estar apenas em loops.")
                            return
                
                    # (SEMÂNTICO) Reseta o registro após sair de escopo.
                    if saida == '28':
                        isPara = False

                    # (SEMÂNTICO) Comparador de TIPOS
                    if saida == '99':
                            simb = get_simbolo_chave(tabela_de_simbolos, entrada[0][0])
                            tipo_simbolo = simb['tipo']

                    if saida == '05':
                        # (SEMÂNTICO) Ativa o estado de alerta para comparar o TIPO
                        esperar_proximo = True
                    elif saida == '20':
                        #(SEMÂNTICO) Ignora as aspas
                        pass
                    elif esperar_proximo:
                        # (SEMÂNTICO) Realiza a comparação de tipos.
                        esperar_proximo = False
                        valor = get_tipo(entrada[0], tabela_de_simbolos)
                        if not match_tipo(tipo_simbolo, valor):
                            print("ERRO SEMANTICO!! Tipos não compatíveis.")
                            return

                    if saida == '04':
                        # (SEMÂNTICO) Reseta o registro após fim de linha.
                        tipo_simbolo = None
                    entrada.pop()

                else:
                    print(f"ERRO DE SINTAXE!!! Recebeu: {entrada[0]}, Esperava: {saida}.")
                    return

            elif pilha[0] == 'vazio':
                pilha.pop(0)
            else:
                producao = verificar_gramatica(entrada[0][1], pilha[0])
                if producao:
                    producao = producao.split()
                    saida = pilha.pop(0)
                    if saida != entrada[0][1]:
                        producao.reverse()
                        for item in producao:
                            pilha.insert(0, item)
                    else:
                        entrada.pop()
    print("Nenhum erro de sintaxe, parabens!! :D")


# Função principal que coordena as análises léxicas do compilador
def analisador_lexico(texto):
    fluxo_codigo = []
    tabela_de_simbolos = []

    # ID / chave dos simbolos
    cont = 0

    aspas = 0

    # (SEMÂNTICO) Avisa o tipo do rótulo para ser guardado na tabela de simbolos.
    eh_numerico = False
    eh_string = False

    # (SEMÂNTICO) Analisa se entrou no campo de declaração de variáveis
    declaracao = False

    for palavra in texto:
        if palavra in tipos:
            if palavra == '"' and aspas == 0:
                aspas = 1
            elif palavra == '"' and aspas == 1:
                aspas = 0

            # (SEMÂNTICO) Verifica se é string ou número
            if palavra == "numerico":
                eh_numerico = True
            elif palavra == "string":
                eh_string = True

            # (SEMÂNTICO) Entrou no campo de declaração de variáveis
            if palavra == "declarar":
                declaracao = True
            
            # (SEMÂNTICO) Reseta o registro após sair de escopo
            if palavra == "}":
                declaracao = False

            fluxo_codigo.append((palavra, tipos[palavra]))
        else:
            if aspas == 1:
                fluxo_codigo.append((palavra, '97'))
            else:
                simbolo = get_simbolo(tabela_de_simbolos, palavra)
                if simbolo:
                    fluxo_codigo.append((str(simbolo['chave']), '99'))
                else:
                        if verificar_variavel(palavra):
                            # (SEMÂNTICO) Verifica se está no campo de declaração de variáveis
                            if declaracao:
                                # (SEMÂNTICO) Criação de simbolo com base no nome do rotulo, ID e TIPO
                                simb = {
                                    'nome': palavra,
                                    'chave': str(cont),
                                    'tipo': "01" if eh_numerico else "03"
                                }
                                eh_numerico = False
                                tabela_de_simbolos.append(simb)
                                fluxo_codigo.append((str(cont), '99'))
                                cont += 1
                            else:
                                print("> ERRO SEMANTICO!! Variavel <" + palavra + "> não foi delcarada no campo de declaração.")
                                return
                        elif palavra.isnumeric():
                            fluxo_codigo.append((palavra, '98'))
                        else:
                            print("> ERRO LÉXICO!! POR FAVOR VERIFIQUE A PALAVRA: " + palavra)
                            return
                    

    print("> Gerando Documento de Fluxo de Tokens...")
    gerar_fluxo_lexico(fluxo_codigo)

    print("> Gerando Tabela de Simbolos...")
    gerar_tabela_de_simbolos(tabela_de_simbolos)

    return fluxo_codigo, tabela_de_simbolos
