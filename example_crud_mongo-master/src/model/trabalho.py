from datetime import date

class Trabalho:
    def __init__(self, 
                 id_trabalho:int=None, 
                 qtdCriteriosAvaliados:int=None, 
                 dateEntrega:date=None 
                ):
        self.set_id_trabalho(id_trabalho)
        self.set_qtdCriteriosAvaliados(qtdCriteriosAvaliados)
        self.set_dateEntrega(dateEntrega)

    def set_id_trabalho(self, id_trabalho:int):
        self.id_trabalho = id_trabalho
    
    def set_qtdCriteriosAvaliados(self, qtdCriteriosAvaliados:int):
        self.qtdCriteriosAvaliados = qtdCriteriosAvaliados
    
    def set_dateEntrega(self, dateEntrega:date):
        self.dateEntrega = dateEntrega 
    
    def get_id_trabalho(self) -> int:
        return self.id_trabalho
    
    def get_qtdCriteriosAvaliados(self) -> int:
        return self.qtdCriteriosAvaliados
    
    def get_dateEntrega(self) -> date:
        return self.dateEntrega
    
    def to_string(self) -> str:
        return f"ID: {self.get_id_trabalho()} | Quantidade de Critérios Avaliados: {self.get_qtdCriteriosAvaliados()} | Data de entrega: {self.get_dateEntrega()}"