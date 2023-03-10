from funcoes import getAlgoritmo, analizador_lexico, separar_texto

# AQUI É A MAIN DO NOSSO PROGRAMA

texto = getAlgoritmo('racobaldo.txt')       # Pegando o texto do algoritmo
texto = texto.split()                       # Separando a string e transformando em Lista
texto = separar_texto(texto)                # Limpando a lista dos caracteres especiais
analizador_lexico(texto)                    # Aqui é onde a magica acontece  >:)
