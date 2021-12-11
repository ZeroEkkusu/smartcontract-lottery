// SPDX-License-Identifier: MIT
// Desc: All copies of this software or its substantial portions
// must include a copy of the terms of the MIT License and also a copyright notice,
// and may be distributed under different terms and without source code

// Soldity version 0.8.X
pragma solidity ^0.8.0;

// (📜 See brownie-config.yaml for dependencies)
// For Chainlink price feeds
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
// For contract ownership management
import "@openzeppelin/contracts/access/Ownable.sol";
// For verifiable random number generation
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

// Inherit the functionailty
contract Lottery is VRFConsumerBase, Ownable {
    // Define possible lottery states (values: 0, 1, 2)
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    // Current lottery state
    LOTTERY_STATE public lottery_state;
    // Minimum entry fee, in USD
    uint256 public usdEntryFee;
    // Chainlink price feed interface (internal - not accessible from the outside)
    AggregatorV3Interface internal ethUsdPriceFeed;
    // Lottery entries (payable - can receive funds from this contract)
    address payable[] public players;

    // (Working with VRFConsumerBase)
    // Public key against which randomness is generated
    bytes32 public keyHash;
    // VRF service fee, in LINK
    uint256 public fee;

    // The winner of last lottery
    address payable public recentWinner;
    // The randomness used in last lottery
    uint256 public randomness;

    // Define events
    // (Similar to printing out to the console in the traditional programming
    // Stored in log entries on the blockchain, not accessible by smart contracts)
    // VRF service request ID
    event RequestedRandomness(bytes32 requestId);
    // Random number
    event RandomnessReceived(uint256 _randomness);

    // ℹ️ Working with 18 decimals

    // Add any inherited constructors before the body
    constructor(
        address _priceFeedAddress,
        uint256 _fee,
        bytes32 _keyHash,
        // VRFCoordinator contract address
        address _vrfCoordinator,
        // LINK contract address
        address _link
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        // 50 USD entry fee
        usdEntryFee = 50e18;
        // ETH/USD price feed contract
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        // Lottery state closed
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    // Starts the lottery (onlyOwner - proceeds only if called by the owner)
    function startLottery() public onlyOwner {
        // Can't start a new lottery if the current one has not ended
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    // Returns the minimum entrance fee in wei (view - cannot change the state)
    function getEntranceFee() public view returns (uint256) {
        // Get the latest ETH/USD exchange rate
        // (Returns a tuple; skip other values)
        (, int256 answer, , , ) = ethUsdPriceFeed.latestRoundData();
        // The answer has 8 decimals, add 10 more
        uint256 adjustedPrice = uint256(answer) * 1e10;
        // Calculate the fee (multiply before dividing!)
        uint256 costToEnter = (usdEntryFee * 1e18) / adjustedPrice;
        return costToEnter;
    }

    // Allows anyone to enter the lottery (payable - accepts ETH)
    function enter() public payable {
        // if it's open
        require(lottery_state == LOTTERY_STATE.OPEN);
        // and they pay the entry fee
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        // Store the entry
        players.push(payable(msg.sender));
    }

    // Ends the lottery and requests randomness
    function endLottery() public onlyOwner {
        // Lock other functionality
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        // (Request and receive data cycle)
        // Requesting data from VRFCoordinator
        bytes32 requestId = requestRandomness(keyHash, fee);
        // Emit an event for testing purposes
        emit RequestedRandomness(requestId);
    }

    // Picks a winner
    // (Request and receive data cycle)
    // Receiving data from VRFCoordinator
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        // Proceed if waiting for response
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet"
        );
        // The random number shouldn't be 0
        require(_randomness > 0, "random-not-found");
        // Pick a winner
        // (Let's say randomness is 11 and there are 4 entries
        // 11 % 4 The reminder can't be >= 4)
        uint256 indexOfWinner = _randomness % players.length;
        // Store their address
        recentWinner = players[indexOfWinner];
        // Transfer the funds
        recentWinner.transfer(address(this).balance);
        // Store the randomeness
        randomness = _randomness;
        // Clear entries
        players = new address payable[](0);
        // Close the lottery
        lottery_state = LOTTERY_STATE.CLOSED;
        // Emit an event for testing purposes
        emit RandomnessReceived(_randomness);
    }
}
