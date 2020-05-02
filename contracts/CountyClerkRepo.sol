pragma solidity >=0.4.21 <0.7.0;

import "/Users/shaunhillin/Documents/WebstormProjects/final_project/node_modules/@openzeppelin/contracts/token/ERC721/ERC721Full.sol";


contract CountyClerkRepo is ERC721Full {

    struct DeedInfo{
        string name;
        string propAddress;
        bool owned;
        uint256 accountNumber;
        uint256[] chain;
        uint owners;
    }

    // mapping from deedid to DeedInfo
    mapping (uint256 => DeedInfo) private deeds;

    // All deeds need an account number
    // know what deed is up next to be created
    uint256 private nextAccount=0;

    //mapping from deed id to account number
    //gives you the ability to lookup deeds by account number
    mapping (uint256 => uint256) private accounts;

    constructor() public ERC721Full("County Clerk Title Repository", "CCTP"){
    }
    /**
    * Used to register new deed
    **/
    function registerDeed(uint256 _tokenId, string memory _name, string memory _address) public{
        //Check to see if their is an existing owner
        require(deeds[_tokenId].owned != true);
        _mint(msg.sender, _tokenId);
        addDeedData(_tokenId, _name, _address );
        //increase account number by 1
        nextAccount += 1;
        emit DeedRegistered(msg.sender, _tokenId, deeds[_tokenId].name, deeds[_tokenId].propAddress);
    }

    function changeDeed(uint256 _tokenId, string memory _name) public{
        //TODO Lookup deed by account number
        //Check to see if the deed exist
        require(deeds[_tokenId].owned != false);
        changeDeedOwner(_tokenId, _name);
        //increase account number by 1
        nextAccount += 1;
        emit DeedUpdate(msg.sender, _tokenId, deeds[_tokenId].name);
    }

    function retrieveDeedOwner(uint256 _tokenId) public view returns(string memory){
        return(deeds[_tokenId].name);
    }

    function retrieveDeedAddress(uint256 _tokenId) public view returns(string memory){
        return(deeds[_tokenId].propAddress);
    }

    function retrieveDeedStatus(uint256 _tokenId) public view returns(bool){
        return(deeds[_tokenId].owned);
    }

    function retrieveNextAccount() public view returns(uint){
        return(nextAccount);
    }

    function retrieveAccountNumber(uint256 _tokenId) public view returns(uint256){
        return(deeds[_tokenId].accountNumber);
    }

    function retrieveChainTitle(uint256 _tokenId) public view returns(uint256[] memory){
        return(deeds[_tokenId].chain);
    }

    //functions returns the id of the next available
    function addDeedData(uint256 _tokenId, string memory _name, string memory _address) public {
        DeedInfo memory d;
        d.name = _name;
        d.propAddress = _address;
        d.owned = true;
        d.accountNumber = nextAccount;
        d.owners = 1;
        deeds[_tokenId] = d;
        deeds[_tokenId].chain.push(nextAccount);
    }


    //updates owner, adds old owner to chain of title, and references new account number
    function changeDeedOwner(uint256 _tokenId, string memory _name) public {
        //push new account number to chain
        deeds[_tokenId].chain.push(nextAccount);
        deeds[_tokenId].name= _name;
        deeds[_tokenId].accountNumber = nextAccount;
        emit DeedUpdate(msg.sender, _tokenId, deeds[_tokenId].name);
    }

        //given a token id return chainofTitle


    event DeedUpdate(address _by, uint256 _tokenId, string _name);

    event DeedRegistered(address _by, uint256 _tokenId, string _name, string _address);
}



