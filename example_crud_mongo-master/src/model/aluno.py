class Aluno:
    def __init__(self,
                 id_aluno:int=None,
                 nome:str=None, 
                 idade:str=None,
                 turma:str=None,
                 ):
        self.set_id_aluno(id_aluno)
        self.set_nome(nome) 
        self.set_idade(idade)
        self.set_turma(turma)

    def set_id_aluno(self, id_aluno:int):
        self.id_aluno = id_aluno
    
    def set_nome(self, nome:str):
        self.nome = nome
        
    def set_idade(self, idade:str):
        self.idade = idade

    def set_turma(self, turma:str):
        self.turma = turma

    def get_id_aluno(self) -> int:
          return self.id_aluno

    def get_nome(self) -> str:
          return self.nome

    def get_idade(self) -> str:
          return self.idade

    def get_turma(self) -> str:
          return self.turma
    
    def to_string(self) -> str:
          return f"ID :{self.get_id_aluno()} | Nome :{self.get_nome()} | Idade :{self.get_idade()} | Turma :{self.get_turma()}"


















   
