class Estafeta:
    def __init__(self, nome, status, veiculo, encPorEntregar = [], numEntregas = 0, somaClassificacoes = 0):
        self.nome = nome
        self.status = status
        self.veiculo = veiculo
        self.encPorEntregar = encPorEntregar
        self.numEntregas = numEntregas
        self.somaClassificacoes = somaClassificacoes

    def getEncomendas(self):
        return self.encPorEntregar

    def getNumeroEntregas(self):
        return len(self.encPorEntregar) 
    
    def getMedAval(self):
        if (self.numEntregas == 0):
            return 0
        else:
            return round(self.somaClassificacoes/self.numEntregas, 2)

    def adicionaEnc(self, idEnc):
        self.encPorEntregar.append(idEnc)
    
    def tempoBicla(self, distancia, peso):
        return distancia / (10 - 0.6 * peso)

    def tempoMota(self, distancia, peso):
        return distancia / (35 - 0.5 * peso)

    def tempoCarro(self, distancia, peso):
        return distancia / (50 - 0.1 * peso)
    
    def tempoEncomenda(self, distancia, peso):
        match self.veiculo:
            case "bicicleta":
                return self.tempoBicla(distancia, peso)
            case "mota":
                return self.tempoMota(distancia, peso)
            case "carro":
                return self.tempoCarro(distancia, peso)
    
    def verficaViabilidade(self, peso, distancia, tempo):
        match self.veiculo:
            case "bicicleta":  
                if tempo != 0 and self.tempoBicla(distancia, peso) > tempo:
                    return -1

                return 0
            case "mota": 
                if tempo != 0 and self.tempoBicla(distancia, peso) > tempo:
                    return -1
                
                return 70 * distancia  
            case "carro": 
                if tempo != 0 and self.tempoCarro(distancia, peso) > tempo:
                    return -1

                return 180 * distancia


    def verificaAddEncomenda(self, peso):
        match self.veiculo:
            case "bicicleta":
                if peso <= 5:
                    return True
                else:
                    return False
            case "mota":
                if peso <= 20:
                    return True
                else:
                    return False
            case "carro":
                if peso <= 100:
                    return True
                else:
                    return False
