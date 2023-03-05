from tipos import tipos

def getAlgoritmo(nome_do_arquivo):
    with open(nome_do_arquivo, 'r', encoding='utf-8') as arq:
        texto = arq.read()
        #print(texto)
    return texto

'''
TODO:
- Rever a logica de como identificar as palavras pois as variaveis que nao existem podem atrapalhar na hora de reconhecer um tipo.
    Exemplo:
        caso eu crie uma variavel "i", e depois eu vou fazer uma declaração "int b" no codigo. Da forma como está escrito,
        o analizador vai encontrar o "i" de int e achar que é uma variavel solta "i" que eu declarei anteriormente.

- Implementar no lugar dos prints a inserção da tabela de símbolos e o inicio do fluxo de uma linguagem intermediaria.
- Implementar na verificação de criação de variavel a validação Regex que Racoba criou
'''
def analizado_lexico(texto):
    for palavra in texto:
        aux = ''
        for letra in palavra:
            aux += letra
            if letra in tipos:
                print(f"Achei {letra}! seu tipo eh {tipos[letra]}")
            elif aux in tipos:
                print(f"Achei {aux}! seu tipo eh {tipos[aux]}")
            else:
                print(f'nao achei ainda o que significa {aux}')