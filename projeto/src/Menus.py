def MenuPrincipal(sistema):
    while True:
        print("\n--- Menu Principal ---\n")
        print("1 - Interface Cliente")
        print("2 - Interface Estafeta")
        print("3 - Interface Admnistrador")
        print("4 - Guardar estado")
        print("0 - Sair")

        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 0:
                print("... A sair ...")
                break

            case 1:
                menuClienteLogin(sistema)
                break

            case 2:
                menuEstafetaLogin(sistema)
                break

            case 3:
                menuAdmin(sistema)
                break

            case 4:
                sistema.guardarData()
                break

            case _:
                print("Opção inválida")


def menuClienteLogin(sistema):
    while True:
        print("\n--- Menu Login Cliente ---\n")
        print("1 - Login")
        print("2 - Registar Cliente")
        print("0 - Voltar")

        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 0:
                MenuPrincipal(sistema)
                break

            case 1:
                nome_cliente = input("Introduza o nome do cliente - ")
                if sistema.loginCliente(nome_cliente):
                    menuCliente(sistema, nome_cliente)
                    break
                else:
                    print("Cliente não registado")

            case 2:  
                nome_cliente = input("Introduza o seu nome: ")

                sistema.adicionarCliente(nome_cliente)
                print("Registro completo")

                menuClienteLogin(sistema)
                break
            case _:
                print("Opção inválida")

def menuCliente(sistema, nome):
    while True:
        print("\n--- Menu Cliente ---\n")
        print("1 - Fazer encomenda")
        print("2 - Avaliar Estafetas que fizeram entrega")
        print("0 - Voltar")

        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 0:
                menuClienteLogin(sistema)
                break

            case 1:  
                menuClienteFazerEncomenda(sistema, nome)
                break

            case 2:  
                menuAvaliarEstafetas(sistema, nome)
                break

            case _:
                print("Opção inválida")


def menuAvaliarEstafetas(sistema, nome):
    estafetas = sistema.getEstafetasParaAvaliar(nome)
    i = 1

    print("\n--- Estafetas para Avaliar ---\n")
    if(len(estafetas) == 0):
        print("Não há estafetas para avaliar!")
    else:
        for estafeta in estafetas:
            print(f"{i} -> {estafeta[1].nome} da encomenda de id {estafeta[0]}")
            i += 1
    print("\n0 - Voltar")
    opcao = int(input("\nIntroduza a sua opcao - "))

    if opcao == 0:
        menuCliente(sistema, nome)
    elif 1 <= opcao <= i:
        aval = int(input("\nAvalie de 0 a 5 - "))
        cliente = sistema.clientes[nome]
        cliente.removeEstafetaParaAva(estafetas[opcao-1][0])
        sistema.atribuiAvaliacao(estafetas[opcao-1][1], aval)

        menuAvaliarEstafetas(sistema, nome)
    else:
        print("Opção inválida")


def menuClienteFazerEncomenda(sistema, nome):
    print("\n--- Menu Fazer Encomenda ---")

    while (peso := float(input("\nPeso da Encomenda: "))) > 100 or peso <= 0:
        print("Peso não suportado.")

    while (volume := float(input("\nVolume da Encomenda: "))) <= 0:
        print("Volume inválido.")

    while (tempoPedido := float(input("\nTempo em que quer receber a Encomenda (0 se não tiver preferência): "))) < 0:
        print("Tempo inválido.")

    while not sistema.localidadeExiste(local := input("\nLocal onde deseja receber a Encomenda: ")):
        print(f"O local '{local}' não existe.")

    distancia = sistema.calculaMelhorCaminho(local, "bestpath")[1]

    estafeta = sistema.estafetaMaisEcologico(peso, distancia, tempoPedido)

    if estafeta == None:
        print("Prazo de entrega é muito curto para a localidade que escolheu")
        menuCliente(sistema, nome)

    precoenc = sistema.definePreco(estafeta.veiculo, volume, distancia, tempoPedido)
    precoformatado = round(precoenc, 2)

    if (input(f"O preço da encomenda é {precoformatado}. Deseja aceitar? (S ou N): ").lower() == "s"):
        enc = sistema.novaEncomenda(local, peso, volume, tempoPedido, distancia, nome)
        estafeta.adicionaEnc(enc.id)
        menuCliente(sistema, nome)
    else:
        menuCliente(sistema, nome)

def menuEstafetaLogin(sistema):
    while True:
        print("\n--- Menu Login Estafeta ---\n")
        print("1 - Login")
        print("2 - Registar novo estafeta")
        print("0 - Voltar")

        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 1:
                nome_estafeta = input("\nIntroduza o nome do estafeta - ")
                if sistema.loginEstafeta(nome_estafeta):
                    menuEstafeta(sistema, nome_estafeta)
                else:
                    print("Estafeta não registado")

            case 2:
                nome_estafeta = input("Introduza o seu nome: ")

                while not (veiculo := input("Qual é o seu veiculo (bicicleta/mota/carro): ").lower()) in ["bicicleta","mota","carro"]:
                    print("Veiculo inválido.")
                sistema.adicionarEstafeta(nome_estafeta, 0, veiculo)
                print("Registro completo")

            case 0:
                MenuPrincipal(sistema)
                break

            case _:
                print("Opção inválida")
                
def menuEstafeta(sistema, nome):
    while True:
        print("\n--- Menu Estafeta ---\n")
        print("1 - Verificar encomendas disponíveis")
        print("2 - Rankings")
        print("0 - Voltar")

        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 1:
                menuEncomendasEstafeta(sistema, nome)
                break
            case 2:
                menuRankings(sistema, nome)
                break
            case 0:
                menuEstafetaLogin(sistema)
                break

