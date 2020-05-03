



### Necessary software and packages.

- Ganache
- Install python 3.7
- Solidity 0.5.5 
- Install truffle
- Requirements.txt python packages
- @openzeppelin/contracts@2.5.0


### Instructions for installing each of the above. 
    
    https://www.trufflesuite.com/ganache
    npm install truffle -g
    pip install -r requirements.txt
    
Download my repo: https://github.com/smhillin/erc721_deed
From the top level directory run the following
    
    pip install -r requirements.txt
    npm install @openzeppelin/contracts@2.5.0
    

### How to run the code. 

- Download my repo: https://github.com/smhillin/erc721_deed

- Open main.py make sure that the relative paths for contract and node module @zepplin directory are accurate.

    contract="contracts/CountyClerkRepo.sol"
    zepplin_directory="node_modules/@openzeppelin/"

- In python.main update "chain_info" with your ganache address and port 

    chain_info = 'http://127.0.0.1:8545'


- From CLI Compile code

    truffle compile

- From top level directory on the CLI run main.py this will run a series of unit test

    python main.py
    
- if all test run ok you should see

    ----------------------------------------------------------------------
    Ran 4 tests in 7.311s

    OK


### Credits 

"Mastering Ethereum" by Andreas M. Antonopoulos
https://github.com/nastassiasachs/ERC721ExampleDeed/blob/master/contracts/ExampleDeed.sol


### Additional Instructions

Main.py file that serves as my interface.  

Country Clerk class is used to create a contract and interact with it.  
From that contract you can create and change deeds.


Class DeedCreateTest runs the unit test for the following

- creating a deed
- creating two deeds
- creating a deed and changing the owner
- creating a deed, changing the owner and returning account numbers for chain of title