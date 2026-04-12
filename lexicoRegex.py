import sys

def analise(pathArquivo):
    with open(pathArquivo, 'r') as f:
        linhas = f.readlines()
    
    tabela = []
    erro = ""
    for numeroDaLinha, linha in enumerate(linhas, 1):
        posicao = 0
        while posicao < len(linha):            
            caractere = linha[posicao]            
            if caractere in ' \t':
                posicao += 1
                continue
            
            if caractere == '\n' or caractere == '\r':
                break
            
            if caractere.isalpha():
                inicioToken = posicao
                while posicao < len(linha) and (linha[posicao].isalpha() or linha[posicao].isdigit()): 
                    posicao += 1
                token = linha[inicioToken:posicao]
                if token == 'int':
                    tabela.append({"tipo":"tipo_variavel", "valor":token, "linha":numeroDaLinha})
                else:
                    tabela.append({"tipo":"identificador_variavel", "valor":token, "linha":numeroDaLinha})
                continue
            
            if caractere.isdigit():
                inicioToken = posicao
                while posicao < len(linha) and linha[posicao].isdigit(): 
                    posicao += 1
                token = linha[inicioToken:posicao]
                tabela.append({"tipo":"numero", "valor":token, "linha":numeroDaLinha})
                continue
            
            if caractere == ';':
                tabela.append({"tipo":"delimitador", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '=':
                tabela.append({"tipo":"atribuicao", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '+':
                tabela.append({"tipo":"soma", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '-':
                tabela.append({"tipo":"subtracao", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '*':
                tabela.append({"tipo":"multiplicacao", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '/':
                tabela.append({"tipo":"divisao", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == '(':
                tabela.append({"tipo":"abre_parenteses", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            if caractere == ')':
                tabela.append({"tipo":"fecha_parenteses", "valor":caractere, "linha":numeroDaLinha})
                posicao += 1
                continue
            
            erro = erro + f"Erro léxico na linha {numeroDaLinha}. Caractere inesperado:{caractere}\n"
            posicao += 1
            continue
    return tabela, erro

tabela, erros = analise(sys.argv[1])

print(f"{'Tipo':<24} {'Valor':<20} {'Linha':<5}")
print('-'*60)
for token in tabela:
    print(f"{token['tipo']:<24} {token['valor']:<20} {token['linha']:<5}")

print(erros)


            
