from pymongo.mongo_client import MongoClient
import os, time
from datetime import datetime

# Send a ping to confirm a successful connection
try:
    uri = "mongodb+srv://murilo8jogos:marangoni30@biblioteca.gg32n.mongodb.net/?retryWrites=true&w=majority&appName=biblioteca"
    client = MongoClient(uri)

    # Acessando o banco de dados e as coleções
    db = client["Biblioteca"] 
    livros = db["Livros"] 
    user = db["Usuarios"]
    emprestimos = db["Emprestimos"]
    devolucao = db["Devolucao"]  # Evite acentos nos nomes das coleções

    # Confirmar se a conexão foi bem-sucedida
    print("Conexão bem-sucedida com o banco de dados!")

except Exception as e:
    print(f"Erro ao acessar o banco de dados: {e}")
    exit()


def Criar():

    print("\t**CRIAÇÃO DE LIVROS/USÚARIOS**\n")
    print("1. Criar Livro\n2. Criar Usúario\n3. Atualização Livro\n4. Atualizar Usúario\n5. Deletar Livro\n6. Deletar Usúario\n7. Menu")
    try:
        o = int(input(">>>"))
    except ValueError:
        print("Por favor insira um valor valido (1 ou 2).")
        time.sleep(1.5)
        os.system("cls")
        return Criar()

    if (o == 1):
        livro = []
        doc = ["Titulo", "Autor", "Gênero", "Ano de publicação", "ISBN", "Quantidade de exemplares disponíveis"]
        print("*Digite os dados para criar o livro (Aperte enter a cada dado inserido)*")
        for i in range(len(doc)):
            while True:
                dados = input(f"{doc[i]}: ").strip()
                if not dados:
                    print(f"Erro: O campo {doc[i]} não pode ser vazio. Por favor, insira um valor.")
                else:
                    livro.append(dados)
                    break

        documento = {
            "Titulo": livro[0], 
            "Autor": livro[1], 
            "Gênero": livro[2], 
            "Ano de publicação": livro[3], 
            "ISBN": livro[4], 
            "Quantidade de exemplares disponíveis": int(livro[5])
            }

        livro_existente = livros.find_one({"$or": [{"Titulo": livro[0]}, {"ISBN": livro[4]}]})
        if livro_existente:
            print("Erro: Já existe um livro com o mesmo título ou ISBN no banco de dados.")
            print("**Retornando ao menu**")
            time.sleep(2)
            return main()

        livros.insert_one(documento)
        print("\nLivro criado na database com sucesso\n")
        print("-----------------------------------------")

        x = livros.find_one({"Titulo": livro[0]}, {'_id':0})
        if x:
            for chave, valor in x.items():
                print(f"{chave}: {valor}")

        print("-----------------------------------------")
        print("**Retornando ao menu**")
        time.sleep(2)
        return main()

    if (o == 2):
        usurario = []
        doc = ["Nome", "Email", "Data de nascimento (DD-MM-AAAA)", "Número de documento (CPF ou RG)"]
        print("*Digite os dados para criar o usúario (Aperte enter a cada dado inserido)*")
        for i in range(len(doc)):
            while True:
                dados = input(f"{doc[i]}: ").strip()
                if not dados:
                    print(f"Erro: O campo {doc[i]} não pode ser vazio. Por favor, insira um valor.")
                if (i == 2):
                    try:
                        data_formatada = datetime.strptime(dados, "%d-%m-%Y")
                        usurario.append(data_formatada)
                        break
                    except ValueError:
                        print("Erro: Data de nascimento inválida. Por favor, use o formato DD-MM-AAAA.")
                elif not dados:
                    print(f"Erro: O campo {doc[i]} não pode ser vazio. Por favor, insira um valor.")
                else:
                    usurario.append(dados)
                    break

        documento = {
            "Nome": usurario[0], 
            "Email": usurario[1], 
            "Data de Nascimento": usurario[2], 
            "Documento": usurario[3],
            }

        usuario_existente = user.find_one({"Documento": usurario[3]})
        if usuario_existente:
            print("Erro: Já existe um usuário com esse número de documento.")
            print("**Retornando ao menu**")
            time.sleep(2)
            return main()

        user.insert_one(documento)
        print("\nUsúario criado na database com sucesso\n")
        print("-----------------------------------------")

        x = user.find_one({"Nome": usurario[0]}, {'_id':0})
        if x:
            for chave, valor in x.items():
                print(f"{chave}: {valor}")

        print("-----------------------------------------")
        print("**Retornando ao menu**")
        time.sleep(2)
        return main()
    
    if (o == 3):
        print("**Atualizar Livro**")
        print("Qual livro o usuário quer atualizar (Pode ser Título ou o código ISBN)")
        livroemprestar = input(">>>").strip().lower()
        x = livros.find_one({
            "$or": [{"Titulo": {"$regex": f'^{livroemprestar}$', "$options": "i"}},{"ISBN": livroemprestar}]})
        if x:
            doc = ["Titulo", "Autor", "Gênero", "Ano de publicação", "ISBN", "Quantidade de exemplares disponíveis"]
            print(doc)
            o = input(f"Qual informação você quer atualizar no livro '{x['Titulo']}' (Caso queira atualizar tudo digite 'Todas'): ").strip().lower()

            if o == "todas":
                livro = []
                for i in range(len(doc)):
                    while True:
                        dados = input(f"{doc[i]}: ").strip()
                        if not dados:
                            print(f"Erro: O campo {doc[i]} não pode ser vazio. Por favor, insira um valor.")
                        else:
                            livro.append(dados)
                            break
                documento = {
                    "Titulo": livro[0],
                    "Autor": livro[1],
                    "Gênero": livro[2],
                    "Ano de publicação": livro[3],
                    "ISBN": livro[4],
                    "Quantidade de exemplares disponíveis": int(livro[5])
                }
                livro_existente = livros.find_one({"$or": [{"Titulo": livro[0]}, {"ISBN": livro[4]}]})
                if livro_existente:
                    print("Erro: Já existe um livro com o mesmo título ou ISBN no banco de dados.")
                    print("**Retornando ao menu**")
                    time.sleep(2)
                    return main()
                
                livros.update_one({"_id": x["_id"]}, {"$set": documento})
                print("Livro atualizado com sucesso!")

            elif o in [campo.lower() for campo in doc]:
                while True:
                    a = input(f"{o.capitalize()}: ").strip()
                    if not a:
                        print(f"Erro: O campo {o} não pode ser vazio. Por favor, insira um valor.")
                    else:
                        
                        livros.update_one({"_id": x["_id"]}, {"$set": {o.capitalize(): a}})
                        print(f"{o.capitalize()} atualizado com sucesso")
                        break
        else:
            print("Livro não encontrado.")
            print("Voltando para tela de Criação")
            time.sleep(1.5)
            return Criar()
        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
    
    if (o == 4):
        print("**Atualizar Usúario**")
        print("Qual Usúario deseja atualizar (Pode ser Nome ou o Documento)")
        usario = input(">>>").strip().lower()
        x = user.find_one({
            "$or": [{"Nome": {"$regex": f'^{usario}$', "$options": "i"}}, {"Documento": usario}]
        })

        if x:
            doc = ["Nome", "Email", "Data de Nascimento", "Documento"]
            print(doc)
            o = input(f"Qual informação você quer atualizar no usúario '{x['Nome']}' (Caso queira atualizar tudo digite 'Todas'): ").strip().lower()

            usuario_dados = []

            if o == "todas":
                for i in range(len(doc)):
                    while True:
                        dados = input(f"{doc[i]}: ").strip()
                        if not dados:
                            print(f"Erro: O campo {doc[i]} não pode ser vazio. Por favor, insira um valor.")
                        else:
                            usuario_dados.append(dados)
                            break
            
                documento = {
                    "Nome": usuario_dados[0],
                    "Email": usuario_dados[1],
                    "Data de Nascimento": usuario_dados[2],
                    "Documento": usuario_dados[3],
                }

                usuario_existente = user.find_one({"Documento": usuario_dados[3]})
                if usuario_existente and usuario_existente["_id"] != x["_id"]:
                    print("Erro: Já existe um usúario com este documento.")
                    print("**Retornando ao menu**")
                    time.sleep(2)
                    return main()

                user.update_one({"_id": x["_id"]}, {"$set": documento})
                print("Usúario atualizado com sucesso!")

                emprestimos.update_many({"Usúario": x["Nome"]}, {"$set": {"Usúario": usuario_dados[0]}})
                emprestimos.update_many({"Documento": x["Documento"]}, {"$set": {"Documento": usuario_dados[3]}})
                print("Atualizado também a tabela 'Emprestimos' com o nome e documento novos.")

            elif o in [campo.lower() for campo in doc]:
                while True:
                    a = input(f"{o.capitalize()}: ").strip().lower()
                    if not a:
                        print(f"Erro: O campo {o} não pode ser vazio. Por favor, insira um valor.")
                    else:
                        user.update_one({"_id": x["_id"]}, {"$set": {o.capitalize(): a}})
                        print(f"{o.capitalize()} atualizado com sucesso")

                        if o == "nome":
                            emprestimos.update_many({"Usúario": x["Nome"]}, {"$set": {"Usúario": a}})
                            print("Atualizado também a tabela 'Emprestimos' com o novo nome.")

                        if o == "documento":
                            emprestimos.update_many({"Documento": x["Documento"]}, {"$set": {"Documento": a}})
                            print("Atualizado também a tabela 'Emprestimos' com o novo documento.")
                    break
            else:
                print("Usúario não encontrado.")
                print("Voltando para tela de Criação")
                time.sleep(1.5)
                return Criar()
            v = input("Aperte ENTER para voltar para o menu ")
            if v or not v:
                print("Voltando para o menu...")
                time.sleep(1.5)
                return main()
    
    if (o == 5):
        print("**Deletar Livro**")
        print("Digite o titulo do livro ou ISBN que queria deletar")
        x = input(">>>")
        livro_existente = livros.find_one({"$or": [{"Titulo": x}, {"ISBN": x}]})
        nome_livro = (livro_existente["Titulo"])
        if livro_existente:
            print("DESEJA REALMENTE DELETAR ESTE LIVRO, ESTA AÇÃO NÃO PODERA SER REVERTIDA")
            print("Sim | Não")
            a = input(">>>").strip()

            if (a.capitalize() == "Sim"):
                livros.delete_one({'Titulo': nome_livro})
                print(nome_livro, "Foi deletado do sistema")
    
            elif (a.capitalize() == "Não"):
                print("Deletamento foi cancelado")

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
    
    if (o == 6):
        print("**Deletar usúario**")
        print("Digite o nome do usúario ou o documento que queria deletar")
        x = input(">>>")
        user_existente = user.find_one({"$or": [{"Nome": x}, {"Documento": x}]})
        nome_User = (user_existente["Nome"])
        if user_existente:
            print("DESEJA REALMENTE DELETAR ESTE USÚARIO, ESTA AÇÃO NÃO PODERA SER REVERTIDA")
            print("Sim | Não")
            a = input(">>>").strip()

            if (a.capitalize() == "Sim"):
                user.delete_one({'Nome': nome_User})
                print(nome_User, "Foi deletado do sistema")
    
            elif (a.capitalize() == "Não"):
                print("Deletamento foi cancelado")

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
    
    if (o == 7):
        return main() 


