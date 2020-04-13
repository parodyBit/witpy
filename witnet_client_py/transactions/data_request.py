class DataRequest:
    def __init__(self):
        self.data_request = {}
        self.witness_reward = 10
        self.witnesses = 20
        self.backup_witnesses = 5
        self.commit_fee = 1
        self.reveal_fee = 1
        self.tally_fee = 1
        self.extra_commit_rounds = 3
        self.extra_reveal_rounds = 3
        self.min_consensus_percentage = 3

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

