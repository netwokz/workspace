

class WorkOrder:
    id = None
    description = None
    owner = None
    type = None
    link = None
    pm_max_date = None

    def __init__(self, id: str, desc: str, owner: str, type: str, max: str, link: str) -> None:
        self.id = id
        self.description = desc
        self.owner = owner
        self.type = type
        self.link = link
        self.pm_max_date = max

    def get_id(self):
        return self.id
