// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Storage {
    uint256 private storedNumber;

    event NumberStored(address indexed caller, uint256 value);

    function store(uint256 number) external {
        storedNumber = number;
        emit NumberStored(msg.sender, number);
    }

    function retrieve() external view returns (uint256) {
        return storedNumber;
    }
}
