
import glob
import json
import shutil
import time

class Queuer:
    """
    Classe qui créer un dictionnaire de queue ou la clef est la priorité d'extraction"""
    def __init__(self) -> None:
        self.queuer = {}
    

    def create_queue_list(self, ndim: int=5) -> dict:
        """créer un dictionnaire d'indice
        """
        ndim += 1
        for i in range(ndim):
            self.queuer[i] = []


    def insert(self, element:dict) -> None:
        """ insert un element à la place de la queue"""
        if element["indice"] <= len(self.queuer):
            self.queuer[element["indice"]].append(element["message"])
        else:
            self.queuer[-1].append(element["message"])


    def extract(self) -> list:
        """ extrait les elements"""
        value: list = self.queuer[0]
        self.reafector()
        return value


    def reafector(self) -> None:
        """ reaffecte les indices n-1"""
        ndim = len(self.queuer) - 1
        new_queuer = {}
        for i in range(ndim):
            new_queuer[i] = self.queuer[i + 1]
        new_queuer[ndim] = []
        self.queuer = new_queuer
    

    def get_path(self) -> list:
        """ crée la list des messages reçu"""
        path = "/home/manu/proga/queue/new_messages/*.json"
        folders = []
        for message in glob.glob(path):
            folders.append(message)
        return folders
    

    def move_message(self) -> None:
        """deplace les messages lu"""
        path = "/home/manu/proga/queue/read_messages"
        folders = self.get_path()
        for folder in folders:
            shutil.move(folder, path)
    
    
    def load_message(self) -> None:
        """récupere le message est l'insert dans la file"""
        folders = self.get_path()
        if folders:
            print("messages reçus")
        for folder in folders:
            with open(folder, "r") as message:
                reception = json.load(message)
                self.insert(reception)
                

    def reception(self) -> list:
        """ recupére les messages dans l'ordre d'importance"""
        result = [self.extract() for _ in range(len(self.queuer))]
        return result


    def interrogation(self, timer=5) -> list:
        """ interroge la liste pendant une durée de temps, puis effectue les taches"""
        i = 0
        while i < 5:
            self.load_message()
            self.move_message()
            time.sleep(timer)
            i += 1
        reception_result = self.reception()
        reception_clean = self.cleaner(reception_result)
        return reception_clean
    

    def cleaner(self, messages:list) -> list:
        """ retire les listes vides"""
        messages_clean = [message for message in messages if message]
        return messages_clean


if __name__ == "__main__":


    print("initialisation du programme")
    messages = Queuer()
    messages.create_queue_list()
    while True:
        reception = messages.interrogation()
        if reception:
            print(reception)
  

    