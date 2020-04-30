import websockets
import asyncio

from jsonrpcclient.exceptions import ReceivedNon2xxResponseError, ReceivedErrorResponseError
from jsonrpcclient.clients.websockets_client import WebSocketsClient

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
            self.url = ''
            self.running = False
            self.wallet_thread = None
            self.set_url_port(url=url, port=port)

    @staticmethod
    def socket(url='127.0.0.1', port=11212):
        if WalletClient._instance is None:
            return WalletClient(url=url, port=port)
        else:
            return WalletClient._instance

    def set_url_port(self, url='', port=0):
        self.url = f'{url}:{port}'

    def poll_server(self, command='', **kwargs):
        async def _request():
            response = None
            async with websockets.connect(f"ws://{self.url}/") as ws:
                try:
                    response = await WebSocketsClient(ws).request(command, **kwargs)

                except ReceivedErrorResponseError as error:
                    print('Response Error: ', error.response.code, error.response.message)
                except ReceivedNon2xxResponseError as error:
                    print(error)
            if response is None:
                return response
            else:
                return response.data.result

        return asyncio.get_event_loop().run_until_complete(_request())

    # length must be: 12, 15, 18, 21, 24
    # create_mnemonics(length=12)
    def create_mnemonics(self, length=12):
        return self.poll_server(command='create_mnemonics', length=length)

    def create_wallet(self, name='', caption='', password='', seed_source='mnemonics/xprv', seed_data=''):
        return self.poll_server(command='create_wallet', name=name, caption=caption,
                                password=password, seed_source=seed_source, seed_data=seed_data)

    def unlock_wallet(self, wallet_id='', password=''):
        return self.poll_server(command='unlock_wallet', wallet_id=wallet_id, password=password)

    def lock_wallet(self, wallet_id='', session_id=''):
        return self.poll_server(command='lock_wallet', wallet_id=wallet_id, session_id=session_id)

    def run_rad_request(self, rad_request={}):
        return self.poll_server(command='run_rad_request', rad_request=rad_request)

    def close_session(self, session_id=''):
        return self.poll_server(command='close_session', session_id=session_id)

    def create_data_request(self, wallet_id='', session_id='', request={}, fee=0):
        return self.poll_server(command='create_data_request', wallet_id=wallet_id, session_id=session_id,
                                request=request, fee=fee)

    def create_vtt(self, wallet_id='', session_id='', address='', amount=0, fee=0, time_lock=0):
        return self.poll_server(command='create_vtt', wallet_id=wallet_id, session_id=session_id,
                                address=address, amount=amount, fee=fee, time_lock=time_lock)

    def get_wallet_infos(self, **kwargs):
        return self.poll_server(command='get_wallet_infos', **kwargs)

    def generate_address(self, wallet_id='', session_id=''):
        return self.poll_server(command='generate_address', wallet_id=wallet_id, session_id=session_id)

    def get_addresses(self, wallet_id='', session_id='', offset=0, limit=0):
        return self.poll_server(command='get_addresses', wallet_id=wallet_id, session_id=session_id,
                                offset=offset, limit=limit)

    def import_seed(self, mnemonics='', seed=''):
        return self.poll_server(command='import_seed', mnemonics=mnemonics, seed=seed)

    def next_subscription_id(self, **kwargs):
        return self.poll_server(command='next_subscription_id', **kwargs)

    def get_transactions(self, wallet_id='', session_id='', offset=0, limit=0):
        return self.poll_server(command='get_transactions', wallet_id=wallet_id, session_id=session_id,
                                offset=offset, limit=limit)

    def send_transaction(self, wallet_id='', session_id='', transaction={}):
        return self.poll_server(command='send_transaction', wallet_id=wallet_id, session_id=session_id,
                                transaction=transaction)

    def unsubscribe_notifications(self, **kwargs):
        return self.poll_server(command='unsubscribe_notifications', **kwargs)

    def subscribe_notifications(self, **kwargs):
        return self.poll_server(command='subscribe_notifications', **kwargs)

    def update_wallet(self, **kwargs):
        return self.poll_server(command='update_wallet', **kwargs)

    # Forwarded methods

    # this method is the only one to pass a list instead of a map for **kwargs
    # need to refactor
    def get_block(self, block):
        async def _request():
            response = None
            async with websockets.connect(f"ws://{self.url}/") as ws:
                try:
                    response = await WebSocketsClient(ws).request('get_block', block)
                except ReceivedErrorResponseError as error:
                    print('Response Error: ', error.response.code, error.response.message)
                except ReceivedNon2xxResponseError as error:
                    print(error)
            if response is None:
                return response
            else:
                return response.data.result

        return asyncio.get_event_loop().run_until_complete(_request())

    def get_block_chain(self, **kwargs):
        return self.poll_server(command='get_block_chain', **kwargs)

# Test Wallet Function


def main():
    wallet = WalletClient().socket(url='127.0.0.1', port=11212)
    wallet.create_mnemonics(length=12)


if __name__ == '__main__':
    main()
