import inflect

class GeneralUtils:
    @staticmethod
    def filter_dict(dictionary, keys):
        return {k: v for k, v in dictionary.items() if k in keys}
    
    # @staticmethod
    # def get_ordinal(n):
    #     return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]) ### https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712

    @staticmethod
    def get_ordinal(n):
        if n >= 1 and n <= 4:
            d = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}
            return d[n]
        else:
            p = inflect.engine()
            return p.number_to_words(p.ordinal(n))
            
    
    @staticmethod
    def safe_isinstance(obj: object, type: str) -> bool:
        ### Probably not fully valid but helps to prevent circular imports
        return obj.__class__.__name__ == type