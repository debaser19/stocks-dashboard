import asyncio
from sre_constants import GROUPREF_EXISTS

from tastyworks.models.session import TastyAPISession
from tastyworks.models.trading_account import TradingAccount
from tastyworks.streamer import DataStreamer
from tastyworks.tastyworks_api import tasty_session

import config


async def get_positions(account, session):
	return await account.get_positions(session)


async def main(session: TastyAPISession, streamer: DataStreamer):
	accounts = await TradingAccount.get_remote_accounts(session)
	roth = accounts[0]
	trading = accounts[1]
	# print(f'Accounts available: {accounts}')

	balances = await trading.get_balance(session)
	net_liq = balances['net-liquidating-value']

	print(net_liq)
	positions = await get_positions(trading, session)
	
	for position in positions:
		print(f'Symbol: {position["symbol"]}')
		print(f'Price: {position["close-price"]}')
		print(f'Quantity: {position["quantity"]}')



if __name__ == '__main__':
	tasty_client = tasty_session.create_new_session(config.tw_user, config.tw_pass)
	streamer = DataStreamer(tasty_client)
	loop = asyncio.get_event_loop()

	try:
		loop.run_until_complete(main(tasty_client, streamer))
	except Exception as e:
		print(f'Exception in main loop: {e}')

