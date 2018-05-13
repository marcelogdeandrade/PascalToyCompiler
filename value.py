class Value():
    def __init__(self, var_type):
        self.type = var_type
        self.value = None

    def setValue(self, value):
        self.value = value

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

