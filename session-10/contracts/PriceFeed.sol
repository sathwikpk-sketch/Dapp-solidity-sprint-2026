// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract PriceFeed {
    address public owner;
    address public oracle;
    int256 public price; // USD price scaled to 8 decimals
    uint256 public updatedAt;
    uint80 public roundId;
    event OracleChanged(address indexed previousOracle,address indexed newOracle);
    event PriceUpdated(uint80 indexed roundId,int256 price,uint256 updatedAt,address indexed updater);
    modifier onlyOwner(){require(msg.sender==owner,'Only owner');_;}
    modifier onlyOracle(){require(msg.sender==oracle,'Only oracle');_;}
    constructor(address initialOracle){require(initialOracle!=address(0),'Zero oracle');owner=msg.sender;oracle=initialOracle;}
    function setOracle(address nextOracle) external onlyOwner {require(nextOracle!=address(0),'Zero oracle');emit OracleChanged(oracle,nextOracle);oracle=nextOracle;}
    function updatePrice(int256 nextPrice) external onlyOracle {require(nextPrice>0,'Price must be positive');price=nextPrice;updatedAt=block.timestamp;roundId++;emit PriceUpdated(roundId,nextPrice,block.timestamp,msg.sender);}
    function latestPrice() external view returns(uint80,int256,uint256){return(roundId,price,updatedAt);}
}
