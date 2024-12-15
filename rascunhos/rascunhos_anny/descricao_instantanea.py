class PDAutomataSnapshot:
    def __init__(self, state, input_remaining, stack):
        """
        Representa uma descrição instantânea de um Autômato de Pilha
        
        :param state: Estado atual do autômato
        :param input_remaining: Parte restante da cadeia de entrada
        :param stack: Conteúdo atual da pilha
        """
        self.state = state
        self.input_remaining = input_remaining
        self.stack = stack.copy()  # Cria uma cópia para evitar modificações inesperadas
    
    def __str__(self):
        """
        Representa a descrição instantânea como uma string legível
        """
        return f"(State: {self.state}, " \
               f"Input: {self.input_remaining}, " \
               f"Stack: {self.stack})"
    
    def __repr__(self):
        """
        Representação formal para debugging
        """
        return self.__str__()
    
    def is_final(self, final_states):
        """
        Verifica se esta configuração é um estado final
        
        :param final_states: Conjunto de estados finais
        :return: Booleano indicando se é um estado final
        """
        return self.state in final_states and len(self.input_remaining) == 0
    
    def can_transition(self, transition_rules):
        """
        Verifica possíveis transições a partir desta configuração
        
        :param transition_rules: Regras de transição do autômato
        :return: Lista de próximas configurações possíveis
        """
        possible_transitions = []
        
        # Lógica de transição de estado
        for rule in transition_rules:
            # Verificar condições de transição
            if (self.state == rule.current_state and 
                (not self.input_remaining or 
                 self.input_remaining[0] == rule.input_symbol) and
                (self.stack and self.stack[-1] == rule.stack_top)):
                
                # Criar nova configuração
                new_input = self.input_remaining[1:] if self.input_remaining else []
                new_stack = self.stack.copy()
                
                # Remover símbolo do topo da pilha
                if rule.stack_top != 'ε':
                    new_stack.pop()
                
                # Adicionar novos símbolos à pilha
                if rule.push_symbols != ['ε']:
                    new_stack.extend(reversed(rule.push_symbols))
                
                new_snapshot = PDAutomataSnapshot(
                    rule.next_state, 
                    new_input, 
                    new_stack
                )
                
                possible_transitions.append(new_snapshot)
        
        return possible_transitions

class TransitionRule:
    def __init__(self, current_state, input_symbol, 
                 stack_top, next_state, push_symbols):
        """
        Representa uma regra de transição para o Autômato de Pilha
        
        :param current_state: Estado atual
        :param input_symbol: Símbolo de entrada
        :param stack_top: Símbolo no topo da pilha
        :param next_state: Próximo estado
        :param push_symbols: Símbolos a serem empilhados
        """
        self.current_state = current_state
        self.input_symbol = input_symbol
        self.stack_top = stack_top
        self.next_state = next_state
        self.push_symbols = push_symbols

# Exemplo de uso
def example_usage():
    # Definir regras de transição para reconhecer palíndromos
    transition_rules = [
        TransitionRule('q0', '0', 'Z', 'q0', ['0', 'Z']),
        TransitionRule('q0', '1', 'Z', 'q0', ['1', 'Z']),
        TransitionRule('q0', 'ε', 'Z', 'q1', ['Z']),
        TransitionRule('q1', '0', '0', 'q1', ['ε']),
        TransitionRule('q1', '1', '1', 'q1', ['ε']),
        TransitionRule('q1', 'ε', 'Z', 'q2', ['ε'])
    ]
    
    # Estado inicial
    initial_snapshot = PDAutomataSnapshot(
        state='q0', 
        input_remaining=['0', '1', '1', '0'], 
        stack=['Z']
    )
    
    # Simular transições
    current_snapshots = [initial_snapshot]
    
    print("Configurações iniciais:")
    for snapshot in current_snapshots:
        print(snapshot)
    
    # Processar transições
    while current_snapshots:
        next_snapshots = []
        
        for snapshot in current_snapshots:
            # Tentar transições
            transitions = snapshot.can_transition(transition_rules)
            next_snapshots.extend(transitions)
        
        current_snapshots = next_snapshots
        
        if current_snapshots:
            print("\nNovas configurações:")
            for snapshot in current_snapshots:
                print(snapshot)

# Executar exemplo
if __name__ == '__main__':
    example_usage()