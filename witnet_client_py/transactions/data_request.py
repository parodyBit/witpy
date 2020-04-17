from witnet_client_py.util import radon_to_cbor


class DataRequest:
    def __init__(self):
        self.data_request = {'aggregate': {'filters': [], 'reducer': None},
                             'retrieve': [],
                             'tally': {'filters': [], 'reducer': None}
                             }
        self.witness_reward = 1
        self.witnesses = 1
        self.backup_witnesses = 1
        self.commit_fee = 1
        self.reveal_fee = 1
        self.tally_fee = 1
        self.extra_commit_rounds = 1
        self.extra_reveal_rounds = 1
        self.min_consensus_percentage = 51
        self.report = None

    def add_source(self, source):
        source.encode()
        self.data_request['retrieve'].append({'kind': 'HTTP-GET', 'url': source.url,
                                              'script': radon_to_cbor(source.script)})
        return self

    def set_aggregate(self, aggregator):
        self.data_request['aggregate']['reducer'] = aggregator.reducer
        self.data_request['aggregate']['filters'].append({'args': radon_to_cbor(aggregator.filters[0]['args']),
                                                          'op': aggregator.filters[0]['op']})
        return self

    def set_tally(self, tally):
        self.data_request['tally']['reducer'] = tally.reducer
        self.data_request['tally']['filters'].append({'args': radon_to_cbor(tally.filters[0]['args']),
                                                      'op': tally.filters[0]['op']})
        return self

    def set_quorum(self, witnesses,
                   backup_witnesses,
                   extra_commit_rounds,
                   extra_reveal_rounds,
                   min_consensus_percentage):
        self.witnesses = witnesses
        self.backup_witnesses = backup_witnesses
        self.extra_commit_rounds = extra_commit_rounds
        self.extra_reveal_rounds = extra_reveal_rounds
        self.min_consensus_percentage = min_consensus_percentage
        return self

    def set_fees(self, reward, commit_fee, reveal_fee, tally_fee):
        self.witness_reward = reward
        self.commit_fee = commit_fee
        self.reveal_fee = reveal_fee
        self.tally_fee = tally_fee
        return self
    def to_json(self):
        return {
            "data_request": self.data_request,
            "witness_reward": self.witness_reward,
            "witnesses": self.witnesses,
            "backup_witnesses": self.backup_witnesses,
            "commit_fee": self.commit_fee,
            "reveal_fee": self.reveal_fee,
            "tally_fee": self.tally_fee,
            "extra_commit_rounds": self.extra_commit_rounds,
            "extra_reveal_rounds": self.extra_reveal_rounds,
            "min_consensus_percentage": self.min_consensus_percentage,
        }
