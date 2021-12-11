from scripts.helpful_scripts import get_account, fund_with_link
from brownie import Lottery


def end_lottery(index=None, id=None, env=None):
    # Ends the lottery and returns the randomness if on an actual mainnet/testnet

    # Get the account that will make the transaction
    account = get_account(index=index, id=id, env=env)
    # Grab last Lottery deployment
    lottery = Lottery[-1]
    # Fund the contract with LINK
    fund_with_link(lottery)
    print("Ending Lottery...\n")
    # Call the endLottery function
    lottery.endLottery({"from": account})


def main():
    end_lottery()
