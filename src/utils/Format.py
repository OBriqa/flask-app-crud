import datetime
from math import ceil

OK = 'ok'
LIKE = 'LIKE'
WILDCARD = '%'
PAGE_ELEMENTS = 10
NUM_NAV_BUTTONS = 5

fid_class = {
    'nacionalitat'      :   'codi',
    'seu'               :   'codi',
    'pilotCampio'       :   'nomP',
    'constructorCampio' :   'nomC',
    'situat'            :   'codi'
}

id_class = {
    'nomC' : 'constructors',
    'nomP' : 'pilots',
    'anyT' : 'temporades',
    'codi' : 'paissos',
    'nomGP': 'granspremis'
}

comparators = ['>', '>=', '=','!=', '<=', '<']
classes = ('pilots', 'constructors', 'temporades', 'paissos', 'grans premis', 'participants', 'formades')

class Format():

    @classmethod
    def convert_date(self, date):
        return datetime.datetime.strftime(date, '%d/%m/%Y')
    
    @classmethod
    def parse_numpage(self, num_page, max_pages):
        if int(num_page) < 1:
            return 1
        elif int(num_page) > max_pages:
            return int(max_pages)
        else:
            return int(num_page)
        
    @classmethod
    def parse_comparator(self, comparator):
        return LIKE if comparator not in comparators else comparator
    
    @classmethod
    def parse_query(self, query):
        for key in query:
            if 'op' in key:
                comp = self.parse_comparator(query[key])
                if comp == LIKE:
                    query[key] = LIKE  
                    if len(query[key[:-3]]) == 0:
                        query[key[:-3]] = WILDCARD