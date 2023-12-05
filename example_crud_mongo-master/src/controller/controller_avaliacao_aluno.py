from model.avaliacao_aluno import avaliacaoaluno
from model.aluno import Aluno
from controller.controller_aluno import controller_aluno
from model.prova import Prova
from controller.controller_prova import controller_prova
from model.trabalho import Trabalho
from controller.controller_trabalho import controller_trabalho
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio
from utils import config
from model.aluno import Aluno
from bson import ObjectId
from conexion.mongo_queries import MongoQueries
import pandas as pd
from reports.relatorios import Relatorio

relatorio = Relatorio()

class controller_avaliacao_aluno:

    def __init__(self):
        self.ctrl_aluno = controller_aluno()
        self.ctrl_prova = controller_prova()
        self.ctrl_trabalho = controller_trabalho()
        self.mongo = MongoQueries()

    def inserir_prova(self):
        self.mongo.connect()

        self.listar_provas(opc=1)
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(id_prova)
        if prova is None:
            return None

        turmas = self.listar_turmas()
        if len(turmas.turma.values) == 0:
            return None
        
        turma = input("Informe a para a qual a avaliação foi aplicada: ")
        df_alunos_turma = self.recuperar_alunos_turma(turma=turma)
        print(len(df_alunos_turma.id_aluno.values))
        for index in range(0, len(df_alunos_turma.id_aluno.values)):
            nota_aluno = int(input(f"Informe a nota do aluno {df_alunos_turma.nome.values[index]}: "))
            proximo_id_av_aluno = self.mongo.db["avaliacao_aluno"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$avaliacao_aluno', 
                                                            'proximo_id_av_aluno': {
                                                                '$max': '$id_avaliacao'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_id_av_aluno': {
                                                                '$sum': [
                                                                    '$proximo_id_av_aluno', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])
            
            proximo_id_av_aluno_list = list(proximo_id_av_aluno)
            if proximo_id_av_aluno:
                proximo_id_av_aluno = int(proximo_id_av_aluno_list[0]['proximo_id_av_aluno'])
            else:
                proximo_id_av_aluno = 1  

            data = dict(codigo=proximo_id_av_aluno, id_aluno=int(df_alunos_turma.id_aluno.values[index]), id_prova=id_prova, id_trabalho=0, nota_avaliacao=nota_aluno, nome_aluno= df_alunos_turma.nome.values[index])
            self.mongo.db["avaliacao_aluno"].insert_one(data)

            config.clear_console()
            self.recuperar_av_alunoProva(prova=id_prova)
            print("")

        self.mongo.close()
    
    def inserir_trabalho(self):
        oracle = OracleQueries()

        self.listar_trabalhos(oracle, need_connect=True, opc=1)
        id_trabalho = int(input("Digite o ID do Trabalho: "))
        trabalho = self.valida_trabalho(oracle, id_trabalho)
        if trabalho is None:
            return None

        turmas = self.listar_turmas(oracle, need_connect=True)
        if len(turmas.turma.values) == 0:
            return None
        
        turma = input("Informe a turma para a qual o trabalho foi aplicado: ")
        df_alunos_turma = self.recuperar_alunos_turma(oracle, need_connect=True, turma=turma)
        for index in range(0, len(df_alunos_turma.id_aluno.values)):
            nota_aluno = float(input(f"Informe a nota do aluno {df_alunos_turma.nome.values[index]}: "))

            proximo_id_av_aluno = self.mongo.db["avaliacao_aluno"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$avaliacao_aluno', 
                                                            'proximo_id_av_aluno': {
                                                                '$max': '$id_avaliacao'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_id_av_aluno': {
                                                                '$sum': [
                                                                    '$proximo_id_av_aluno', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])
            
            proximo_id_av_aluno_list = list(proximo_id_av_aluno)
            if proximo_id_av_aluno:
                proximo_id_av_aluno = int(proximo_id_av_aluno_list[0]['proximo_id_av_aluno'])
            else:
                proximo_id_av_aluno = 1
            data = dict(codigo=proximo_id_av_aluno, id_aluno=int(df_alunos_turma.id_aluno.values[index]), id_prova=0, id_trabalho=id_trabalho, nota_avaliacao=nota_aluno, nome_aluno=df_alunos_turma.nome.values[index])
            self.mongo.db["avaliacao_aluno"].insert_one(data)
            config.clear_console()
            self.recuperar_av_alunoTrabalho(trabalho=id_trabalho)
            print("")
        self.mongo.close()



    def alterar_prova(self):
        self.mongo.connect()

        self.listar_provas()
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(id_prova)
        if prova is None:
            print("Prova prova não existe!")
            return None
        
        config.clear_console(1)
        df_av_alunoProva = self.recuperar_av_alunoProva(prova=id_prova)
        avAlunoAlterar = int(input("Digite o código da avliação(coluna Avaliacão) que deseja alterar: "))
        if avAlunoAlterar in df_av_alunoProva.avaliacao.values:
            nova_nota = float(input("Digite a nova nota: "))
            self.mongo.db["avaliacao_aluno"].updateOne(
                                                        { "id_avaliacao_aluno": avAlunoAlterar },
                                                        { "$set": { "nota_avaliacao": nova_nota } }
                                                        )
            df_av_aluno = pd.DataFrame(list(self.mongo.db.avaliacao_aluno.find(
                                                                                { "id_avaliacao_aluno": avAlunoAlterar },
                                                                                { "_id": 0,
                                                                                  "id_avaliacao_aluno": 1,
                                                                                  "id_aluno": 1,
                                                                                  "id_prova": 1,
                                                                                  "nota_avaliacao": 1,
                                                                                  "nomealuno": 1 })))
            
            editav_aluno = avaliacaoaluno(df_av_aluno.id_avaliacao_aluno.values[0], df_av_aluno.id_aluno.values[0],df_av_aluno.id_prova.values[0], 0, df_av_aluno.nota_avaliacao.values[0], df_av_aluno.nomealuno.values[0])
            print(editav_aluno.to_string_prova())
            return editav_aluno
        
        else:
            print("Esta avaliação de aluno não existe")
        
        self.mongo.close()


    def alterar_trabalho(self):
        self.mongo.connect()

        self.listar_trabalhos()
        id_trabalho = int(input("Digite o ID do Trabalho: "))
        trabalho = self.valida_trabalho(id_trabalho)
        if trabalho is None:
            print("Trabalho não Existe!")
            return None
        
        config.clear_console(1)
        df_av_alunoTrabalho = self.recuperar_av_alunoTrabalho(trabalho=id_trabalho)
        avAlunoAlterar = int(input("Digite o código da avliação(coluna Avaliacão) que deseja alterar: "))
        if avAlunoAlterar in df_av_alunoTrabalho.avaliacao.values:
            nova_nota = float(input("Digite a nova nota: "))
            self.mongo.db["avaliacao_aluno"].updateOne(
                                                        { "id_avaliacao_aluno": avAlunoAlterar },
                                                        { "$set": { "nota_avaliacao": nova_nota } }
                                                        )
            df_av_aluno = pd.DataFrame(list(self.mongo.db.avaliacao_aluno.find(
                                                                                { "id_avaliacao_aluno": avAlunoAlterar },
                                                                                { "_id": 0,
                                                                                  "id_avaliacao_aluno": 1,
                                                                                  "id_aluno": 1,
                                                                                  "id_trabalho": 1,
                                                                                  "nota_avaliacao": 1,
                                                                                  "nomealuno": 1 })))
            editav_aluno = avaliacaoaluno(df_av_aluno.id_avaliacao_aluno.values[0], df_av_aluno.id_aluno.values[0], 0, df_av_aluno.id_trabalho.values[0], df_av_aluno.nota_avaliacao.values[0], df_av_aluno.nomealuno.values[0])
            print(editav_aluno.to_string_trabalho())
            return editav_aluno
        
        else:
            print("Esta avaliação de aluno não existe")

        self.mongo.close()


    def excluir_prova(self):
        self.mongo.connect()

        self.listar_provas()
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(id_prova)
        if prova is None:
            print("Esta prova não não existe para ser excluida")
            return None
        
        self.mongo.db["avaliacao_aluno"].deleteMany( { "id_prova": id_prova } )
        print(f'Avaliações de aluno removidas para a prova {id_prova}')
        self.mongo.close()
        return None

    def excluir_trabalho(self):
        oracle = OracleQueries(can_write=True)

        self.listar_trabalhos(oracle, need_connect=True)
        id_trabalho = int(input("Digite o ID do trabalho: "))
        trabalho = self.valida_trabalho(oracle, id_trabalho)
        if trabalho is None:
            print("Este não trabalho não existe para ser excluido")
            return None
        
        self.mongo.db["avaliacao_aluno"].deleteMany( { "id_trabalho": id_trabalho } )
        print(f'Avaliações de aluno removidas para o trabalho {id_trabalho}')
        return None    




    def listar_provas(self, oracle:OracleQueries, need_connect:bool=False, opc=0):
        if opc == 1:
            #self.mongo.db["aluno"].find({ "turma": opc },{ "id_aluno": 1, "nome": 1, "_id": 0 })
            df_provas = pd.DataFrame(list(self.mongo.dbdb["prova"].aggregate([{
                "$match": {
                    "id_prova": { "$ne": 0 }
                }
                     },{ "$lookup": {
             "from": "avaliacao_aluno",
             "let": { "prova_id": "$id_prova" },
            "pipeline": [
               {
                 "$match": {
                   "$expr": { "$eq": ["$id_prova", "$$prova_id"] }
                 }
               },
               {
                 "$limit": 1
               }
             ],
             "as": "avaliacoes"
            }
            },
            {
              "$match": {
                "avaliacoes": { "$size": 0 }
              }
            },
            {
              "$project": {
                "_id": 0,
                "Prova": "$id_prova",
                "data_aplicacao": {
                  "$dateToString": {
                    "format": "%d-%m-%Y",
                    "date": "$date_aplicacao"
                  }
                }
              }
            }
            ]) ) )   
             
        else:

            df_provas = pd.DataFrame(list(
                self.mongo.db["prova"].aggregate([
                                                    {
                                                      "$match": {
                                                        "id_prova": { "$ne": 0 }
                                                      }
                                                    },
                                                    {
                                                      "$lookup": {
                                                        "from": "avaliacao_aluno",
                                                        "let": { "prova_id": "$id_prova" },
                                                        "pipeline": [
                                                          {
                                                            "$match": {
                                                              "$expr": { "$eq": ["$id_prova", "$$prova_id"] }
                                                            }
                                                          },
                                                          {
                                                            "$limit": 1
                                                          }
                                                        ],
                                                        "as": "avaliacoes"
                                                      }
                                                    },
                                                    {
                                                      "$match": {
                                                        "avaliacoes": { "$ne": [] }
                                                      }
                                                    },
                                                    {
                                                      "$project": {
                                                        "_id": 0,
                                                        "Prova": "$id_prova",
                                                        "data_aplicacao": {
                                                          "$dateToString": {
                                                            "format": "%d-%m-%Y",
                                                            "date": "$date_aplicacao"
                                                          }
                                                        }
                                                      }
                                                    }
                                                  ]))) 
        print(df_provas)

    def listar_trabalhos(self, oracle:OracleQueries, need_connect:bool=False, opc=0):
        if opc == 1: 
            df_trabalhos = pd.DataFrame(list(
                self.mongo.db["trabalho"].aggregate([
                                                      {
                                                        "$match": {
                                                          "id_trabalho": { "$ne": 0 }
                                                        }
                                                      },
                                                      {
                                                        "$lookup": {
                                                          "from": "avaliacao_aluno",
                                                          "let": { "trabalho_id": "$id_trabalho" },
                                                          "pipeline": [
                                                            {
                                                              "$match": {
                                                                "$expr": { "$eq": ["$id_trabalho", "$$trabalho_id"] }
                                                              }
                                                            },
                                                            {
                                                              "$limit": 1
                                                            }
                                                          ],
                                                          "as": "avaliacoes"
                                                        }
                                                      },
                                                      {
                                                        "$match": {
                                                          "avaliacoes": { "$size": 0 }
                                                        }
                                                      },
                                                      {
                                                        "$project": {
                                                          "_id": 0,
                                                          "Trabalho": "$id_trabalho",
                                                          "data_entrega": {
                                                            "$dateToString": {
                                                              "format": "%d-%m-%Y",
                                                              "date": "$date_entrega"
                                                            }
                                                          }
                                                        }
                                                      }
                                                    ])))
            print(df_trabalhos)

        else:

            df_trabalhos = pd.DataFrame(list( self.mongo.db["trabalho"].aggregate([
                                                                               {
                                                                                 "$match": {
                                                                                   "id_trabalho": { "$ne": 0 }
                                                                                 }
                                                                               },
                                                                               {
                                                                                 "$lookup": {
                                                                                   "from": "avaliacao_aluno",
                                                                                   "let": { "trabalho_id": "$id_trabalho" },
                                                                                   "pipeline": [
                                                                                     {
                                                                                       "$match": {
                                                                                         "$expr": { "$eq": ["$id_trabalho", "$$trabalho_id"] }
                                                                                       }
                                                                                     },
                                                                                     {
                                                                                       "$limit": 1
                                                                                     }
                                                                                   ],
                                                                                   "as": "avaliacoes"
                                                                                 }
                                                                               },
                                                                               {
                                                                                 "$match": {
                                                                                   "avaliacoes": { "$ne": [] }
                                                                                 }
                                                                               },
                                                                               {
                                                                                 "$project": {
                                                                                   "_id": 0,
                                                                                   "Trabalho": "$id_trabalho",
                                                                                   "data_entrega": {
                                                                                     "$dateToString": {
                                                                                       "format": "%d-%m-%Y",
                                                                                       "date": "$date_entrega"
                                                                                     }
                                                                                   }
                                                                                 }
                                                                               }
                                                                             ])))
        
            print(df_trabalhos)


    def listar_turmas(self):
        df_turmas = pd.DataFrame(list(self.mongo.db["aluno"].aggregate([
                                                                            {
                                                                                "$group": {
                                                                                    "_id": "$turma"
                                                                                }
                                                                            },
                                                                            {
                                                                                "$project": {
                                                                                    "_id": 0,
                                                                                    "turma": "$_id"
                                                                                }
                                                                            }
                                                                        ])))
        
        print(df_turmas)
        return df_turmas


    def recuperar_alunos_turma(self, turma=""):
        df_alunos = pd.dataframe(list(self.mongo.db["aluno"].find(
                                                                    { "turma": turma },
                                                                    { "_id": 0, "id_aluno": 1, "nome": 1 }
                                                                  )))        
        return df_alunos
    

    
    def recuperar_av_alunoProva(self, prova=0):

        df_av_alunoProva = pd.DataFrame(list(self.mongo.db["avaliacao_aluno"].aggregate([
                                                                                   {
                                                                                     "$match": {
                                                                                       "id_prova": prova
                                                                                     }
                                                                                   },
                                                                                   {
                                                                                     "$project": {
                                                                                       "_id": 0,
                                                                                       "avaliacao": "$id_avaliacao_aluno",
                                                                                       "prova": "$id_prova",
                                                                                       "nome": "$nomealuno",
                                                                                       "nota": "$nota_avaliacao"
                                                                                     }
                                                                                   }
                                                                                 ])))
        
        print(df_av_alunoProva)
        return df_av_alunoProva


    def recuperar_av_alunoTrabalho(self, trabalho=0):
        df_av_alunoTrabalho = pd.DataFrame(list( self.mongo.db["avaliacao_aluno"].aggregate([
                                                                                   {
                                                                                     "$match": {
                                                                                       "id_trabalho": trabalho
                                                                                     }
                                                                                   },
                                                                                   {
                                                                                     "$project": {
                                                                                       "_id": 0,
                                                                                       "avaliacao": "$id_avaliacao_aluno",
                                                                                       "trabalho": "$id_trabalho",
                                                                                       "nome": "$nomealuno",
                                                                                       "nota": "$nota_avaliacao"
                                                                                     }
                                                                                   }
                                                                                 ])))
        print(df_av_alunoTrabalho)
        return df_av_alunoTrabalho



    def valida_prova(self, oracle:OracleQueries, id_prova:int=None) -> Prova:
        if self.ctrl_prova.verifica_existencia_id_prova( id_prova):
            print(f"Não existe na base, prova cadastrada com o {id_prova}")
            return None
        else:
            df_prova = pd.DataFrame(list(self.mongo.db["prova"].find({
                                                                      "id_prova": id_prova },
                                                                     { "_id": 0,
                                                                       "id_prova": 1,
                                                                        "quant_questao": 1,
                                                                        "date_aplicacao": { "$dateToString": { "format": "%d-%m-%Y", "date": "$date_aplicacao" } } } )))
            prova = Prova(df_prova.id_prova.values[0], df_prova.quant_questao.values[0], df_prova.date_aplicacao[0] )
            return prova
        
    def valida_trabalho(self, oracle:OracleQueries, id_trabalho:int=None) -> Trabalho:
        if self.ctrl_trabalho.verifica_existencia_id_trabalho(oracle, id_trabalho):
            print(f"Não existe na base, trabalho cadastrada com o {id_trabalho}")
            return None
        else:
            df_trabalho = pd.DataFrame(list(self.mongo.db["trabalho"].find(
                                                                            {"id_trabalho": id_trabalho },
                                                                            { "_id": 0,
                                                                              "id_trabalho": 1,
                                                                               "qtdcriteriosavaliados": 1,
                                                                               "data_entrega": { "$dateToString": { "format": "%d-%m-%Y", "date": "$date_entrega" } } })))
            trabalho = Trabalho(df_trabalho.id_trabalho.values[0],df_trabalho.qtdcriteriosavaliados.values[0], df_trabalho.data_entrega.values[0] )
            return trabalho
        