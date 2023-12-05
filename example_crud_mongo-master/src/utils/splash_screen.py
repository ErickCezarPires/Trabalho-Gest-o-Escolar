from utils import config

class SplashScreen:

    def __init__(self):
        # Nome(s) do(s) criador(es)
        self.created_by = """Bernardo N.                             #
        #              Erick C.                                #
        #              Henrique A.                             # 
        #              Mateus P.                               #
        #              Pedro B.                                #
        #              Pedro G.                                #"""
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                    GESTÃO ESCOLAR                    #  
        #                                                      #   
        #  TOTAL DE REGISTROS:                                 #   
        #      1 - ALUNOS:         {str(self.get_documents_count(collection_name="aluno")).rjust(5)}                       #
        #      2 - PROVAS:         {str(self.get_documents_count(collection_name="prova")).rjust(5)}                       #
        #      3 - TRABALHOS:      {str(self.get_documents_count(collection_name="trabalho")).rjust(5)}                       #
        #      4 - AVALIAÇÕES:     {str(self.get_documents_count(collection_name="avaliacaoAluno")).rjust(5)}                       #
        #                                                      #
        #  CRIADO POR: {self.created_by}                       
        #                                                      #
        #  PROFESSOR:  {self.professor}               # 
        #                                                      #
        #  DISCIPLINA: {self.disciplina}                          #
        #              {self.semestre}                                  #
        ########################################################
        """