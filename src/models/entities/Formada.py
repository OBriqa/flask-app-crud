class Formada():
    
    def __init__(self, anyT, nomGP) -> None:
        self.anyT = anyT
        self.nomGP = nomGP
    
    def to_JSON(self):
        return {
            'anyT'  : self.anyT,
            'nomGP' : self.nomGP
        }

    def get_atributtes():
        return ('anyT', 'nomGP')
    
    def get_headings():
        return ('Any', 'Gran Premi')
    
    def get_id():
        return ('anyT', 'nomGP')