#python ex1.py --d 30 --a 120 --i 8 --l 4 --axim "FGRBO" --rules "F:F[-G][+G],G:F[-R][+R],R:F[-B][+B],B:F[-O][+O],O:F[-F][+F]"
import turtle
from collections import deque
import argparse
import json
Y = (0, 255, 0)
class LSystem:
    def __init__(self, axiom, rules, angle, distance, largura):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.result = ""
        self.distance = distance
        self.largura = largura

    def generate(self, iterations):
        self.result = self.axiom
        for _ in range(iterations):
            self.result = "".join(self.rules.get(ch, ch) for ch in self.result)

    def draw(self, distance, largura):
        stack = deque()
        turtle.speed(65000)
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

    lsys = LSystem(axiom, rules, angle, distance, largura)
    lsys.generate(iter)  #aqui é o N
    print(lsys.result)
    lsys.draw(distance, largura)
    turtle.done()
