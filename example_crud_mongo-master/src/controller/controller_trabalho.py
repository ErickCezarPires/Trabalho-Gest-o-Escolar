from model.trabalho import Trabalho
from bson import ObjectId
from conexion.mongo_queries import MongoQueries
import pandas as pd
from reports.relatorios import Relatorio
from datetime import datetime, date, timedelta
relatorio=Relatorio()

class controller_trabalho:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_trabalho(self) -> Trabalho:
        self.mongo.connect()

        qtdCriteriosAvaliados = input("Digite a quantidade de critérios avaliados que o trabalho terá: ")
        dateEntrega = datetime.today()+timedelta(int(input(f"Quantos dias à frente da data {datetime.today().strftime('%d-%m-%Y')} a trabalho deverá ser entregue? ")))
        proximo_trabalho = self.mongo.db["trabalho"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$trabalho', 
                                                            'proximo_trabalho': {
                                                                '$max': '$id_trabalho'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_trabalho': {
                                                                '$sum': [
                                                                    '$proximo_trabalho', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_trabalho_list = list(proximo_trabalho)

        if proximo_trabalho_list: 
            proximo_trabalho = int(proximo_trabalho_list[0]['proximo_trabalho'])
        else:
            proximo_trabalho = 1

        id_trabalho = self.mongo.db["trabalho"].insert_one({"id_trabalho": proximo_trabalho, "qtdCriteriosAvaliados": qtdCriteriosAvaliados, "dateEntrega": f"{dateEntrega}"})
        df_trabalho = self.recupera_trabalho(proximo_trabalho)
        print(df_trabalho)
        novo_trabalho = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdCriteriosAvaliados.values[0], df_trabalho.dateEntrega.values[0])
        print(novo_trabalho.to_string())
        self.mongo.close()
        return novo_trabalho

    def atualizar_trabalho(self) -> Trabalho:
        self.mongo.connect()

        id_trabalho=int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_ID_Trabalho(id_trabalho):
            nova_qtdCriteriosAvaliados = input("Digite a nova quantidade de critérios avaliados: ")

            self.mongo.db["trabalho"].update_one({"id_trabalho": id_trabalho}, {"$set": {"qtdCriteriosAvaliados": nova_qtdCriteriosAvaliados}})
            df_trabalho = self.recupera_trabalho(id_trabalho)
            trabalho_atualizado = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdCriteriosAvaliados.values[0], df_trabalho.dateEntrega.values[0])
            print(trabalho_atualizado.to_string())
            self.mongo.close()
            return trabalho_atualizado
        else:
            print(f"O código {id_trabalho} não existe.")
            return None
        
    def excluir_trabalho(self):

        self.mongo.connect()

        id_trabalho = int(input("Digite o código do trabalho que deseja excluir: "))         

        if not self.verifica_existencia_ID_Trabalho(id_trabalho):            
            df_trabalho = self.recupera_trabalho(id_trabalho)
            self.mongo.db["trabalho"].delete_one({"id_trabalho": id_trabalho})
            trabalho_excluida = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdCriteriosAvaliados.values[0], df_trabalho.dateEntrega.values[0])
            print("Trabalho removido com sucesso!")
            print(trabalho_excluida.to_string())
            self.mongo.close()
            
    def verifica_existencia_ID_Trabalho(self, id_trabalho:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        df_trabalho = pd.DataFrame(self.mongo.db["trabalho"].find({"id_trabalho":id_trabalho}, {"id_trabalho": 1, "qtdCriteriosAvaliados": 1, "dateEntrega" : 1, "_id": 0}))
        print(df_trabalho)

        if external:
            self.mongo.close()

        return df_trabalho.empty
    
    def recupera_trabalho(self, id_trabalho:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_trabalho = pd.DataFrame(list(self.mongo.db["trabalho"].find({"id_trabalho":id_trabalho}, {"id_trabalho": 1, "qtdCriteriosAvaliados": 1, "dateEntrega" : 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_trabalho