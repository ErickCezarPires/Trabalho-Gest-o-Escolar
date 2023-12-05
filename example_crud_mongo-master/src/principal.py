from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_aluno import controller_aluno
from controller.controller_prova import controller_prova
from controller.controller_trabalho import controller_trabalho
from controller.controller_avaliacao_aluno import controller_avaliacao_aluno

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_aluno = controller_aluno()
ctrl_prova = controller_prova()
ctrl_trabalho = controller_trabalho()
ctrl_avaliacaoAluno = controller_avaliacao_aluno()

def reports(opcao_relatorio:int=0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_aluno()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_prova()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_trabalho()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_avaliacaoAluno()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_notaAlualhnoTrabo()
    elif opcao_relatorio == 0:
        executaMenu()

def inserir(opcao_inserir:int=0):
    if opcao_inserir == 1:                               
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_aluno()
            novo_aluno = ctrl_aluno.inserir_aluno()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_inserir == 2:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_prova()
            nova_prova = ctrl_prova.inserir_prova()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_inserir == 3:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_trabalho()
            novo_trabalho = ctrl_trabalho.inserir_trabalho()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_inserir == 4:
        continua = 'S'
        while config.continuaProcedimento(continua):
            print(config.MENU_AVALIACAO_ALUNO)
            opcaoIserirAvAluno = int(input("Escolha a opcão[0-2]:"))
            config.clear_console()
            while opcaoIserirAvAluno in range(0,3):
                if opcaoIserirAvAluno == 1:
                    ctrl_avaliacaoAluno.inserir_prova()
                    break
                elif opcaoIserirAvAluno == 2:
                    ctrl_avaliacaoAluno.inserir_trabalho()
                    break
                elif opcaoIserirAvAluno == 0:
                    print(config.MENU_ENTIDADES)
                    opcao_inserir = int(input("Escolha uma opção [0-4]: "))
                    config.clear_console()

                    inserir(opcao_inserir=opcao_inserir)

                    config.clear_console()
                    print(tela_inicial.get_updated_screen())
                    config.clear_console()
                else:
                    opcaoIserirAvAluno = int(input("Valor inválido! Escolha uma opcão[0-2]:"))
                    config.clear_console()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_inserir == 0:
        executaMenu()
                    
def atualizar(opcao_atualizar:int=0):
    if opcao_atualizar == 1:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_aluno()
            aluno_atualizado = ctrl_aluno.atualizar_aluno()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_atualizar == 2:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_prova()
            prova_atualizada = ctrl_prova.atualizar_prova()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_atualizar == 3:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_trabalho()
            trabalho_atualizado = ctrl_trabalho.atualizar_trabalho()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_atualizar == 4:
        continua = 'S'
        while config.continuaProcedimento(continua):
            print(config.MENU_AVALIACAO_ALUNO)
            opcaoIserirAvAluno = int(input("Escolha a opcão[0-2]:"))
            config.clear_console()
            while opcaoIserirAvAluno in range(0,3):
                if opcaoIserirAvAluno == 1:
                    ctrl_avaliacaoAluno.alterar_prova()
                    break
                elif opcaoIserirAvAluno == 2:
                    ctrl_avaliacaoAluno.alterar_trabalho()
                    break
                elif opcaoIserirAvAluno == 0:
                    print(config.MENU_ENTIDADES)
                    opcao_atualizar = int(input("Escolha uma opção [0-4]: "))
                    config.clear_console()

                    atualizar(opcao_atualizar=opcao_atualizar)

                    config.clear_console()
                else:
                    opcaoIserirAvAluno = int(input("Valor inválido! Escolha uma opcão[0-2]:"))
                    config.clear_console()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_atualizar == 0:
        executaMenu()

def excluir(opcao_excluir:int=0):
    if opcao_excluir == 1:
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_aluno()
            aluno_excluido = ctrl_aluno.excluir_Aluno()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_excluir == 2:                
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_prova()
            prova_excluido = ctrl_prova.excluir_prova()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_excluir == 3:                
        continua = 'S'
        while config.continuaProcedimento(continua):
            relatorio.get_relatorio_trabalho()
            trabalho_excluido = ctrl_trabalho.excluir_trabalho()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_excluir == 4:  
        continua = 'S'
        while config.continuaProcedimento(continua):             
            print(config.MENU_AVALIACAO_ALUNO)
            opcaoIserirAvAluno = int(input("Escolha a opcão[0-2]:"))
            config.clear_console()
            while opcaoIserirAvAluno in range(0,3):
                if opcaoIserirAvAluno == 1:
                    ctrl_avaliacaoAluno.excluir_prova()
                    break
                elif opcaoIserirAvAluno == 2:
                    ctrl_avaliacaoAluno.excluir_trabalho()
                    break
                elif opcaoIserirAvAluno == 0:
                    print(config.MENU_ENTIDADES)
                    opcao_excluir = int(input("Escolha uma opção [0-4]: "))
                    config.clear_console()

                    excluir(opcao_excluir=opcao_excluir)

                    config.clear_console()
                    print(tela_inicial.get_updated_screen())
                    config.clear_console()
                else:
                    opcaoIserirAvAluno = int(input("Valor inválido! Escolha uma opcão[0-2]:"))
                    config.clear_console()
            continua = input("Deseja continuar? (S = Sim / N = Não)").upper()
    elif opcao_excluir == 0:
        executaMenu()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()
    executaMenu()

def executaMenu():
   while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [0-4]: "))
        config.clear_console()

        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-4]: "))
            config.clear_console()

            reports(opcao_relatorio)

            config.clear_console()

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [0-4]: "))
            config.clear_console()

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [0-4]: "))
            config.clear_console()

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4: # Excluir Registros

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [0-4]: "))
            config.clear_console()

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 0: # Sair

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else: # Opção Inválida
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()