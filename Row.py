class Row:
    def __init__(self, values):
        self.values = values

    def __getitem__(self, index):
        return self.values[index]
