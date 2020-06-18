from ..util.jsonrpc.requests import Request
from ..util.jsonrpc.exceptions import ReceivedNon2xxResponseError, ReceivedErrorResponseError, ErrorResponse
from ..util.websocket import WebSocket
from ..util.websocket import WebSocketException
import subprocess
import threading
import os
import time
import json
import sys

wallet_url = '127.0.0.1:11212'


class Wallet:
    def __init__(self, session_id=''):
        self.session_id = session_id


class WalletClient:
    _instance = None

    def __init__(self, url='127.0.0.1', port=11212):
        if WalletClient._instance is not None:
            raise Exception('Singleton')
        else:
            WalletClient._instance = self
            self.url = url
            self.running = False
            self.wallet_thread = None
            self.set_url_port(url=url, port=port)
            self.ws = WebSocket()



    @staticmethod
    def socket(url='127.0.0.1', port=11212):
        """
        :param url:
        :param port:
        :return:
        """
        if WalletClient._instance is None:
            return WalletClient(url=url, port=port)
        else:
            return WalletClient._instance

    def set_url_port(self, url='127.0.0.1', port=11212):
        """
        :param url:
        :param port:
        :return:
        """
        self.url = f'{url}:{port}'

    def poll_server(self, command='', **kwargs):
        """
        :param command:
        :param kwargs:
        :return:
        """
        response = None
        try:
            self.ws.connect(f"ws://{self.url}/")
            request = Request(command, **kwargs)

            self.ws.send(f'{request}')
            response = self.ws.recv()
        except Exception as error:
            print(error)
        if response is None:
            return response
        else:
            return json.loads(response)['result']

    # length must be: 12, 15, 18, 21, 24
    # create_mnemonics(length=12)
    def create_mnemonics(self, length=12):
        """
        Creates a BIP39 mnemonic word sentence that can be used to generate a new HD wallet
        :param length: Integer. valid lengths are: 12, 15, 18, 21, 24
        :return: A dict with key 'mnemonics' containing the word phrase OR returns None
        """
        return self.poll_server(command='create_mnemonics', length=length)

    def create_wallet(self, name='', caption='', password='', seed_source='mnemonics/xprv', seed_data=''):
        """

        :param name: A human-friendly name for your the wallet. (optional)
        :param caption: A human-friendly caption for your the wallet. (optional)
        :param password:  The password that will seed the key used to encrypt
                          the wallet in the file system. The password must have
                          at least eight characters.
        :param seed_source: Must be `mnemonics` or `xprv` and determines
                            how the HD wallet master key will be generated
                            from the data sent in the `seedData` param.
        :param seed_data: The data used for generating the new HD wallet master key.
        :return:
        """
        return self.poll_server(command='create_wallet', name=name, caption=caption,
                                password=password, seed_source=seed_source, seed_data=seed_data)

    def unlock_wallet(self, wallet_id='', password=''):
        """

        :param wallet_id: The ID associated to the wallet.
        :param password: The password that unlocks the wallet.
        :return:
        """
        return self.poll_server(command='unlock_wallet', wallet_id=wallet_id, password=password)

    def lock_wallet(self, wallet_id='', session_id=''):
        """
        `lock_wallet` is used to *lock* the wallet with the specified id
        and close the active session. What does it mean to *lock a wallet*?
        It means that the decryption key for that wallet that is being hold
        in memory is forgotten and the Wallet server will be unable to update
        that wallet information until it is unlocked again.

        :param wallet_id: The ID associated to the wallet.
        :param session_id: The session ID assigned to you when you unlocked the wallet.
        :return:
        """
        return self.poll_server(command='lock_wallet', wallet_id=wallet_id, session_id=session_id)

    def run_rad_request(self, rad_request={}):
        """

        :param rad_request:
        :return:
        """
        return self.poll_server(command='run_rad_request', rad_request=rad_request)

    def close_session(self, session_id=''):
        """

        :param session_id:
        :return:
        """
        return self.poll_server(command='close_session', session_id=session_id)

    def create_data_request(self, wallet_id='', session_id='', request={}, fee=0):
        """

        :param wallet_id:
        :param session_id:
        :param request:
        :param fee:
        :return:
        """
        return self.poll_server(command='create_data_request', wallet_id=wallet_id, session_id=session_id,
                                request=request, fee=fee)

    def create_vtt(self, wallet_id='', session_id='', address='', amount=0, fee=0, time_lock=0):
        """

        :param wallet_id:
        :param session_id:
        :param address:
        :param amount:
        :param fee:
        :param time_lock:
        :return:
        """
        return self.poll_server(command='create_vtt', wallet_id=wallet_id, session_id=session_id,
                                address=address, amount=amount, fee=fee, time_lock=time_lock)

    def get_wallet_infos(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.poll_server(command='get_wallet_infos', **kwargs)

    def generate_address(self, wallet_id='', session_id=''):
        """

        :param wallet_id:
        :param session_id:
        :return:
        """
        return self.poll_server(command='generate_address', wallet_id=wallet_id, session_id=session_id)

    def get_addresses(self, wallet_id='', session_id='', offset=0, limit=0):
        """

        :param wallet_id:
        :param session_id:
        :param offset:
        :param limit:
        :return:
        """
        return self.poll_server(command='get_addresses', wallet_id=wallet_id, session_id=session_id,
                                offset=offset, limit=limit)

    def import_seed(self, mnemonics='', seed=''):
        """

        :param mnemonics:
        :param seed:
        :return:
        """
        return self.poll_server(command='import_seed', mnemonics=mnemonics, seed=seed)

    def next_subscription_id(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.poll_server(command='next_subscription_id', **kwargs)

    def get_transactions(self, wallet_id='', session_id='', offset=0, limit=0):
        """

        :param wallet_id:
        :param session_id:
        :param offset:
        :param limit:
        :return:
        """
        return self.poll_server(command='get_transactions', wallet_id=wallet_id, session_id=session_id,
                                offset=offset, limit=limit)

    def send_transaction(self, wallet_id='', session_id='', transaction={}):
        """

        :param wallet_id:
        :param session_id:
        :param transaction:
        :return:
        """
        return self.poll_server(command='send_transaction', wallet_id=wallet_id, session_id=session_id,
                                transaction=transaction)

    def unsubscribe_notifications(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.poll_server(command='unsubscribe_notifications', **kwargs)

    def subscribe_notifications(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.poll_server(command='subscribe_notifications', **kwargs)

    def update_wallet(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.poll_server(command='update_wallet', **kwargs)

    # Forwarded methods

    # this method is the only one to pass a list instead of a map for **kwargs
    # need to refactor
    def get_block(self, block):
        """

        :param block:
        :return:
        """
        response = None
        try:
            self.ws.connect(f"ws://{self.url}/")
            request = Request('get_block', block)
            self.ws.send(f'{request}')
            response = self.ws.recv()
        except Exception as error:
            print(error)

        if response is None:
            return response
        else:
            return json.loads(response)['result']

    def get_block_chain(self, epoch=-1, limit=1):
        """

        :param limit:
        :param epoch:
        :return:
        """
        return self.poll_server(command='get_block_chain', epoch=epoch, limit=limit)


# Test Wallet Function


def main():
    wallet = WalletClient().socket(url='127.0.0.1', port=11212)
    wallet.create_mnemonics(length=12)


if __name__ == '__main__':
    main()
