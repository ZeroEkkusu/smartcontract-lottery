from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest


def test_can_start_and_enter_lottery():
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

    # (Act)
    # Call the enter function
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # (Assert)
    # that the entry has been stored
    assert lottery.players(0) == account.address
