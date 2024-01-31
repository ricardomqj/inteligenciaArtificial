import json
import os
from Grafo import Graph
from Encomenda import Encomenda
from Estafeta import Estafeta

from Cliente import Cliente

class Sistema:
    def __init__(self):     
        self.estafetas = {}  
        self.encomendas = {}  
        self.clientes = {}
        self.grafo = Graph()
        self.carregaData()

    def localidadeExiste(self, nome):
        return self.grafo.locationExists(nome)
    
    def novaEncomenda(self, local, peso, volume, tempoPedido, distancia, nome):
        if self.encomendas:
            id = list(self.encomendas.items())[-1][0] + 1
        else:
            id = 0

        enc = Encomenda(id, local, peso, volume, tempoPedido, distancia, nome)
        self.encomendas[id] = enc
        return enc

    def definePreco(self, veiculo, volume, distancia , prazoEntrega):
        match veiculo:
            case "bicicleta":
                if prazoEntrega == 0:
                    return 3 + volume * 0.1 + distancia * 0.02
                else:
                    return 3 + volume * 0.1 + distancia * 0.02 + 2
            case "mota":
                if prazoEntrega == 0:
                    return 3 + volume * 0.1 + distancia * 0.0325
                else:
                    return 3 + volume * 0.1 + distancia * 0.0325 + 2
            case "carro":
                if prazoEntrega == 0:
                    return 3 + volume * 0.1 + distancia * 0.065
                else:
                    return 3 + volume * 0.1 + distancia * 0.065 + 2

    def loginCliente(self, nome):
        if nome in self.clientes:
            return True
        else:
            return False

    def adicionarCliente(self, nome_cliente):
        cliente = Cliente(nome_cliente)
        self.clientes[nome_cliente] = cliente

    def getEstafetasParaAvaliar(self, nome_cliente):
        cliente = self.clientes[nome_cliente]
        lista_estafetas = []

        for id_encomenda, estafeta_nome in cliente.estafetasPorAvaliar.items():
            lista_estafetas.append((id_encomenda, self.estafetas[estafeta_nome]))

        return lista_estafetas

        
    def adicionarEstafeta(self, nome_estafeta, status, veiculo):
        estafeta = Estafeta(nome_estafeta, status, veiculo)
        self.estafetas[nome_estafeta] = estafeta

    def loginEstafeta(self, nome):
        if nome in self.estafetas:
            return True
        else:
            return False
        
    def estafetaMaisEcologico(self, peso, distancia, tempo):
        estafetaEscolhido = None 
        niveisDeCO2Baixos = -1

        for estafeta in self.estafetas.values():
            if not estafeta.verificaAddEncomenda(peso):
                continue

            niveisCO2Estafeta = estafeta.verficaViabilidade(peso, distancia, tempo)

            if niveisCO2Estafeta == -1:
                continue
            
            if niveisDeCO2Baixos == -1:
                estafetaEscolhido = estafeta
                niveisDeCO2Baixos = niveisCO2Estafeta 
            else:
                if niveisCO2Estafeta < niveisDeCO2Baixos:
                    estafetaEscolhido = estafeta
                    niveisDeCO2Baixos = niveisCO2Estafeta

                if niveisCO2Estafeta == niveisDeCO2Baixos:
                    if estafeta.getNumeroEntregas() < estafetaEscolhido.getNumeroEntregas():
                        estafetaEscolhido = estafeta
        
        return estafetaEscolhido

    def respostaPosEncomenda(self, idEnc, nome, caminho):

        enc = self.getEncomenda(idEnc)

        for node in caminho:
            print(str(node))

        tempoEntrega = self.getEstafeta(nome).tempoEncomenda(enc.distancia, enc.peso)
        tempoFormatado = round(tempoEntrega, 2)

        print(f"Encomenda demorou {tempoFormatado} horas a ser entregue.")
        print(f"Encomenda foi entregue de {self.getEstafeta(nome).veiculo}.")
        print(f"A distancia percorrida foi de {enc.distancia}km.")


    def repostaPosPacoteEncomenda(self, nome, caminho, distancia, tempoDemorado):
        print("--- Caminho Efetuado ---")
        for node in caminho:
            print(str(node))
        
        print(f"\nEncomenda demorou {tempoDemorado} horas a ser entregue.")
        print(f"Encomenda foi entregue de {self.getEstafeta(nome).veiculo}.")
        print(f"A distancia percorrida foi de {distancia}km.")

    def removeEncomenda(self, idEnc, nome):

        estafeta = self.getEstafeta(nome)
        encomenda = self.encomendas[idEnc]
        estafeta.encPorEntregar.remove(idEnc)

        del self.encomendas[idEnc]
        estafeta.numEntregas += 1

        cliente = self.clientes[encomenda.cliente]
        cliente.adicionaEstafetaParaAva(nome, idEnc)


    def getEncomenda(self, idEnc):
        return self.encomendas.get(idEnc)

    def getEstafeta(self, nome):
        return self.estafetas.get(nome)

    def espacoLivreEstafeta(self, nome):
        estafeta = self.estafetas.get(nome)
        espacoOcupado = estafeta.somaEncomendas()

        match  estafeta.veiculo:
            case "bicicleta":
                return 5 - espacoOcupado

            case "mota":
                return 20 - espacoOcupado

            case "carro":
                return 100 - espacoOcupado

    def mostrarEncomendasEstafetas(self, nome):
        estafeta = self.estafetas.get(nome)

        listaEnc = estafeta.getEncomendas()
        
        encomendas_string = "" 

        for encomendaId in listaEnc:
            encomenda = self.encomendas.get(encomendaId)
            if encomenda:
                encomendas_string += f"ID: {encomenda.id}, Local de Entrega: {encomenda.localChegada}\n"

        print(encomendas_string)
        return encomendas_string


    def mostraEncomendasAdmin(self):
        encStr = ""
        for enc in self.encomendas.values():
            encStr += f"ID: {enc.id}, Local de Entrega: {enc.localChegada}, Peso: {enc.peso}\n"

        return encStr
    
    def mostrarEstafetasAdmin(self):
        estStr = ""
        for est in self.estafetas.values():
            estStr += f"Nome: {est.nome}, Veiculo: {est.veiculo}, Avaliação: {est.getMedAval()}\n"
        
        return estStr

    def mostrarClientesAdmin(self):
        cliStr = ""
        for cli in self.clientes.values():
            cliStr += f"Nome: {cli.nome}\n"
        
        return cliStr

    def atribuiEncomenda(self, nome, encomenda):
        estafeta = self.estafetas.get(nome)

        encomenda.estado = 1
        estafeta.listaEncomenda.append(encomenda)

    def atribuiAvaliacao(self, estafeta, avaliacao):
        estafeta.somaClassificacoes += int(avaliacao)
        estafeta.status = 0

    def mediaEstafeta(self, estafeta):
        print(estafeta.somaClassificacoes)
        print("/")
        print(len(estafeta.encomenda_ids))
        return estafeta.somaClassificacoes / len(estafeta.encomenda_ids)
    
    def calculaMelhorCaminho(self, local, heuristic, localInicio = "Central"):
        result_BFS = self.grafo.procura_BFS(localInicio, local)
        print(f"BFS: {result_BFS}")
        result_DFS = self.grafo.procura_DFS(localInicio, local)
        print(f"DFS: {result_DFS}")
        result_Greedy = self.grafo.greedy(localInicio, local, heuristic)
        print(f"Greedy: {result_Greedy}")
        result_Astar = self.grafo.procura_aStar(localInicio, local, heuristic)
        print(f"AStar: {result_Astar}")

        results = [result_BFS, result_DFS, result_Greedy, result_Astar]
        valid_results = [result for result in results if result is not None]

        if not valid_results:
            return None

        min_result = min(valid_results, key=lambda x: x[1])
        melhorCaminho, custoMin = min_result

        print("Melhor Caminho:", melhorCaminho)
        print("Custo Mínimo:", custoMin)

        return min_result
    
    def calculaCaminhoInformada(self, local, heuristic, localInicio = "Central"):
        result_Greedy = self.grafo.greedy(localInicio, local, heuristic)
        print(result_Greedy)
        result_Astar = self.grafo.procura_aStar(localInicio, local, heuristic)
        print(result_Astar)

        results = [result_Greedy, result_Astar]
        valid_results = [result for result in results if result is not None]

        if not valid_results:
            return None

        min_result = min(valid_results, key=lambda x: x[1])
        melhorCaminho, custoMin = min_result

        print("Melhor Caminho:", melhorCaminho)
        print("Custo Mínimo:", custoMin)

        return min_result


    def formarPacoteEncomendas(self, nome):
        estafeta = self.estafetas.get(nome)
        listaEncId = estafeta.getEncomendas()
        
        tempoDemorado = 0
        distanciaPercorrida = 0
        
        listaEnc = []

        for idEnc in listaEncId:
            listaEnc.append(self.encomendas[idEnc])
        
        listaEnc = sorted(listaEnc, key=lambda encomenda: (encomenda.tempoPedido == 0, encomenda.tempoPedido))

        encomendasEntregar = [] 
        Pesoqueleva = 0
        acumulador = 0

        for enc in listaEnc: 
            distanciaPercorrida += enc.distancia
            acumulador = Pesoqueleva + enc.peso 
            tempo = estafeta.tempoEncomenda(enc.distancia, enc.peso)
        
            if estafeta.verificaAddEncomenda(acumulador):
                if enc.tempoPedido == 0 or tempo + tempoDemorado <= enc.tempoPedido:
                    encomendasEntregar.append(enc)
                    tempoDemorado += tempo

        resposta = []
        resposta.append(encomendasEntregar)
        resposta.append(distanciaPercorrida)
        resposta.append(tempoDemorado)

        return resposta

    # --- Rankings ---

    def rankingMediaAvaliacao(self, nome_estafeta):
        sorted_estafetas = sorted(self.estafetas.values(), key=lambda estafeta: estafeta.getMedAval(), reverse=True)
        position = next((i+1 for i, estafeta in enumerate(sorted_estafetas) if estafeta.nome == nome_estafeta), None)
        
        print("\n____________________\n")
        for i, estafeta in enumerate(sorted_estafetas[:5]):
            print(f"{i+1}. {estafeta.nome} - Média de avaliação: {estafeta.getMedAval()}")
        
        print("\n____________________\n")
        
        if position is not None:
            print(f"[{nome_estafeta}], encontras-te na posição nº {position}\n")
        else:
            print(f"Estafeta {nome_estafeta} não encontrado no ranking de média de avaliação\n")
            
    # ranking de estafetas com mais entregas no geral
    def rankingNumEntregasGeral(self, nome_estafeta):
        sorted_estafetas = sorted(self.estafetas.values(), key=lambda estafeta: estafeta.numEntregas, reverse=True)
        position = next((i+1 for i, estafeta in enumerate(sorted_estafetas) if estafeta.nome == nome_estafeta), None)
        
        print("\n____________________\n")
        for i, estafeta in enumerate(sorted_estafetas[:5]):
            print(f"{i+1}. {estafeta.nome} - Número de Entregas: {estafeta.numEntregas}")
            
        print("\n____________________\n")
        
        if position is not None:
            print(f"[{nome_estafeta}], encontras-te na posição nº {position}\n")
        else:
            print(f"Estafeta {nome_estafeta} não encontrado no ranking de maior número de entregas\n")
            
    #ranking de numero de entregas de Mota, bicicleta e carro respetivamente
    def rankingNumEntregasMota(self, nome_estafeta):
        sorted_estafetas_mota = sorted([estafeta for estafeta in self.estafetas.values() if estafeta.veiculo == 'mota'],
                                       key=lambda estafeta: estafeta.numEntregas, reverse=True)
        position = next((i + 1 for i, estafeta in enumerate(sorted_estafetas_mota) if estafeta.nome == nome_estafeta), None)
        
        print("\n____________________\n")
        for i, estafeta in enumerate(sorted_estafetas_mota[:5]):
            print(f"{i+1}. {estafeta.nome} - Número de entregas: {estafeta.numEntregas}")
            
        print("\n____________________\n")
        
        if position is not None:
            print(f"[{nome_estafeta}], encontras-te na posição nº {position}\n")
        else:
            print(f"Estafeta {nome_estafeta} não encontrado no ranking de maior número de entregas de mota\n")
        
    def rankingNumEntregasBicicleta(self, nome_estafeta):
        sorted_estafetas_bicicleta = sorted([estafeta for estafeta in self.estafetas.values() if estafeta.veiculo == 'bicicleta'],
                                            key=lambda estafeta: estafeta.numEntregas, reverse=True)
        position = next((i + 1 for i, estafeta in enumerate(sorted_estafetas_bicicleta) if estafeta.nome == nome_estafeta), None)

        print("\n____________________\n")
        for i, estafeta in enumerate(sorted_estafetas_bicicleta[:5]):
            print(f"{i + 1}. {estafeta.nome} - Número de Entregas: {estafeta.numEntregas}")
            
        print("\n____________________\n")
            
        if position is not None:
            print(f"[{nome_estafeta}], encontras-te na posição nº {position}\n")
        else:
            print(f"Estafeta {nome_estafeta} não encontrado no ranking de maior número de entregas de bicicleta\n")


    def rankingNumEntregasCarro(self, nome_estafeta):
        sorted_estafetas_carro = sorted([estafeta for estafeta in self.estafetas.values() if estafeta.veiculo == 'carro'],
                                        key=lambda estafeta: estafeta.numEntregas, reverse=True)
        position = next((i + 1 for i, estafeta in enumerate(sorted_estafetas_carro) if estafeta.nome == nome_estafeta), None)
        
        print("\n____________________\n")
        for i, estafeta in enumerate(sorted_estafetas_carro[:5]):
            print(f"{i + 1}. {estafeta.nome} - Número de Entregas: {estafeta.numEntregas}")
            
        print("\n____________________\n")

        if position is not None:
            print(f"[{nome_estafeta}], encontras-te na posição nº {position}\n")
        else:
            print(f"Estafeta {nome_estafeta} não encontrado no ranking de maior número de entregas de carro\n")


    def guardarData(self):
        map_path = os.path.join('data', 'estafetas.json')
        existing_data = []

        for estafeta in self.estafetas.values():
            new_estafeta_data = {
                "nome": estafeta.nome,
                "status": estafeta.status,
                "veiculo": estafeta.veiculo,
                "listEnc": estafeta.encPorEntregar,
                "numEntregas": estafeta.numEntregas,
                "somaClass": estafeta.somaClassificacoes
            }
            existing_data.append(new_estafeta_data)

        with open(map_path, 'w') as file:
            json.dump(existing_data, file, indent=2)

        encomendas_path = os.path.join('data', 'encomendas.json')
        existing_data = []

        for encomenda in self.encomendas.values():
            new_encomenda_data = {
                "id": encomenda.id,
                "local": encomenda.localChegada,
                "peso": encomenda.peso,
                "volume": encomenda.volume,
                "tempo": encomenda.tempoPedido,
                "dist": encomenda.distancia,
                "nome": encomenda.cliente
            }
            existing_data.append(new_encomenda_data)

        with open(encomendas_path, 'w') as file:
            json.dump(existing_data, file, indent=2)

        clientes_path = os.path.join('data', 'clientes.json')
        existing_data = []

        for cliente in self.clientes.values():
            new_cliente_data = {
                "nome": cliente.nome,
                "listaEstafetasId": cliente.estafetasPorAvaliar,
            }
            existing_data.append(new_cliente_data)

        with open(clientes_path, 'w') as file:
            json.dump(existing_data, file, indent=2)


    def carregaData(self):
        estafetas_path = os.path.join('data', 'estafetas.json')
        encomendas_path = os.path.join('data', 'encomendas.json')
        clientes_path = os.path.join('data', 'clientes.json')

        with open(estafetas_path, 'r') as estafetas_file:
            estafetas_data = json.load(estafetas_file)

            for estafeta_data in estafetas_data:
                estafeta = Estafeta(
                    nome=estafeta_data["nome"],
                    status=estafeta_data["status"],
                    veiculo=estafeta_data["veiculo"],
                    encPorEntregar=estafeta_data["listEnc"],
                    numEntregas=estafeta_data["numEntregas"],
                    somaClassificacoes=estafeta_data["somaClass"]
                )
                self.estafetas[estafeta_data["nome"]] = estafeta

        with open(encomendas_path, 'r') as encomendas_file:
            encomendas_data = json.load(encomendas_file)

            for encomenda_data in encomendas_data:
                encomenda = Encomenda(
                    id=encomenda_data["id"],
                    localChegada=encomenda_data["local"],
                    peso=encomenda_data["peso"],
                    volume=encomenda_data["volume"],
                    tempoPedido=encomenda_data["tempo"],
                    distancia=encomenda_data["dist"],
                    nome=encomenda_data["nome"]
                )
                self.encomendas[encomenda_data["id"]] = encomenda

        with open(clientes_path, 'r') as clientes_file:
            clientes_data = json.load(clientes_file)

            for cliente_data in clientes_data:
                cliente = Cliente(
                    nome=cliente_data["nome"],
                    estafetasPorAvaliar=cliente_data["listaEstafetasId"]
                )
                self.clientes[cliente_data["nome"]] = cliente