# reader.py
import webbrowser

import ply.lex as lex
from my_utils import slurp, replace_multiple, getKeyFromIndex


class Reader:
    # Tokens
    tokens = ("COUNTRY", "CAPITAL", "CURRENCY", "LANGUAGE", "COMMENTARY", "NEWLINE")

    # States
    states = (
        ("capital", "exclusive"),
        ("currency", "exclusive"),
        ("language", "exclusive"),
    )

    # Ignore rule
    t_ANY_ignore = r","

    # Funcoes de definicao de campo lexical


    # Função que serve para reconhecer o campo Country do ficheiro de texto
    def t_COUNTRY(self, t):
        r"([A-Z]|[a-z])[^,]+"
        t.type = "COUNTRY"
        t.lexer.begin("capital")
        return t

    # Função que serve para reconhecer o campo Capital do ficheiro de texto
    def t_capital_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CAPITAL"
        t.lexer.begin("currency")
        return t

    # Função que serve para reconhecer o campo Currency do ficheiro de texto
    def t_currency_STR(self, t):
        r'"([A-Z][a-z]*,?\s?)*"|(([A-Z]|[a-z])[^,]+)'
        t.type = "CURRENCY"
        t.lexer.begin("language")
        return t

    # Função que serve para reconhecer o campo Language do ficheiro de texto
    def t_language_STR(self, t):
        r'".+"|(([A-Z]|[a-z])[^\n]+)'
        t.type = "LANGUAGE"
        t.lexer.begin("INITIAL")
        return t

    # Função para reconhecer comentários
    def t_COMMENTARY(self, t):
        r"\#[^\n]+"
        pass

    # Função que serve para reconhecer o "parágrafo"/"\n"/nova linha
    def t_NEWLINE(self, t):
        r"\n"
        pass

    # Função que retorna um erro caso o token lido não seja o esperado
    def t_ANY_error(self, t):
        print(f"Unexpected token: {t.value[:20]}")
        exit(1)

    # Inicializador do objeto
    def __init__(self, filename):
        self.lexer = None
        self.filename = filename

    # Construtor
    @staticmethod
    def builder(filename, **kwargs):
        obje = Reader(filename)
        obje.lexer = lex.lex(module=obje, **kwargs)
        return obje

    # Função de leitura do doc csv, armazenando o conteudo numa dictionary
    def read(self):
        my_dict = {}
        self.lexer.input(slurp(self.filename))
        i=0
        for token in iter(self.lexer.token, None):
            if i<4:
                my_dict[token.type] = []
                i+=1
            else:
                my_dict[token.type].append(token.value)
        return my_dict

    # Procedimento para printar o dicionário que é lido pela função read
    # Recebe o dicionário
    def print(self, dict1):
        # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
        value_list = []

        # Input do utilizador
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        # Caso existam virgulas no input, o input é dividido para a lista
        if "," in value:
            value_list = value.split(",")

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)
            if element == "COMMENTARY":
                headers.remove(element)

        # Caso a value_list não esteja vazia (printa colunas escolhidas pelo user)
        if value_list:
            key_indexes = []
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for value_single in value_list:
                i = 0
                for key in dict1:
                    if key == value_single:
                        key_indexes.append(i)
                        print(key, end="\t")
                    i+=1

            print()
            key_indexes_size = len(key_indexes)

            value_index = 0

            while value_index < list_length:
                key_index = 0
                while key_index < key_indexes_size:
                    string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "\n": ""})
                    print(string_final, end="\t")
                    key_index += 1
                print()
                value_index += 1


        # Caso o input do user não exista nos headers (printa todas as colunas)
        elif value not in headers:
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for key in dict1:
                print(key, end="\t")
            print()

            value_index = 0
            while value_index < list_length:
                key_index = 0
                while key_index < 4:
                    string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "\n": ""})
                    print(string_final, end="\t")
                    key_index += 1
                print()
                value_index += 1

        # Caso o utilizador tenha inserido apenas o nome de uma coluna (printa apenas uma coluna)
        else:
            print(value)
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "\n": ""})
                print(string_final)

    # Procedimento para imprimir num ficheiro HTML o dicionário que é lido pela função read
    # Recebe o dicionário
    def html(self, dict1):
        f = open("file.html", "w")

        # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
        value_list = []

        # Input do utilizador
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        # Caso existam virgulas no input, o input é dividido para a lista
        if "," in value:
            value_list = value.split(",")

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)
            if element == "COMMENTARY":
                headers.remove(element)

        html = '<html><head><link rel="stylesheet" href="styles.css"></head><body><table><tr>'

        # Caso a value_list não esteja vazia (imprime colunas escolhidas pelo user)
        if value_list:
            key_indexes = []
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for value_single in value_list:
                i = 0
                for key in dict1:
                    if key == value_single:
                        key_indexes.append(i)
                        html += f"<th>{key}</th>"
                    i += 1

            html += "</tr>"
            key_indexes_size = len(key_indexes)

            value_index = 0

            while value_index < list_length:
                key_index = 0
                html += "</tr><tr>"
                while key_index < key_indexes_size:
                    string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "\n": ""})
                    html += f"<td>{string_final}</td>"
                    key_index += 1

                value_index += 1

            html += "</tr>"

        # Caso o input do user não exista nos headers (imprime todas as colunas)
        elif value not in headers:
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for key in dict1:
                html += f"<th>{key}</th>"

            html += "</tr>"
            value_index = 0
            while value_index < list_length:
                key_index = 0
                html += "</tr><tr>"
                while key_index < 4:
                    string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "\n": ""})
                    html += f"<td>{string_final}</td>"
                    key_index += 1
                value_index += 1

        # Caso o utilizador tenha inserido apenas o nome de uma coluna (imprime apenas uma coluna)
        else:
            html += f"<th>{value}</th></tr>"
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "\n": ""})
                html += f"</tr><tr><td>{string_final}</td>"

        html += "</table></body></html>"
        f.write(html)
        f.close()
        webbrowser.open_new_tab("file.html")
        print("Documento HTML gerado com sucesso!")

    # Procedimento para escrever num ficheiro .tex (Latex) as colunas lidas do ficheiro de texto
    # Recebe o filename do ficheiro de texto
    def latex(self, dict1):

        f = open("file.tex", "w")

        # Inicializar lista que será usada caso o utilizador use virgulas para selecionar as colunas
        value_list = []

        # Input do utilizador
        value = input("(Se pretender ver o output da tabela inteira dê enter)\n"
                      "Caso contrário insira um token:  ").upper()

        # Caso existam virgulas no input, o input é dividido para a lista
        if "," in value:
            value_list = value.split(",")

        headers = [member for member in self.tokens]

        for element in headers:
            if element == "NEWLINE":
                headers.remove(element)
            if element == "COMMENTARY":
                headers.remove(element)

        latex = '\documentclass{article}\\begin{document}\\begin{center}\\begin{tabular}{||'

        # Caso a value_list não esteja vazia (imprime colunas escolhidas pelo user)
        if value_list:

            for value_single in value_list:
                latex += 'c '
            latex += '||} \hline '

            key_indexes = []
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            i = 0
            for value_single in value_list:
                j = 0
                for key in dict1:

                    if (key == value_single) & (i<len(value_list)-1):
                        key_indexes.append(j)
                        latex += f"{key} & "
                        i += 1
                    elif key == value_single:
                        key_indexes.append(j)
                        latex += f"{key} \\\\ [0.5ex] \hline \hline "
                        i += 1
                    j += 1

            key_indexes_size = len(key_indexes)

            value_index = 0

            while value_index < list_length:
                key_index = 0
                while key_index < key_indexes_size-1:
                    string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "&": "\\&","\n": ""})
                    latex += f"{string_final} & "
                    key_index += 1
                if key_index == key_indexes_size-1:
                    string_final = dict1[getKeyFromIndex(key_indexes[key_index], dict1)][value_index]
                    string_final = replace_multiple(string_final, {'"': '', "&": "\\&", "\n": ""})
                    latex += f"{string_final} \\\\ \hline "
                value_index += 1

        # Caso o input do user não exista nos headers (imprime todas as colunas)
        elif value not in headers:
            list_length = len(dict1[getKeyFromIndex(0, dict1)])
            for element in headers:
                latex += 'c '
            latex += '||} \hline '

            # Printar headers
            headers_length = len(headers)
            i = 0

            for key in dict1:
                if i < headers_length-1:
                    string_final = replace_multiple(key, {'"': '', "&": "\\&", "\n": ""})
                    latex += f"{string_final} & "
                else:
                    string_final = replace_multiple(key, {'"': '', "&": "\\&", "\n": ""})
                    latex += f"{string_final} \\\\ [0.5ex] \hline \hline "
                i+=1

            # Printar linhas
            value_index = 0
            while value_index < list_length:
                key_index = 0
                while key_index < 4:
                    if key_index < 3:
                        string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                        string_final = replace_multiple(string_final, {'"': '', "\n": "", "&": "\\&"})
                        latex += f"{string_final} & "
                        key_index += 1
                    else:
                        string_final = dict1[getKeyFromIndex(key_index, dict1)][value_index]
                        string_final = replace_multiple(string_final, {'"': '', "\n": "", "&": "\\&"})
                        latex += f"{string_final} \\\\ \hline "
                        key_index += 1
                value_index += 1

        # Caso o utilizador tenha inserido apenas o nome de uma coluna (imprime apenas uma coluna)
        else:
            latex += 'c ||} \hline '
            latex += f"{value}\\\\[0.5ex] \hline\hline "
            for x in dict1[value]:
                string_final = replace_multiple(x, {'"': '', "&": "\\&"})
                latex += f"{string_final} \\\\ \hline "

        latex += "\end{tabular}\end{center}\end{document}"
        f.write(latex)
        f.close()
        webbrowser.open_new_tab("file.tex")
        print("Documento LaTex gerado com sucesso!")
