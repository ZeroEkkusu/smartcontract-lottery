from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account
import pytest


def test_can_end_lottery():
    # (Arrange)
    # Only on a local, non-forked network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploy a Lottery
    lottery = deploy_lottery()
    # Get an account, which will make the transaction
    account = get_account()
    # Call the startLottery function
    lottery.startLottery({"from": account})
    # Call the enter function
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Fund the contract with LINK
    fund_with_link(lottery)

    # (Act)
    # Call the endLottery function
    lottery.endLottery({"from": account})

    # (Assert)
    # that the state is Closed
    assert lottery.lottery_state() == 2
