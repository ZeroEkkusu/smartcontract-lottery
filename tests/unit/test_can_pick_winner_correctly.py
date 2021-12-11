from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, get_contract
import pytest


def test_can_pick_winner_correctly():
    # (Arrange)
    # Only on a local, non-forked network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploy a Lottery
    lottery = deploy_lottery()
    # Get accounts, which will participate in the lottery
    account = get_account(index=0)
    account2 = get_account(index=1)
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
    transaction = lottery.endLottery({"from": account})

    # (Act)
    # Grab the requestId
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    # The randomness
    STATIC_RNG = 777
    # Let's pretend I'm a Chainlink node and call the VRFCoordinatorMock's callBackWithRandomness function
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery, {"from": account})
    # Save the balances
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    # (Assert)
    # that the right account has been picked as the winner
    assert lottery.recentWinner() == entries[STATIC_RNG % len(entries)].address
    # that the funds have been transfered
    assert lottery.balance() == 0
    # that the winner has received the funds
    assert account.balance() == starting_balance_of_account + balance_of_lottery
