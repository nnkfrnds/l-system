from typing import Dict, Set, List, Tuple
from dataclasses import dataclass, field

@dataclass
class Estado:
    identificador: str
    eh_nao_terminal: bool = False
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
    alfabeto_pilha: Set[str]
    
    def validar_cadeia(self, iteracoes: int) -> bool:
        return self.debug_validacao(iteracoes)
    
    def debug_validacao(self, iteracoes: int) -> bool:
        cadeia = self.l_system.gerar_cadeia(iteracoes)
        pilha: List[str] = ['$']  # Símbolo inicial de pilha
        
        print(f"Iniciando validação da cadeia: {cadeia}")
        
        for simbolo in cadeia:
            print(f"\nProcessando símbolo: {simbolo}")
            
            transicoes_validas = [
                t for t in self.construir_transicoes()
                if (t.estado_origem == self.estado and 
                    t.simbolo_leitura == simbolo and 
                    (not t.simbolo_pilha or 
                     not pilha or 
                     t.simbolo_pilha == pilha[-1]))
            ]
            
            if not transicoes_validas:
                print(f"Nenhuma transição válida encontrada para o símbolo {simbolo}")
                return False
            
            transicao = transicoes_validas[0]
            
            print(f"Transição escolhida:")
            print(f"  Origem: {transicao.estado_origem.identificador}")
            print(f"  Destino: {transicao.estado_destino.identificador}")
            print(f"  Símbolo de leitura: {transicao.simbolo_leitura}")
            print(f"  Símbolo de pilha: {transicao.simbolo_pilha}")
            print(f"  Símbolos a empilhar: {transicao.simbolos_empilhar}")
            
            pilha = transicao.aplicar(pilha)
            
            print(f"Pilha após transição: {pilha}")
        
        resultado_final = len(pilha) == 1 and pilha[0] == '$'
        
        print("\nValidação concluída:")
        print(f"Resultado: {resultado_final}")
        
        return resultado_final
    
    def construir_transicoes(self) -> List[Transicao]:
        transicoes = []
        
        # Adiciona transições para cada regra de produção (símbolos não terminais)
        for simbolo, producao in self.l_system.regras_producao.items():
            transicoes.append(Transicao(
                Estado(simbolo, eh_nao_terminal=True), 
                Estado(producao, eh_nao_terminal=True), 
                simbolo, '$', list(producao)
            ))
        
        # Adiciona transições para símbolos terminais
        for simbolo in self.l_system.alfabeto:
            transicoes.append(Transicao(
                Estado(simbolo, eh_nao_terminal=False), 
                Estado(simbolo, eh_nao_terminal=False), 
                simbolo, simbolo, []
            ))
        
        return transicoes

def exemplo_automato():
    # Definição do sistema L
    l_system = LSystem(
        alfabeto={'A', 'B'},
        axioma='A',
        regras_producao={
            'A': 'AB',
            'B': 'A'
        }
    )
    
    # Criação do autômato com pilha
    automato = AutomatoPilha(
        estado=Estado('q0', eh_estado_inicial=True, eh_estado_final=True),
        l_system=l_system,
        alfabeto_pilha={'a', 'b', '$'}
    )
    
    # Testes com função de depuração
    for iteracoes in range(1, 4):
        print(f"Cadeia após {iteracoes} iterações: {automato.validar_cadeia(iteracoes)}")

# Executa o exemplo
exemplo_automato()