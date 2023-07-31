class Temporada():

    def __init__(self, anyT, pilotCampio, constructorCampio) -> None:
        self.anyT = anyT
        self.pilotCampio = pilotCampio
        self.constructorCampio = constructorCampio

    def to_JSON(self):
        return {
            'anyT'              : self.anyT,
            'pilotCampio'       : self.pilotCampio,
            'constructorCampio' : self.constructorCampio
        }
    
    def get_atributtes():
        return ('anyT', 'pilotCampio', 'constructorCampio')
    
    def get_headings():
        return ('Any', 'Pilot Campió', 'Constructor Campió')
    
    def get_id():
        return ('anyT')