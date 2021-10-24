class GeneralUtils:
    @staticmethod
    def filter_dict(dictionary, keys):
        return {k: v for k, v in dictionary.items() if k in keys}