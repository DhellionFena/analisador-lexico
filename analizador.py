from funcoes import getAlgoritmo, analizador_lexico, separar_texto

# AQUI É A MAIN DO NOSSO PROGRAMA

texto = getAlgoritmo('racobaldo.txt')       # Pegando o texto do algoritmo
texto = texto.split()                       # Separando a string e transformando em Lista
texto = separar_texto(texto)                # Limpando a lista dos caracteres especiais
analizador_lexico(texto)                    # Aqui é onde a magica acontece  >:)



# Coisas que precisam ser revisadas: esse separador de texto ta me cheirando a POG.

# Algumas palavras estão sendo salvas na tabela de simbolos mesmo não sendo rotulos
# na teoria isso não é um problema já que nosso papel não é semantico, o problema é
# que caso alguma palavra dentro de uma string não se encaixe na REGEX de rotulos
# o analizador léxico vai dizer que é um erro. (sendo que não é.)

# De Resto, nosso código está praticamente finalizado, só será necessário conferir se
# todos os caracteres especiais estão dentro da lista do separador de texto e também é
# válido comentar as funções de cada código para facilitar a vida de quem vai apresentá-lo.