def Emprestimos():
    print("**EMPRESTIMOS**")
    print("1. Registrar um emprestimo\n2. Livros para emprestimo\n3. Consultar Emprestimos abertos\n4. Consultar Emprestimos vencidos\n5. Voltar Menu")
    try:
        o = int(input(">>>"))
    except ValueError:
        print("Por favor insira um valor valido (1 a 3).")
        time.sleep(1.5)
        os.system("cls")
        return Emprestimos()

    if (o == 1):
        os.system("cls")
        for l in livros.find({}, {'_id':0}):
            print(l)
        print("Qual livro o usúario quer emprestar (Pode ser Titulo ou o codigo ISBN)")
        livroemprestar = input(">>>").strip().lower()
        x = livros.find_one({"$or": [{"Titulo": {"$regex": f'^{livroemprestar}$', "$options": "i"}}, {"ISBN": livroemprestar}]})
        if x:
            qntd_disponivel = x["Quantidade de exemplares disponíveis"]

            if (qntd_disponivel > 0):
                print(f"O livro '{x['Titulo']}' está disponivel para empréstimo\n")
                print(f"Quantidade de exemplares disponiveis {qntd_disponivel}\n")
                print("Qual usúario quer emprestar este livro (Pode ser Nome ou CPF)")
                usuarioemprestimo = input(">>>").strip().lower()
                y = user.find_one({"$or": [{"Nome": {"$regex": f'^{usuarioemprestimo}$', "$options": "i"}}, {"Documento": usuarioemprestimo}]})
            if y:
                datalista = []
                print("\nQual foi a data de empréstimo e qual será a data de devolução")

                while True:
                    try:
                        dataE = input("Empréstimo (formato: DD-MM-AAAA): ")
                        dataE_formatada = datetime.strptime(dataE, "%d-%m-%Y")
                        break
                    except ValueError:
                        print("Erro: Data de empréstimo inválida. Por favor, use o formato DD-MM-AAAA.")

                while True:
                    try:
                        dataD = input("Devolução (formato: DD-MM-AAAA): ")
                        dataD_formatada = datetime.strptime(dataD, "%d-%m-%Y")
                        break 
                    except ValueError:
                        print("Erro: Data de devolução inválida. Por favor, use o formato DD-MM-AAAA.")

                datalista.append((dataE_formatada, dataD_formatada))
                documento = {
                    "Usúario": y["Nome"],
                    "Documento": y["Documento"],
                    "Livro emprestado": x["Titulo"],
                    "Data emprestimo": dataE_formatada, 
                    "Data devolução": dataD_formatada  
                }

                emprestimos.insert_one(documento)
                print("--------------------------------------------------------------------------------------")
                print(f"Usuário {y['Nome']} do documento {y["Documento"]} emprestou o livro {x['Titulo']} na data {dataE_formatada.strftime('%d-%m-%Y')} e deverá devolver na data {dataD_formatada.strftime('%d-%m-%Y')}")
                livros.update_one({"_id": x["_id"]}, {"$inc": {"Quantidade de exemplares disponíveis": -1}})
                print("--------------------------------------------------------------------------------------")
            
            if not y:
                print("Usuário não existe ou foi digitada alguma informação errada")
                print("Voltando para Empréstimos...")
                time.sleep(1.5)
                os.system("cls")
                return Emprestimos()

            if (qntd_disponivel == 0):
                print("Este livro não tem exemplares.")
                print("Voltando para emprestimos...")
                time.sleep(1.5)
                os.system("cls")
                return Emprestimos()

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
        
    if (o == 2):
        os.system("cls")
        print("**LIVROS DISPONIVEIS PARA EMPRESTIMO**")
        for x in livros.find({"Quantidade de exemplares disponíveis": {"$gt": 1}}, {"_id": 0}):
            print(x)

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()

    if (o == 3):
        os.system("cls")
        print("**CONSULTA DE EMPRESTIMOS EM ABERTO DE UM USÚARIO ESPECIFICO**")
        u = input("Qual o nome ou documento do usúario: ")
        y = user.find_one({"$or": [{"Nome": u}, {"Documento": u}]})
        if y:
            for e in emprestimos.find({"$or": [{"Nome": y["Nome"]}, {"Documento": y["Documento"]}]}):
                data_emprestimo_formatada = e['Data emprestimo'].strftime('%d-%m-%Y')
                data_devolucao_formatada = e['Data devolução'].strftime('%d-%m-%Y')
                print(f"Usuário: {e['Usúario']} | Livro: {e['Livro emprestado']} | Data de Empréstimo: {data_emprestimo_formatada} | Data de Devolução: {data_devolucao_formatada}")
        if not y:
            print("Este usúario não existe.")
            print("Voltando para tela Emprestimos")
            os.system("cls")
            return Emprestimos()


        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
        
    if (o == 4):
        data_atual = datetime.now()
        emprestimos_vencidos = emprestimos.find({"Data devolução": {"$lt": data_atual}})
        print("Usuários com empréstimos vencidos:")
        for emprestimo in emprestimos_vencidos:
            print(f"Usuário: {emprestimo['Usúario']}, Livro: {emprestimo['Livro emprestado']}, Data de Empréstimo: {emprestimo['Data emprestimo'].strftime('%d-%m-%Y')}, Data de Devolução: {emprestimo['Data devolução'].strftime('%d-%m-%Y')}")

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
        
    if (o == 5):
        return main()    


