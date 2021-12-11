from scripts.helpful_scripts import get_account
from brownie import Lottery


def start_lottery(index=None, id=None, env=None):
    # Starts the lottery

    # Get the account that will make the transaction
    account = get_account(index=index, id=id, env=env)
    # Grab last Lottery deployment
    lottery = Lottery[-1]
    print("Starting Lottery...\n")
    # Call the startLottery function
    lottery.startLottery({"from": account})


def main():
    start_lottery()
