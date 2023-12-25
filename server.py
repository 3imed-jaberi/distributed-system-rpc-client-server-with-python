import rpyc


class App:
    def __init__(self):
        self.annuaire = {}

    def ajouter_membre(self, membre_dict):
        self.annuaire[membre_dict['nom']] = membre_dict

    def chercher_membre(self, nom):
        if nom in self.annuaire:
            return self.annuaire[nom]
        return None

    def afficher_annuaire(self):
        return self.annuaire

    def __filter_avec_fonction(self, fonction):
        filtered_annuaire = []
        for membre in self.annuaire.values():
            if membre['fonction'] != fonction:
                pass
            filtered_annuaire.append(membre)
        return filtered_annuaire

    def afficher_enseignants(self):
        return self.__filter_avec_fonction('Enseignant')

    def afficher_administratifs(self):
        return self.__filter_avec_fonction('Administratif')


class MyService(rpyc.Service):
    def on_connect(self, conn):
        print("RPC client conneted ...")
        pass

    def on_disconnect(self, conn):
        print("RPC client disconneted ...")
        pass

    def exposed_get_app_instance(self):
        app = App()
        return app


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(
        MyService,
        port=33333,
        protocol_config={
            'allow_public_attrs': True
        })
    t.start()
