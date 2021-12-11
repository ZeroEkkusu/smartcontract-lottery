from scripts.helpful_scripts import get_account
from brownie import Lottery


def enter_lottery(index=None, id=None, env=None):
    # Enters the lottery with an account

    # Get the account that will make the transaction
    account = get_account(index=index, id=id, env=env)
    # Grab last Lottery deployment
    lottery = Lottery[-1]
    # Call the getEntraceFee function
    value = lottery.getEntranceFee()
    print("Entering Lottery...\n")
    # Call the enter function
    lottery.enter({"from": account, "value": value})


def main():
    enter_lottery()
