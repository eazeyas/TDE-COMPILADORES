import sys
import re

DEFINICAO_TOKENS = [
    (r'\bint\b', 'tipo_variavel_int'),
    (r'\bstr\b', 'tipo_variavel_str'),
    (r'\bfloat\b', 'tipo_variavel_float'),
    (r'[a-zA-Z][a-zA-Z0-9]*', 'identificador'),
    (r'\d+', 'NUMERO'),
    (r'\+', 'SOMA'),
    (r'-', 'SUBTRACAO'),
    (r'\*', 'MULTIPLICACAO'),
    (r'/', 'DIVISAO'),
    (r'=', 'ATRIBUICAO'),
    (r';', 'DELIMITADOR'),
    (r'>', 'MAIOR'),
    (r'>=', 'MAIOR_OU_IGUAL'),
    (r'<', 'MENOR'),
    (r'<=', 'MENOR_OU_IGUAL'),
    (r'!=', 'DIFERENTE'),
    (r'==', 'IGUAL'),
    (r'&&', 'AND'),
    (r'se', 'IF'),
    (r'outro', 'ELSE'),
    (r'para', 'FOR'),
    (r'enquanto', 'WHILE'),
    (r'escolha', 'SWITCH'),
    (r'caso', 'CASE'),
    (r'padrao', 'DEFAULT'),
    (r'continue', 'CONTINUE'),
    (r'quebre', 'BREAK'),
    (r'proc', 'PROCEDURE'),
    (r'\|\|', 'OR'),
    (r'\(', 'abre_parenteses'),
    (r'\)', 'fecha_parenteses'),
    (r'\{', 'abre_chaves'),
    (r'\}', 'fecha_chaves'),
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
