from flask import Flask, render_template
import sys
import re

app = Flask(__name__)

DEFINICAO_TOKENS = [
    (r'\bint\b', 'TIPO_VARIAVEL_INT'),
    (r'\bstr\b', 'TIPO_VARIAVEL_STR'),
    (r'\bfloat\b', 'TIPO_VARIAVEL_FLOAT'),
    (r'[a-zA-Z][a-zA-Z0-9]*', 'IDENTIFICADOR'),
    (r'\d+', 'NUMERO'),
    (r'imprima', 'PRINT'),
    (r'enquanto', 'WHILE'),
    (r'escolha', 'SWITCH'),
    (r'caso', 'CASE'),
    (r'padrao', 'DEFAULT'),
    (r'continue', 'CONTINUE'),
    (r'quebre', 'BREAK'),
    (r'proc', 'PROCEDURE'),
    (r'outro', 'ELSE'),
    (r'para', 'FOR'),
    (r'se', 'IF'),
    (r'>=', 'MAIOR_OU_IGUAL'),
    (r'<=', 'MENOR_OU_IGUAL'),
    (r'!=', 'DIFERENTE'),
    (r'==', 'IGUAL'),
    (r'&&', 'AND'),
    (r'\|\|', 'OR'),
    (r'<', 'MENOR'),
    (r'>', 'MAIOR'),
    (r'\+', 'SOMA'),
    (r'-', 'SUBTRACAO'),
    (r'\*', 'MULTIPLICACAO'),
    (r'/', 'DIVISAO'),
    (r'=', 'ATRIBUICAO'),
    (r';', 'DELIMITADOR'),
    (r'\(', 'ABRE_PARENTHESES'),
    (r'\)', 'FECHA_PARENTHESES'),
    (r'\{', 'ABRE_CHAVES'),
    (r'\}', 'FECHA_CHAVES'),
    (r'##[\s\S]*?##', None),
    (r'\s+', None),
    (r'#.*', None)
]

def analise(pathArquivo):
    with open(pathArquivo, 'r') as f:
        linhas = f.readlines()
    
    tabela = []
    erro = ""
    for numeroDaLinha, linha in enumerate(linhas, 1):
        posicao = 0
        while posicao < len(linha):
            deuMatch = False
            for regra, tipo in DEFINICAO_TOKENS:
                m = re.match(regra, linha[posicao:])
                if m:
                    if tipo:
                        tabela.append({"tipo":tipo, "valor":m.group(0), "linha":numeroDaLinha})
                    posicao += len(m.group(0))
                    deuMatch = True
                    break
            if not deuMatch:
                if linha[posicao] not in ['\n','\r']:
                    erro = erro + f"Erro léxico na linha {numeroDaLinha}. Caractere inesperado:{linha[posicao]}\n"
                posicao += len(linha)
    return tabela, erro

tabela, erros = analise(sys.argv[1])

print(f"{'Tipo':<24} {'Valor':<20} {'Linha':<5}")
print('-'*60)
for token in tabela:
    print(f"{token['tipo']:<24} {token['valor']:<20} {token['linha']:<5}")

print(f"\n{erros}")


@app.route('/')
def hello():
    return render_template("index.html", tokens=tabela, erros=erros, path_arquivo=sys.argv[1], codigo_fonte=open(sys.argv[1], 'r').read())

if __name__ == '__main__':
    app.run(debug=True)

