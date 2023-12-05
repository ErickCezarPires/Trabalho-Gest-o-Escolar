from model.aluno import Aluno
from bson import ObjectId
from conexion.mongo_queries import MongoQueries
import pandas as pd
from reports.relatorios import Relatorio
relatorio=Relatorio()

class controller_aluno:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_aluno(self) -> Aluno:
        self.mongo.connect()

        nome=input("Digite o nome: ")
        idade=input("Digite a idade: ")
        turma=input("Digite a turma: ")
        proximo_aluno = self.mongo.db["aluno"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$aluno', 
                                                            'proximo_aluno': {
                                                                '$max': '$id_aluno'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_aluno': {
                                                                '$sum': [
                                                                    '$proximo_aluno', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])
        
        proximo_aluno_list = list(proximo_aluno)

        if proximo_aluno_list: 
            proximo_aluno = int(proximo_aluno_list[0]['proximo_aluno'])
        else:
            proximo_aluno = 1

        id_aluno = self.mongo.db["aluno"].insert_one({"id_aluno": proximo_aluno, "nome": nome, "idade": idade, "turma": turma})
        df_aluno = self.recupera_aluno(proximo_aluno)
        print(df_aluno)
        novo_aluno = Aluno(df_aluno.id_aluno.values[0], df_aluno.nome.values[0], df_aluno.idade.values[0], df_aluno.turma.values[0])
        print(novo_aluno.to_string())
        self.mongo.close()
        return novo_aluno

    def atualizar_aluno(self) -> Aluno:
        self.mongo.connect()

        id_aluno=int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_ID_Aluno(id_aluno):
            novo_nome=input("Digite o novo nome: ")
            novo_idade=input("Digite a nova idade: ")
            novo_turma=input("Digite a nova turma: ")

            self.mongo.db["aluno"].update_one({"id_aluno": id_aluno}, {"$set": {"nome": novo_nome, "idade" : novo_idade, "turma" : novo_turma}})
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_aluno = self.recupera_aluno(id_aluno)
            # Cria um novo objeto Produto
            aluno_atualizado = Aluno(df_aluno.id_aluno.values[0], df_aluno.nome.values[0], df_aluno.idade.values[0], df_aluno.turma.values[0])
            # Exibe os atributos do novo produto
            print(aluno_atualizado.to_string())
            self.mongo.close()

            return aluno_atualizado
        else:
            print(f"O ID_Aluno {id_aluno} não existe.")
            return None
        
    def excluir_Aluno(self):

        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        id_aluno = int(input("Digite o código do aluno que deseja excluir: "))         

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_ID_Aluno(id_aluno):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_aluno = self.recupera_aluno(id_aluno)
            # Revome o produto da tabela
            self.mongo.db["aluno"].delete_one({"id_aluno": id_aluno})
            # Cria um novo objeto Produto para informar que foi removido
            aluno_excluido = Aluno(df_aluno.id_aluno.values[0], df_aluno.nome.values[0], df_aluno.idade.values[0], df_aluno.turma.values[0])
            # Exibe os atributos do produto excluído
            print("Aluno Removido com Sucesso!")
            print(aluno_excluido.to_string())
            self.mongo.close()
            
    def verifica_existencia_ID_Aluno(self, id_aluno:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

            # Recupera os dados do novo produto criado transformando em um DataFrame
        df_aluno = pd.DataFrame(self.mongo.db["aluno"].find({"id_aluno":id_aluno}, {"id_aluno": 1, "nome": 1, "idade" : 1, "turma" : 1, "_id": 0}))
        print(df_aluno)

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_aluno.empty
    
    def recupera_aluno(self, id_aluno:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_aluno = pd.DataFrame(list(self.mongo.db["aluno"].find({"id_aluno":id_aluno}, {"id_aluno": 1, "nome": 1, "idade" : 1, "turma" : 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_aluno