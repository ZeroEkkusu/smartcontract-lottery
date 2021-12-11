from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, wait_for_randomness
from brownie import network
import pytest
from scripts.deploy_lottery import deploy_lottery


def test_can_pick_winner():
    # A basic integration test

    # Only on an actual mainnet/testnet
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploy a Lottery
    lottery = deploy_lottery()
    # Get the actual accounts that will participate in the lottery
    account = get_account(env="key1")
    account2 = get_account(env="key2")
    # Call the startLottery function
    lottery.startLottery({"from": account})
    # These will be the entries
    entries = [account, account2, account, account2]
    # Call the enter function for each entry
    for a in entries:
        lottery.enter({"from": a, "value": lottery.getEntranceFee()})
    # Fund the contract with LINK
    fund_with_link(lottery)
    # Call the endLottery function
    lottery.endLottery({"from": account})
    # Wait for and get the randomness
    randomness = wait_for_randomness(lottery)
    # Assert that the right account has been picked as the winner
    assert lottery.recentWinner() == entries[randomness % len(entries)].address
    # Assert that the funds have been transfered
    assert lottery.balance() == 0
