// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract LandRegister is AccessControl {
    bytes32 public constant NOTARY_ROLE = keccak256("NOTARY_ROLE");

    struct Property {
        address owner;
        bytes32 dataHash;
        bool exists;
    }

    mapping(string => Property) private properties;

    event PropertyRegistered(string kwId, address owner, bytes32 dataHash);
    event PropertyTransferred(string kwId, address from, address to);
    event PropertyUpdated(string kwId, bytes32 newDataHash);

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function addNotary(address notary)
        external
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        _grantRole(NOTARY_ROLE, notary);
    }

    function registerProperty(
        string memory kwId,
        bytes32 dataHash,
        address owner
    ) external onlyRole(NOTARY_ROLE) {
        require(!properties[kwId].exists, "Property exists");

        properties[kwId] = Property({
            owner: owner,
            dataHash: dataHash,
            exists: true
        });

        emit PropertyRegistered(kwId, owner, dataHash);
    }

    function transferProperty(
        string memory kwId,
        address newOwner
    ) external onlyRole(NOTARY_ROLE) {
        require(properties[kwId].exists, "Not found");

        address previousOwner = properties[kwId].owner;
        properties[kwId].owner = newOwner;

        emit PropertyTransferred(kwId, previousOwner, newOwner);
    }

    function updatePropertyData(
        string memory kwId,
        bytes32 newDataHash
    ) external onlyRole(NOTARY_ROLE) {
        require(properties[kwId].exists, "Not found");

        properties[kwId].dataHash = newDataHash;
        emit PropertyUpdated(kwId, newDataHash);
    }

    function getProperty(string memory kwId)
        external
        view
        returns (address owner, bytes32 dataHash)
    {
        require(properties[kwId].exists, "Not found");
        Property memory p = properties[kwId];
        return (p.owner, p.dataHash);
    }
}
