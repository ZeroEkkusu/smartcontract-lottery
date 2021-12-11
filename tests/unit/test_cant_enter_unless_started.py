from brownie import network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest


def test_cant_enter_unless_started():
    # (Arrange)
    # Only on a local, non-forked network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploy a Lottery
    lottery = deploy_lottery()

    # (Act/Assert)
    # Assert that one can't enter the lottery if it has not started
    # (There's a problem with the GUI Ganache, this is a workaround)
    ex = ValueError if network.show_active(
    ) == "ganache-local" else exceptions.VirtualMachineError
    with pytest.raises(ex):
        lottery.enter(
            {"from": get_account(), "value": lottery.getEntranceFee()})
