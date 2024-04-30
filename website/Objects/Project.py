class Project: 
    def __init__(self, name : str, children : list = [], deadline = None) -> None:
        self.name = name
        self.children = children
        self.deadline = deadline

    def get_estimate(self):
        estimate = 0
        for c in self.children:
            estimate += c.get_estimate()
        return estimate
