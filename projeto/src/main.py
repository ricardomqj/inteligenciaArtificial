from Menus import MenuPrincipal
from Sistema import Sistema

def main():
    sistema = Sistema()
    sistema.grafo.load_json('mapa.json')
    #sistema.grafo.desenha()

    MenuPrincipal(sistema)

if __name__ == "__main__":
    main()
