from utils.Format import Format, datetime

class Pilot():

    def __init__(self, nomP, dataN, nacionalitat) -> None:
        self.nomP = nomP
        self.dataN = dataN
        self.nacionalitat = nacionalitat

    def to_JSON(self):
        return {
            'nomP'          : self.nomP,
            'dataN'         : self.dataN, # Format.convert_date(self.dataN) if isinstance(self.dataN, datetime.date) else self.dataN,
            'nacionalitat'  : self.nacionalitat
        }

    def get_atributtes():
        return ('nomP', 'dataN', 'nacionalitat')
    
    def get_headings():
        return ('Nom', 'Data de naixement', 'Nacionalitat')
    
    def get_id():
        return ('nomP')