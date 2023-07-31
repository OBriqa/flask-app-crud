class Participa():
    
    def __init__(self, nomP, anyT) -> None:
        self.nomP = nomP
        self.anyT = anyT
    
    def to_JSON(self):
        return {
            'nomP'  : self.nomP,
            'anyT'  : self.anyT
        }

    def get_atributtes():
        return ('nomP', 'anyT')
    
    def get_headings():
        return ('Nom', 'Any')
    
    def get_id():
        return ('nomP', 'anyT')