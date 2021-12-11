# About
This is an example of a full scale smart contract project, made using [Solidity](https://github.com/ethereum/solidity) and [Brownie](https://github.com/eth-brownie/brownie). You can use this repo as reference when starting a new project.

How the contract works:
1. Anyone can enter the lottery with 50 USD or more worth of ETH
2. The owner will choose when the lottery is over
3. The lottery will select one random winner and transfer the funds
### Todo
- Use Chainlink Keepers to end the lottery
# Setup
*Note: This isn't a guide on how to set up system for development! For that, see [PatrickAlphaC/smartcontract-lottery](https://github.com/PatrickAlphaC/smartcontract-lottery/blob/main/README.md), which this project is based on.*

To set up your new project, either:

Use [chainlink-mix](https://github.com/brownie-mix/chainlink-mix)
```bash
brownie bake chainlink-mix && mv chainlink <your_project_name>
```
Or start from scratch
```bash
brownie init
```
## Other files
Create a `.env` file inside your project's directory and add the following
```
export PRIVATE_KEY_1 = <YOUR_PRIVATE_KEY_1>
export PRIVATE_KEY_2 = <YOUR_PRIVATE_KEY_2>
export WEB3_INFURA_PROJECT_ID = <YOUR_PROJECT_ID>
export ETHERSCAN_TOKEN = <YOUR_API_TOKEN>
```
To encrypt your private key, add it to Brownie instead
```bash
brownie accounts new <choose_account_id>
```
# Usage
### Compile
```bash
brownie compile
```
### Test
```bash
brownie test --network <choose_network> -s
```
### Deploy
```bash
brownie run scripts/deploy_lottery.py --network <choose_network>
```
