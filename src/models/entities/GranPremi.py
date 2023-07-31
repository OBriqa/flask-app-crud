class GranPremi():

    def __init__(self, nomGP, circuit, situat) -> None:
        self.nomGP = nomGP
        self.circuit = circuit
        self.situat = situat

    def to_JSON(self):
        return {
            'nomGP'     : self.nomGP,
            'circuit'   : self.circuit,
            'situat'    : self.situat
        }

    def get_atributtes():
        return ('nomGP', 'circuit', 'situat')
    
    def get_headings():
        return ('Gran Premi', 'Tipus de Circuit', 'Pais')
    
    def get_id():
        return ('nomGP')