// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract StorageContract {
    uint256 variable;
    bool boolVar;

    struct People {
        uint256 age;
        string name;
    }

    mapping(string => uint256) public mappingToAge;

    People[] public people;

    function store(uint256 _variable) public {
        variable = _variable;
    }

    function viewStateVar() public view returns (uint256) {
        return variable;
    }

    function addPerson(string memory _name, uint256 _age) public {
        people.push(People(_age, _name));
        mappingToAge[_name] = _age;
    }
}
