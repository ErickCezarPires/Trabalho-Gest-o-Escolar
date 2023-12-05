from model.prova import Prova
from bson import ObjectId
from conexion.mongo_queries import MongoQueries
import pandas as pd
from reports.relatorios import Relatorio
from datetime import datetime, date, timedelta
relatorio=Relatorio()

class controller_prova:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_prova(self) -> Prova:
        self.mongo.connect()

        quantQuestoes = input("Digite a quantidade de questões: ")
        dateAplicacao = datetime.today()+timedelta(int(input(f"Quantos dias à frente da data {datetime.today().strftime('%d-%m-%Y')} a prova será aplicada? ")))
        proxima_prova = self.mongo.db["prova"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$prova', 
                                                            'proxima_prova': {
                                                                '$max': '$id_prova'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proxima_prova': {
                                                                '$sum': [
                                                                    '$proxima_prova', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proxima_prova_list = list(proxima_prova)

        if proxima_prova_list: 
            proxima_prova = int(proxima_prova_list[0]['proxima_prova'])
        else:
            proxima_prova = 1

        id_prova = self.mongo.db["prova"].insert_one({"id_prova": proxima_prova, "quantQuestoes": quantQuestoes, "dateAplicacao": f"{dateAplicacao}"})
        df_prova = self.recupera_prova(proxima_prova)
        print(df_prova)
        nova_prova = Prova(df_prova.id_prova.values[0], df_prova.quantQuestoes.values[0], df_prova.dateAplicacao.values[0])
        print(nova_prova.to_string())
        self.mongo.close()
        return nova_prova

    def atualizar_prova(self) -> Prova:
        self.mongo.connect()

        id_prova=int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_ID_Prova(id_prova):
            nova_quantQuestoes = input("Digite a nova quantidade de questões: ")

            self.mongo.db["prova"].update_one({"id_prova": id_prova}, {"$set": {"quantQuestoes": nova_quantQuestoes}})
            df_prova = self.recupera_prova(id_prova)
            prova_atualizada = Prova(df_prova.id_prova.values[0], df_prova.quantQuestoes.values[0], df_prova.dateAplicacao.values[0])
            print(prova_atualizada.to_string())
            self.mongo.close()
            return prova_atualizada
        else:
            print(f"O código {id_prova} não existe.")
            return None
        
    def excluir_prova(self):

        self.mongo.connect()

        id_prova = int(input("Digite o código da prova que deseja excluir: "))         

        if not self.verifica_existencia_ID_Prova(id_prova):            
            df_prova = self.recupera_prova(id_prova)
            self.mongo.db["prova"].delete_one({"id_prova": id_prova})
            prova_excluida = Prova(df_prova.id_prova.values[0], df_prova.quantQuestoes.values[0], df_prova.dateAplicacao.values[0])
            print("Prova removida com sucesso!")
            print(prova_excluida.to_string())
            self.mongo.close()
            
    def verifica_existencia_ID_Prova(self, id_prova:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()
        df_prova = pd.DataFrame(self.mongo.db["prova"].find({"id_prova":id_prova}, {"id_prova": 1, "quantQuestoes": 1, "dateAplicacao" : 1, "_id": 0}))
        print(df_prova)

        if external:
            self.mongo.close()

        return df_prova.empty
    
    def recupera_prova(self, id_prova:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_prova = pd.DataFrame(list(self.mongo.db["prova"].find({"id_prova":id_prova}, {"id_prova": 1, "quantQuestoes": 1, "dateAplicacao" : 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_prova