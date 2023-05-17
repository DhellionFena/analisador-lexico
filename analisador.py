from funcoes import getAlgoritmo, analisador_lexico, separar_texto, analisador_sintatico

# AQUI É A MAIN DO NOSSO PROGRAMA

texto = getAlgoritmo('racobaldo CERTO.txt')       # Pegando o texto do algoritmo
texto = texto.split()                       # Separando a string e transformando em Lista
texto = separar_texto(texto)                # Limpando a lista dos caracteres especiais
tokens = analisador_lexico(texto)           # Aqui é onde a magica acontece  >:)
analisador_sintatico(tokens)                # Aqui é onde a magica acontece  >:) (PARTE 2)