def Relatorios():
    print("**RELATÓRIOS**")
    print("1. Relatório Livros\n2. Relatório usúarios\n3. Relatório emprestimos realizados por data\n4. Voltar Menu")
    try:
        o = int(input(">>>"))
    except ValueError:
        print("Por favor insira um valor valido (1 a 3).")
        time.sleep(1.5)
        os.system("cls")
        return Relatorios()

    if (o == 1):
        os.system("cls")
        for x in livros.find({}, {'_id':0}):
            print(x)
        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
            
    if (o == 2):      
        os.system("cls")
        for x in user.find({}, {'_id':0}):
            print((f"Usuário: {x['Nome']}, Email: {x['Email']}, Data de Nascimento: {x['Data de Nascimento'].strftime('%d-%m-%Y')}, Documento: {x['Documento']}"))
        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()
        
    if (o == 3):
        os.system("cls")
        print("Quais é o intervalo de datas que deseja vêr")
        while True:
            try:
                dataP = input("Primeiro intervalo (formato: DD-MM-AAAA): ")
                dataP_formatada = datetime.strptime(dataP, "%d-%m-%Y")
                break
            except ValueError:
                print("Erro: Data inválida. Por favor, use o formato DD-MM-AAAA.")

        while True:
            try:
                dataF = input("Ultimo intervalo (formato: DD-MM-AAAA): ")
                dataF_formatada = datetime.strptime(dataF, "%d-%m-%Y")
                break 
            except ValueError:
                print("Erro: Data inválida. Por favor, use o formato DD-MM-AAAA.")

        resultados = emprestimos.find({"Data emprestimo": { "$gte": dataP_formatada, "$lte": dataF_formatada }}, {"_id":0})
        print(f"Empréstimos entre {dataP_formatada.strftime('%d-%m-%Y')} e {dataF_formatada.strftime('%d-%m-%Y')}:")
        for emprestimo in resultados:
            data_emprestimo_formatada = emprestimo['Data emprestimo'].strftime('%d-%m-%Y')
            data_devolucao_formatada = emprestimo['Data devolução'].strftime('%d-%m-%Y')
            print(f"Usuário: {emprestimo['Usúario']} | Livro: {emprestimo['Livro emprestado']} | Data de Empréstimo: {data_emprestimo_formatada} | Data de Devolução: {data_devolucao_formatada}")

        v = input("Aperte ENTER para voltar para o menu ")
        if v or not v:
            print("Voltando para o menu...")
            time.sleep(1.5)
            return main()

    if (o == 4):
        return main()


def main():
    os.system("cls")
    print("\t\t--Cadastro e Emprestimos--\n")
    print(f"\tLivros existentes:{livros.count_documents({})}\t Usúarios existentes:{user.count_documents({})}\n")
    print("Escolha uma opção")
    print("1. Cadastros e Atualizações\n2. Emprestimos\n3. Relatórios\n4. Sair")
    opc = int(input(">>>"))
    if (opc == 1):
        os.system('cls')
        Criar()
    if (opc == 2):
        os.system('cls')
        Emprestimos()
    if (opc == 3):
        os.system('cls')
        Relatorios()
    if (opc == 4):
        exit()


if __name__ == "__main__":
    main()