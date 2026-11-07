// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
interface IPriceFeed { function latestPrice() external view returns(uint80,int256,uint256); }
contract PriceConsumer {
    IPriceFeed public immutable feed;
    uint256 public immutable maxAge;
    constructor(address feedAddress,uint256 maxPriceAge){require(feedAddress!=address(0),'Zero feed');require(maxPriceAge>0,'Zero max age');feed=IPriceFeed(feedAddress);maxAge=maxPriceAge;}
    function getLatestPrice() public view returns(int256 price,uint256 updatedAt){(,price,updatedAt)=feed.latestPrice();require(price>0,'No price available');require(block.timestamp-updatedAt<=maxAge,'Stale price');}
    function usdToWei(uint256 usdAmount) external view returns(uint256){(int256 price,)=getLatestPrice();return usdAmount*1e26/uint256(price);}
}
