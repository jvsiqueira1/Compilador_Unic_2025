from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])


class Lexer:
    """Analisador léxico para converter declarações JS (var) para Python."""
    
    def __init__(self, text):
        """Inicializa o lexer com o texto de entrada."""
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def advance(self):
        """Avança a posição e atualiza o caractere atual."""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Pula espaços em branco."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """Lê um número inteiro."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def string(self):
        """Lê uma string entre aspas duplas."""
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()
        return result
    
    def identifier(self):
        """Lê um identificador (nome de variável ou palavra-chave)."""
        result = ''
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        """Retorna o próximo token do texto."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token('NUMBER', self.integer())
            
            if self.current_char == '"':
                return Token('STRING', self.string())
            
            if self.current_char == '=':
                self.advance()
                return Token('EQUALS', '=')
            
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')
            
            if self.current_char.isalpha() or self.current_char == '_':
                ident = self.identifier()
                if ident == 'var':
                    return Token('VAR', 'var')
                else:
                    return Token('IDENTIFIER', ident)
            
            raise Exception(f'Caractere não reconhecido: {self.current_char}')
        
        return Token('EOF', None)


class Transpiler:
    """Parser e Gerador de Código para converter JS para Python."""
    
    def __init__(self, lexer):
        """Inicializa o transpiler com uma instância do Lexer."""
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        """Consome o token esperado e avança para o próximo."""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Token inesperado: esperado {token_type}, encontrado {self.current_token.type}')
    
    def parse_statement(self):
        """Parseia uma declaração var IDENTIFIER = VALOR ; e retorna (nome, valor)."""
        self.eat('VAR')
        
        if self.current_token.type != 'IDENTIFIER':
            raise Exception(f'Esperado IDENTIFIER, encontrado {self.current_token.type}')
        var_name = self.current_token.value
        self.eat('IDENTIFIER')
        
        self.eat('EQUALS')
        
        if self.current_token.type == 'NUMBER':
            var_value = self.current_token.value
            self.eat('NUMBER')
        elif self.current_token.type == 'STRING':
            var_value = self.current_token.value
            self.eat('STRING')
        else:
            raise Exception(f'Esperado NUMBER ou STRING, encontrado {self.current_token.type}')
        
        self.eat('SEMICOLON')
        
        return (var_name, var_value)
    
    def run(self):
        """Processa múltiplas declarações e gera código Python."""
        python_code = []
        
        print("--- LOG DE TRANSPILAÇÃO ---")
        
        while self.current_token.type != 'EOF':
            name, value = self.parse_statement()
            
            if isinstance(value, int):
                hex_value = hex(value)
                print(f"Processando ('{name}', {value}): Hex: {hex_value}")
            elif isinstance(value, str):
                hex_values = [hex(ord(c)) for c in value]
                hex_str = ' '.join(hex_values)
                print(f'Processando (\'{name}\', "{value}"): Hex: {hex_str}')
            
            python_line = f"{name} = {repr(value)}"
            python_code.append(python_line)
        
        return "\n".join(python_code)


def main():
    """Função principal que usa o Transpiler."""
    print("=" * 60)
    print("Transpilador JS para Python")
    print("=" * 60)
    print("\nDigite declarações de variáveis no formato JavaScript:")
    print('Exemplo: var x = 10; var nome = "Lucas";')
    print("Digite 'sair' para encerrar o programa\n")
    
    while True:
        try:
            entrada = input("Digite suas declarações (ou 'sair' para encerrar): ").strip()
            
            if entrada.lower() == 'sair':
                print("\n" + "=" * 60)
                print("Programa encerrado. Até logo!")
                print("=" * 60)
                break
            
            if not entrada:
                print("Por favor, digite uma declaração válida.\n")
                continue
            
            lexer = Lexer(entrada)
            transpiler = Transpiler(lexer)
            
            codigo_final = transpiler.run()
            
            print("\n--- CÓDIGO GERADO (Python) ---")
            print(codigo_final)
            print()
            
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("Programa interrompido pelo usuário. Até logo!")
            print("=" * 60)
            break
        except Exception as e:
            print(f"\nErro: {e}\n")


if __name__ == '__main__':
    main()
