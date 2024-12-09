import turtle
from collections import deque

class LSystem:
    def __init__(self, axiom, rules, angle=60):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.result = ""

    def generate(self, iterations):
        self.result = self.axiom
        for _ in range(iterations):
            self.result = "".join(self.rules.get(ch, ch) for ch in self.result)

    def draw(self):
        stack = deque()
        turtle.speed(0)
        turtle.width(5)
        for cmd in self.result:
            if cmd == "F":
                turtle.forward(20)
            elif cmd == "f":
                turtle.penup()
                turtle.forward(20)
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
            elif cmd.startswith("C"): #caso tenha cores diferentes
                color = tuple(map(int, cmd[1:].split(",")))
                turtle.pencolor(color)

if __name__ == "__main__":

    axiom = "F"
    rules = {
        "F": "F[+F][-F]"
    }
    angle = 60

    lsys = LSystem(axiom, rules, angle)
    lsys.generate(6)  #aqui é o N
    print(lsys.result)
    lsys.draw()
    turtle.done()
