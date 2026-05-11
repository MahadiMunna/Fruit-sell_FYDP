// SPDX-License-Identifier: MIT
pragma solidity ^0.7.1;

contract FruitTrace {
    struct Fruit {
        string name;
        string location;
        uint256 supplyDate;
        uint256 expiryDate;
        string vendor;
        string traceInfo;
        uint256 fruitId;
    }

    mapping(uint256 => Fruit) public fruits;

    event FruitAdded(uint256 fruitId, string name, string location);

    function addFruit(
        string memory name,
        string memory location,
        uint256 supplyDate,
        uint256 expiryDate,
        string memory vendor,
        string memory traceInfo,
        uint256 fruitId
    ) public {
        fruits[fruitId] = Fruit(name, location, supplyDate, expiryDate, vendor, traceInfo, fruitId);
        emit FruitAdded(fruitId, name, location);
    }

    function getFruit(uint256 fruitId) public view returns (
        string memory name,
        string memory location,
        uint256 supplyDate,
        uint256 expiryDate,
        string memory vendor,
        string memory traceInfo
    ) {
        Fruit storage fruit = fruits[fruitId];
        return (
            fruit.name,
            fruit.location,
            fruit.supplyDate,
            fruit.expiryDate,
            fruit.vendor,
            fruit.traceInfo
        );
    }
}
