import turtle
from collections import deque
import argparse
import json
Y = (0, 255, 0)

# Classe do autômato com pilha para o L-System

# Existirá 2 métodos
# Primeiro método = Geração da string após as iteraçõeos
# Segundo método = Validação com pilha da estrutura da string

# Aqui será a classe onde verificaremos se a string passada pelo 
# professor de fato se encaixa com as regras do L-System. 
# Obs.: Start(Axiom) será dado pelo professor. Ele será a string de partida
# para seguir as regras. Pq precisa do autômato? Só comparar não faria sentido? 
# No material , deu a entender que o professor nos daria a string final, mas não
# é verdade.
# O autômato será para fazer essa comparação já que mesmo uma string errada,
# a regras serão aplicadas:
# Exemplo string falha: FFFF[[[[ , A recursão funcionará

class LSystemAutomato:
    def __init__(self,axiom,rules):
        self.axiom = axiom
        self.rules = rules
        self.pilha = []

    def generate(self, iterations):
        self.result = self.axiom
        for _ in range(iterations):
            self.result = "".join(self.rules.get(ch, ch) for ch in self.result)
    
    def validar_string(self, string):
        pilha = []
        ultimo_caractere = None  # Usado para verificar padrões lineares

        for char in string:
            # Verifica duplicação linear (ex.: FF)
            if char == "F" and ultimo_caractere == "F":
                return False  # Sequência inválida encontrada

            # Processamento da pilha para colchetes
            if char == "[":
                pilha.append("[")
            elif char == "]":
                if not pilha or pilha.pop() != "[":
                    return False  # Falha se a pilha está vazia ou há desequilíbrio

            # Verifica caracteres inválidos
            elif char not in self.rules and char not in "+-F":
                return False  # Caracter inválido encontrado

            # Atualiza o último caractere processado
            ultimo_caractere = char

        # Valida que a pilha está vazia ao final (colchetes balanceados)
        return not pilha
        

# Classe que gerará de fato o desenho do LSystem

class LSystem:
    def __init__(self, result, angle, distance, largura):
        self.result = result
        self.angle = angle
        self.result = result
        self.distance = distance
        self.largura = largura

    def draw(self, distance, largura):
        stack = deque()
        turtle.speed(0)
        turtle.width(largura)
        for cmd in self.result:
            if cmd == "F":
                #turtle.pencolor(0, 255, 0)
                turtle.color("black")
                turtle.forward(distance)

            elif cmd == "f":
                turtle.penup()
                turtle.forward(distance)
                turtle.pendown()
            elif cmd == "+":
                turtle.right(self.angle)
            elif cmd == "-":
                turtle.left(self.angle)
            elif cmd == "[":
                pos = turtle.pos()
                angle = turtle.heading()
                stack.append((pos, angle))
            elif cmd == "]":
                pos, angle = stack.pop()
                turtle.penup()
                turtle.setpos(pos)
                turtle.setheading(angle)
                turtle.pendown()
            elif cmd.startswith("S"): #tamanho do galho
                size = int(cmd[1:])
                turtle.width(size)
            elif cmd.startswith("G"): #cor
                turtle.color("green")
                turtle.forward(distance)
            elif cmd.startswith("B"): #cor
                turtle.color("blue")
                turtle.forward(distance)
            elif cmd.startswith("R"): #cor
                turtle.color("red")
                turtle.forward(distance)
            elif cmd.startswith("Y"): #cor
                turtle.color("yellow")
                turtle.forward(distance)
            elif cmd.startswith("O"): #cor
                turtle.color("orange")
                turtle.forward(distance)



'''
'''

def parse_rules(rules_str):
    rules = {}
    for rule in rules_str.split(","):
        key, value = rule.split(":")
        rules[key] = value
    return rules

if __name__ == "__main__":

    axiom = "F"
    rules = {
        "F": "F[+F][-F]"
    }
    #angle = 60

    parser = argparse.ArgumentParser()
    parser.add_argument("--d", type=int, default=10)
    parser.add_argument("--a", type=int, default=60)
    parser.add_argument("--i", type=int, default=6)
    #parser.add_argument("--axiom", type=str, default="F")
    parser.add_argument("--l" , type=int, default=1)
    parser.add_argument("--axim", type=str, default="F")
    #parser.add_argument("--axiom", type=str, default="F")
    parser.add_argument("--rules", type=str, default="F:F[+F][-F]")
    args = parser.parse_args()

    angle = args.a
    distance = args.d
    #axiom = args.axiom
    iter = args.i
    largura = args.l
    #rules = args.rules
    axiom = args.axim
    rules = parse_rules(args.rules)
    
    lsystautom = LSystemAutomato(axiom, rules)
    lsystautom.generate(iter)

    # Verifique se a string gerada é válida
    if not lsystautom.validar_string(lsystautom.result):
        print("A string gerada é inválida. O desenho não será executado.")
    else:
        # Se a string for válida, continue com a execução do desenho
        lsys = LSystem(lsystautom.result, angle, distance, largura)
        print(lsystautom.result)
        lsys.draw(distance, largura)
        turtle.done()