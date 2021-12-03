# Author: Duarte Melo / Pedro Simões
# Contact: a21149@alunos.ipca.pt / a21140@alunos.ipca.pt
# Program: Comma Separated Values
# Objective: Programa capaz de ler um ficheiro CSV e, dependendo do input do user, reproduzir
# uma tabela csv, html ou mesmo resutados em consola dos dados pedidos

from reader import Reader
from my_utils import printCountryShowStuff
from menu import menu, get_country
from printer import values_print, values_to_html, values_to_latex
# Construção do objeto Reader
leitura = Reader.builder("list1.csv")

# Leitura dos dados da tabela CSV
myDict = leitura.read()

option = menu()

while option != -1:
    if option == 1:
        values_print(myDict)
    elif option == 2:
        values_to_html(myDict)
    elif option == 3:
        values_to_latex(myDict)
    elif option == 4:
        pais = get_country()
        printCountryShowStuff(pais, myDict)
    option = menu()

