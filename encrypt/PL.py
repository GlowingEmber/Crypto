class Expression:
    __supported_forms = ["ANF", "CNF"]
    def __init__(self, form, data):
        if form.upper() not in self.__supported_forms:
            raise ValueError(f"Propositional logic form \"{form}\" not supported")
        self.form = form
        self.data = data

    # def to_cnf(): 

    def to_anf():
        pass