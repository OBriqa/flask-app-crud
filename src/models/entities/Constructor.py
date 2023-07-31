class Constructor():
    
    def __init__(self, nomC, seu) -> None:
        self.nomC = nomC
        self.seu = seu
    
    def to_JSON(self):
        return {
            'nomC'  : self.nomC,
            'seu'   : self.seu
        }

    def get_atributtes():
        return ('nomC', 'seu')
    
    def get_headings():
        return ('Nom', 'Seu')
    
    def get_id():
        return ('nomC')