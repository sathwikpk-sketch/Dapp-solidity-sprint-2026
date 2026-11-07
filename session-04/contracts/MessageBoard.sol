// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract MessageBoardEvents {
    string private message;
    event MessageUpdated(address indexed editor, string newMessage);
    constructor(string memory initialMessage) { message = initialMessage; }
    function getMessage() external view returns(string memory) { return message; }
    function setMessage(string calldata nextMessage) external { message=nextMessage; emit MessageUpdated(msg.sender,nextMessage); }
}
