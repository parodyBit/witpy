import websockets
import asyncio

from jsonrpcclient.exceptions import ErrorResponse, ReceivedNon2xxResponseError, ReceivedErrorResponseError
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
    def create_mnemonics(self, **kwargs):
        return self.poll_server(command='create_mnemonics', **kwargs)


    def create_wallet(self, **kwargs):
        return self.poll_server(command='create_wallet', **kwargs)

    # unlock_wallet(self, walletId='', password='')
    def unlock_wallet(self, **kwargs):
        return self.poll_server(command='unlock_wallet', **kwargs)

    # lock_wallet(self, walletId='', sessionId='')
    def lock_wallet(self, **kwargs):
        return self.poll_server(command='lock_wallet', **kwargs)

    def run_rad_request(self, **kwargs):
        return self.poll_server(command='run_rad_request', **kwargs)

    # close_session(sessionId = '<session id>')

    def close_session(self, **kwargs):
        return self.poll_server(command='close_session', **kwargs)

    def create_data_request(self, **kwargs):
        return self.poll_server(command='create_data_request', **kwargs)

    def create_vtt(self, **kwargs):
        return self.poll_server(command='create_vtt', **kwargs)

    def get_wallet_infos(self, **kwargs):
        return self.poll_server(command='get_wallet_infos', **kwargs)

    def generate_address(self, **kwargs):
        return self.poll_server(command='generate_address', **kwargs)

    def get_addresses(self, **kwargs):
        return self.poll_server(command='get_addresses', **kwargs)

    def import_seed(self, **kwargs):
        return self.poll_server(command='import_seed', **kwargs)

    def next_subscription_id(self, **kwargs):
        return self.poll_server(command='next_subscription_id', **kwargs)

    def get_transactions(self, **kwargs):
        return self.poll_server(command='get_transactions', **kwargs)

    def send_transaction(self, **kwargs):
        return self.poll_server(command='send_transaction', **kwargs)

    def unsubscribe_notifications(self, **kwargs):
        return self.poll_server(command='unsubscribe_notifications', **kwargs)

    def subscribe_notifications(self, **kwargs):
        return self.poll_server(command='subscribe_notifications', **kwargs)

    def update_wallet(self, **kwargs):
        return self.poll_server(command='update_wallet', **kwargs)

    # Forwarded methods

    def get_block(self, **kwargs):
        return self.poll_server(command='get_block', **kwargs)

    def get_block_chain(self, **kwargs):
        return self.poll_server(command='get_block_chain', **kwargs)

# Test Wallet Function


def main():
    wallet = WalletClient()
    wallet.create_mnemonics(length=12)


if __name__ == '__main__':
    main()
