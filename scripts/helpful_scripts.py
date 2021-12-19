# ℹ️ Scripts used in other files

from brownie import network, accounts, config, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken, interface, chain
import requests
import time
import web3

# Make it easier to work with networks
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None, env=None):
    # Gets the account...

    # (If specified)
    # ... from the pre-configured accounts on the passed index
    if index:
        return accounts[index]
    # ... saved to Brownie with the passed id
    if id:
        return accounts.load(id)
    # ... from the passed private key env
    if env:
        return accounts.add(config["wallets"]["from_" + env])

    # (If not specified)
    # ... from the pre-configured accounts, on index 0, when on a local network
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    # ... from the first private key env, when on an actual mainnet/testnet
    return accounts.add(config["wallets"]["from_key1"])


# Map contract types to names
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    # Deploys a mock contract if on a local, non-forked network, and returns the deployment
    # Returns a contract object, if on a mainnet/testnet

    # Get the contract type from the name
    contract_type = contract_to_mock[contract_name]

    # If on a local, non-forked network
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # deploy a mock contract if it has not been deployed
        if len(contract_type) <= 0:
            deploy_mocks()
        # and grab last deployment of this contract
        contract = contract_type[-1]
    # If on a mainnet/testnet
    else:
        # get the contract's address
        contract_adrress = config["networks"][network.show_active(
        )][contract_name]
        # and create a new contract object from ABI (use ._name and .abi to get them from a contract)
        # (ABI tells you how to interact with a contract)
        contract = Contract.from_abi(
            contract_type._name, contract_adrress, contract_type.abi)
    # Return the deployment or the contract object
    return contract


# (MockV3Aggregator-specific - imitating the actual contract)
# Working with 8 decimals
DECIMALS = 8
# Initial ETH/USD exchange rate is 2000
INITIAL_VALUE = 2000e8


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    # Deploys any mock contract

    # Get an account, which will make the transaction
    account = get_account()
    print("Deploying Mocks...\n")
    # Deploy a LinkToken contract (default constructor)
    link_token = LinkToken.deploy({"from": account})
    # Deploy a VRFCoordinatorMock contract
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    # Deploy a MockV3Aggregator contract
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})


def fund_with_link(contract_address, account=None, link_token=None, amount=1e17):
    # Funds any contract with LINK

    # If account passed, use it, get one otherwise
    account = account if account else get_account()
    # If LINK contract address passed, use it, get it otherwise
    link_token = link_token if link_token else get_contract("link_token")

    # You can create contract objects from interfaces, as well
    # (They compile down to ABI)
    # link_token = interface.LinkTokenInterface(link_token.address)

    print("Funding Contract With LINK...\n")
    # Call the transfer function
    link_token.transfer(contract_address, amount, {"from": account})


def wait_for_randomness(lottery):
    # Keeps checking for a fulfillRandomness callback using the block explorer's API, and returns the randomness

    # Initial frequency, in seconds
    sleep_time = 120
    # Last checked block num
    from_block = len(chain)
    print("Waiting For Data...\n")
    i = 1

    # Until randomness received
    while(True):
        print(f"Check #{i} in {sleep_time} secs\n")
        # Wait
        time.sleep(sleep_time)
        # Get last mined block num
        to_block = len(chain)

        # Check if randomness received
        # 🔗 See https://docs.etherscan.io/api-endpoints/logs
        response = requests.get(
            config["networks"][network.show_active()]["explorer_api"],
            params={
                "module": "logs",
                "action": "getLogs",
                "fromBlock": from_block,
                "toBlock": to_block,
                "address": lottery.address,
                "topic0": web3.Web3.keccak(text='RandomnessReceived(uint256)').hex(),
                "apikey": config["api_keys"]["etherscan"],
            },
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}).json()
        # Return randomness if received
        if response['status'] == "1":
            return int(response['result'][0]['data'], 16)

        # Half sleep time if longer than 15 seconds
        if(sleep_time > 15):
            sleep_time = int(round(sleep_time/2))

        from_block = to_block

        i += 1