def extractIdsLocalsString(encomendasString):
    idsLocalsString = {}
    
    indexIds = [index for index, palavra in enumerate(encomendasString.split()) if palavra == "ID:"]

    for indexId in indexIds:
        encIdString = encomendasString.split()[indexId + 1].replace(',', '')
        encId = int(encIdString)
        local_index = encomendasString.find("Local de Entrega:", indexId)
        local = encomendasString[local_index:].split(": ")[1].split("\n")[0]
        idsLocalsString[encId] = local

    return idsLocalsString


def sistemaAtribuiPacote(sistema, nome):
    while not (heur := input("Insere a heurística (melhor caminho/menor transito/estrada com melhor qualidade): ").lower()) in ["melhor caminho","menor transito","estrada com melhor qualidade"]:
        print("Heurística inválida.")

        match heur:
            case "melhor caminho":
                break
            case "menor transito":
                break
            case "estrada com melhor qualidade":
                break

    localInicio = "Central"
    
    caminho = []
    
    resposta = sistema.formarPacoteEncomendas(nome)

    if len(resposta[0]) == 0:
        print("Não foi possível formar um pacote de encomendas!")

    for encomenda in resposta[0]:
        match heur:
            case "melhor caminho":
                (caminho,custo) = sistema.calculaCaminhoInformada(encomenda.localChegada, "bestpath", localInicio)
            case "menor transito":
                (caminho,custo) = sistema.calculaCaminhoInformada(encomenda.localChegada, "transit", localInicio)
            case "estrada com melhor qualidade":
                (caminho,custo) = sistema.calculaCaminhoInformada(encomenda.localChegada, "roadquality", localInicio)

        localInicio = encomenda.localChegada
        caminho.append(caminho)
        sistema.removeEncomenda(encomenda.id, nome)
        
    sistema.repostaPosPacoteEncomenda(nome, caminho, resposta[1], resposta[2])


def menuEncomendasEstafeta(sistema, nome):
    print("\n--- Encomendas para Entrega diponíveis ---\n")
    encomendasString = sistema.mostrarEncomendasEstafetas(nome)

    idsLocalsString = extractIdsLocalsString(encomendasString)

    print("\n1 - Escolher uma Encomenda")
    print("2 - Fazer o Sistema atribuir pacote de encomendas")
    print("0 - Voltar")

    userInput1 = int(input("\nIntroduza a sua opcao - "))

    match userInput1:
        case 1:
            
            userInput2 = None

            while(userInput2 not in idsLocalsString):
                userInput2 = int(input("\nIntroduza o ID da Encomenda - "))
                
            if userInput2 in idsLocalsString:
                local = idsLocalsString[userInput2]

                while not (heur := input("Insere a heurtistica (melhor caminho/menor transito/estrada com melhor qualidade): ").lower()) in ["melhor caminho","menor transito","estrada com melhor qualidade"]:
                    print("Heurtistica inválida.")

                match heur:
                    case "melhor caminho":
                        (caminho, custo) = sistema.calculaCaminhoInformada(local, "bestpath")
                    case "menor transito":
                        (caminho, custo) = sistema.calculaCaminhoInformada(local, "transit")
                    case "estrada com melhor qualidade":
                        (caminho, custo) = sistema.calculaCaminhoInformada(local, "roadquality")
                
                sistema.respostaPosEncomenda(userInput2, nome, caminho)

                sistema.removeEncomenda(userInput2, nome)

                menuEstafeta(sistema, nome)
            else:
                print("\nID da encomenda não válido. Tente novamente.")
                
        case 2:
            sistemaAtribuiPacote(sistema, nome)
            
        case 0:
            menuEstafetaLogin(sistema)

    
def menuRankings(sistema, nome):
    print("\n1 - Top 5 ranking estafetas com melhor avaliação média") 
    print("2 - Top 5 ranking de estafetas com mais entregas feitas")
    print("3 - Top 5 ranking de estafetas com mais entregas de carro feitas")
    print("4 - Top 5 ranking de estafetas com mais entregas de mota feitas")
    print("5 - Top 5 ranking de estafetas com mais entregas de bicicleta feitas")
    print("\n0 - Voltar")

    user_input = int(input("\nIntroduza a sua opcao - "))
    match user_input:
        case 1:
            sistema.rankingMediaAvaliacao(nome)
            menuRankings(sistema, nome)
        case 2:
            sistema.rankingNumEntregasGeral(nome)
            menuRankings(sistema, nome)
        case 3:
            sistema.rankingNumEntregasCarro(nome)
            menuRankings(sistema, nome)
        case 4:
            sistema.rankingNumEntregasMota(nome)
            menuRankings(sistema, nome)
        case 5:
            sistema.rankingNumEntregasBicicleta(nome)
            menuRankings(sistema, nome)           
        case 0:
            menuEstafeta(sistema, nome)
            
def menuAdmin(sistema):
    while True: 
        print("\n--- Menu Administrador ---\n")
        print("1 - Mostrar Encomendas")
        print("2 - Mostrar Estafetas")
        print("3 - Mostrar Clientes")
        print("0 - Voltar")
        
        try:
            opcao = int(input("\nIntroduza a sua opção - "))
        except ValueError:
            opcao = -1

        match opcao:
            case 0:
                MenuPrincipal(sistema)
                break

            case 1:
                print(f"\n--- Entregas ---\n{sistema.mostraEncomendasAdmin()}")

            case 2:
                print(f"\n--- Estafetas ---\n{sistema.mostrarEstafetasAdmin()}")

            case 3:
                print(f"\n--- Clientes ---\n{sistema.mostrarClientesAdmin()}")

            case _:
                print("Opção inválida")
