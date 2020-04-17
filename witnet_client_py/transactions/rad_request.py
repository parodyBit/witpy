from witnet_client_py.util import radon_to_cbor


class RadRequest:

    def __init__(self):
        self.time_lock = 0
        self.retrieve = []
        self.aggregate = {'filters': [],'reducer': 3}
        self.tally = {'filters': [], 'reducer': 3}

    def add_source(self, source):
        source.encode()
        self.retrieve.append({'kind': 'HTTP-GET', 'url': source.url, 'script': radon_to_cbor(source.script)})
        return self

    def set_aggregate(self, aggregator):
        self.aggregate['filters'].append({'args': radon_to_cbor(aggregator.filters[0]['args']), 'op': aggregator.filters[0]['op']})
        self.aggregate['reducer'] = aggregator.reducer
        return self

    def set_tally(self, tally):
        self.aggregate['filters'].append({'args': radon_to_cbor(tally.filters[0]['args']), 'op': tally.filters[0]['op']})
        self.aggregate['reducer'] = tally.reducer
        return self

    def to_json(self):
        return {
            'aggregate': self.aggregate,
            'retrieve': self.retrieve,
            'tally': self.tally,
            'time_lock': self.time_lock
        }
