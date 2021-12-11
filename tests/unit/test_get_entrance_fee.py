from brownie import network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest


def test_get_entrance_fee():
    # (Arrange)
    # Only on a local, non-forked network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploy a Lottery
    lottery = deploy_lottery()

    # (Act)
    # Based on the 2000 initial exchange rate and the 50 entrance fee
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    # Call the getEntranceFee function
    entrance_fee = lottery.getEntranceFee()

    # (Assert)
    # that the entrance fee is the expected one
    assert expected_entrance_fee == entrance_fee
