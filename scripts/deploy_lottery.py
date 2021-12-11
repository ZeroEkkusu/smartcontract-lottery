from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery, network, config


def deploy_lottery(index=None, id=None, env=None):
    # Deploys a Lottery contract and returns the deployment

    # Get the account that will make the transaction
    account = get_account(index=index, id=id, env=env)
    print(f"The active network is {network.show_active()}\n")
    print("Deploying Lottery...\n")
    # Deploy the contract
    lottery = Lottery.deploy(
        # Get ETH/USD price feed contract address
        get_contract("eth_usd_price_feed").address,
        # Get VRF service fee, in LINK
        config["networks"][network.show_active()]["fee"],
        # Get the public key
        config["networks"][network.show_active()]["keyhash"],
        # Get VRFCoordinator contract address
        get_contract("vrf_coordinator").address,
        # Get LINK contract address
        get_contract("link_token").address,
        # Low-level transaction parameters
        {"from": account},
        # Verify the contract on Etherscan, defaults to False
        publish_source=config["networks"][network.show_active()].get(
            "verify", False)
    )
    # Return the deployment
    return lottery


def main():
    deploy_lottery()
