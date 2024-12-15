from typing import Dict, Set, List, Tuple
from dataclasses import dataclass, field

@dataclass
class Estado:
    identificador: str
    eh_estado_inicial: bool = False
    eh_estado_final: bool = False

    def __hash__(self):
        return hash(self.identificador)
    
    def __eq__(self, outro):
        return self.identificador == outro.identificador

@dataclass
class Transicao:
    estado_origem: Estado
    estado_destino: Estado
    simbolo_leitura: str
    simbolo_pilha: str
    simbolos_empilhar: List[str]

    def aplicar(self, pilha: List[str]) -> List[str]:
        if self.simbolo_pilha and pilha and pilha[-1] == self.simbolo_pilha:
            pilha.pop()
        pilha.extend(reversed(self.simbolos_empilhar))
        return pilha

@dataclass
class LSystem:
    alfabeto: Set[str]
    simbolos_nao_terminais: Set[str]
    axioma: str
    regras_producao: Dict[str, str]

    def gerar_cadeia(self, iteracoes: int) -> str:
        cadeia_atual = self.axioma
        
        for _ in range(iteracoes):
            nova_cadeia = ""
            for simbolo in cadeia_atual:
                nova_cadeia += self.regras_producao.get(simbolo, simbolo)
            cadeia_atual = nova_cadeia
        
        return cadeia_atual

@dataclass
class AutomatoPilha:
    estado: Estado
    l_system: LSystem
    
    def validar_cadeia(self, iteracoes: int) -> bool:
        cadeia = self.l_system.gerar_cadeia(iteracoes)
        pilha: List[str] = ['$']  # Símbolo inicial de pilha
        
        print(f"Cadeia gerada: {cadeia}")
        
        for simbolo in cadeia:
            transicoes_validas = self.encontrar_transicoes_validas(simbolo, pilha)
            
            if not transicoes_validas:
                print(f"Nenhuma transição válida encontrada para o símbolo '{simbolo}'")
                return False
            
            transicao = transicoes_validas[0]
            pilha = transicao.aplicar(pilha)
            
            print(f"Aplicando transição: {transicao}")
            print(f"Pilha: {pilha}")
        
        print("Validação concluída")
        return len(pilha) == 1 and pilha[0] == '$'
    
    def encontrar_transicoes_validas(self, simbolo: str, pilha: List[str]) -> List[Transicao]:
        transicoes_validas = [
            t for t in self.construir_transicoes()
            if (t.estado_origem == self.estado and 
                t.simbolo_leitura == simbolo and 
                (not t.simbolo_pilha or 
                 not pilha or 
                 t.simbolo_pilha == pilha[-1]))
        ]
        
        # Verifica se o símbolo é terminal ou não terminal
        if simbolo in self.l_system.simbolos_nao_terminais:
            transicoes_validas = [t for t in transicoes_validas if t.simbolo_pilha == '$']
        
        return transicoes_validas
    
    def construir_transicoes(self) -> List[Transicao]:
        transicoes = []
        
        # Adiciona transições para cada regra de produção
        for simbolo, producao in self.l_system.regras_producao.items():
            transicoes.append(Transicao(
                self.estado, self.estado, simbolo, '$', list(producao)
            ))
        
        # Adiciona transições para símbolos terminais
        for simbolo in self.l_system.alfabeto - self.l_system.simbolos_nao_terminais:
            transicoes.append(Transicao(
                self.estado, self.estado, simbolo, simbolo, []
            ))
        
        return transicoes

def exemplo_automato():
    # Definição do sistema L
    l_system = LSystem(
        alfabeto={'A', 'B'},
        simbolos_nao_terminais={'A', 'B'},
        axioma='A',
        regras_producao={
            'A': 'AB',
            'B': 'A'
        }
    )
    
    # Criação do autômato com pilha
    automato = AutomatoPilha(
        estado=Estado('q0', eh_estado_inicial=True, eh_estado_final=True),
        l_system=l_system
    )
    
    # Testes
    for iteracoes in range(1, 4):
        print(f"\nCadeia após {iteracoes} iterações:")
        print(automato.validar_cadeia(iteracoes))

# Executa o exemplo
exemplo_automato()