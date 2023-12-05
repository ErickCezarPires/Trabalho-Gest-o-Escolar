class avaliacaoaluno:
    def __init__(self,
                id_avaliacao_aluno=None,
                id_aluno=None,
                id_prova=None,
                id_trabalho=None, 
                nota_avaliacao=None, 
                nome_aluno=None
                ):
        self.set_id_avaliacao_aluno(id_avaliacao_aluno)
        self.set_id_aluno(id_aluno)
        self.set_id_prova(id_prova)
        self.set_id_trabalho(id_trabalho)
        self.set_nota_avaliacao(nota_avaliacao)
        self.set_nome_aluno(nome_aluno)

    def get_id_avaliacao_aluno(self):
        return self.id_avaliacao_aluno
    
    def set_id_avaliacao_aluno(self, id_avaliacao_aluno):
        self.id_avaliacao_aluno = id_avaliacao_aluno

    def get_id_aluno(self):
        return self.id_aluno

    def set_id_aluno(self, id_aluno):
        self.id_aluno = id_aluno

    def get_id_prova(self):
        return self.id_prova

    def set_id_prova(self, id_prova):
        self.id_prova = id_prova

    def get_id_trabalho(self):
        return self.id_trabalho

    def set_id_trabalho(self, id_trabalho):
        self.id_trabalho = id_trabalho

    def get_nota_avaliacao(self):
        return self.nota_avaliacao

    def set_nota_avaliacao(self, nota_avaliacao):
        self.nota_avaliacao = nota_avaliacao

    def get_nome_aluno(self):
        return self.nome_aluno

    def set_nome_aluno(self, nome_aluno):
        self.nome_aluno = nome_aluno

    def to_string_prova(self):
        return f"Id_Avaliação_Aluno: {self.get_id_avaliacao_aluno()} | Id_Aluno: {self.get_id_aluno()} | Id_Prova: {self.get_id_prova()} | Nota: {self.get_nota_avaliacao()} | Nome: {self.get_nome_aluno()}"

    def to_string_trabalho(self):
        return f"Id_Avaliação_Aluno: {self.get_id_avaliacao_aluno()} | Id_Aluno: {self.get_id_aluno()} | Id_Trabalho: {self.get_id_trabalho()} | Nota: {self.get_nota_avaliacao()} | Nome: {self.get_nome_aluno()}"
