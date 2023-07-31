class Pais():

    def __init__(self, codi, nom) -> None:
        self.codi = codi
        self.nom = nom

    def to_JSON(self):
        return {
            'codi'  : self.codi,
            'nom'   : self.nom
        }

    def get_atributtes():
        return ('codi', 'nom')
    
    def get_headings():
        return ('Codi', 'Nom')
    
    def get_id():
        return ('codi')