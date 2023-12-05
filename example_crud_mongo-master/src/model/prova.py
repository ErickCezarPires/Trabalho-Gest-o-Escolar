from datetime import date

class Prova:
    def __init__(self, 
                 id_prova:int=None, 
                 quantQuestoes:int=None, 
                 dateAplicacao:date=None 
                ):
        self.set_id_prova(id_prova)
        self.set_quantQuestoes(quantQuestoes)
        self.set_dateAplicacao(dateAplicacao)

    def set_id_prova(self, id_prova:int):
        self.id_prova = id_prova
    
    def set_quantQuestoes(self, quantQuestoes:int):
        self.quantQuestoes = quantQuestoes
    
    def set_dateAplicacao(self, dateAplicacao:date):
        self.dateAplicacao = dateAplicacao 
    
    def get_id_prova(self) -> int:
        return self.id_prova

    def get_quantQuestoes(self) -> int:
        return self.quantQuestoes
    
    def get_dateAplicacao(self) -> date:
        return self.dateAplicacao
    
    def to_string(self) -> date:
        return f"id: {self.get_id_prova()} | Quantidade de Questões: {self.get_quantQuestoes()} | Data da prova: {self.get_dateAplicacao()}"