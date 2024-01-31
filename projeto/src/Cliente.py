class Cliente:
    def __init__(self, nome, estafetasPorAvaliar={}):
        self.nome = nome
        self.estafetasPorAvaliar = estafetasPorAvaliar

    def adicionaEstafetaParaAva(self, nome, id_encomenda):
        self.estafetasPorAvaliar[id_encomenda] = nome

    def removeEstafetaParaAva(self, id_encomenda):
        if id_encomenda in self.estafetasPorAvaliar:
            del self.estafetasPorAvaliar[id_encomenda]
