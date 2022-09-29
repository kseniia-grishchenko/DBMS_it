class Row:
    def __init__(self, values):
        self.values = values

    def __getitem__(self, index):
        return self.values[index]

    def __str__(self):
        return f'[{", ".join(map(str, self.values))}]'

    def __repr__(self):
        return f'[{", ".join(map(str, self.values))}]'

