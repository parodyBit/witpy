class RadRequest:

    def __init__(self):
        self.time_lock = 0
        self.retrieve = []
        self.aggregate = {'filters': [],'reducer':3}
        self.tally = {'filters': [], 'reducer': 3}

    def add_script(self, kind='', url='', script=None):
        if script is None:
            script = []
        self.retrieve.append({'kind': kind, 'url': url, 'script': script})


    def to_json(self):
        return {
            'aggregate': self.aggregate,
            'retrieve': self.retrieve,

            'tally': self.tally,
            'time_lock': self.time_lock
        }
