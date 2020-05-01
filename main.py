
from solcx import set_solc_version,compile_source, compile_files, link_code, install_solc

from unittest.mock import patch
from io import StringIO
from web3 import Web3, HTTPProvider
import os

import unittest

install_solc('v0.5.5')

set_solc_version('v0.5.5')




def get_contract_interface(input_str, contract_source_code):
    # Solidity Compiler
    max_gas = 5000000
    gas = {'gas': 5000000}
    compiled_sol = compile_files([contract_source_code], \
                                 import_remappings=[
                                     "zeppeling=/Users/shaunhillin/Documents/WebstormProjects/final_project/node_modules/@openzeppelin/"])  # Compiled source code
    key = contract_source_code + ':' + input_str
    contract_interface = compiled_sol[key]

    # web3.py instance ganache
    w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]

    # Instantiate and deploy contract
    ContractDeploy = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    #estimate gas
    deployment_estimate = ContractDeploy.constructor().estimateGas()
    print("deployment estimated gas:",deployment_estimate)
    if deployment_estimate < max_gas:

        # Submit the transaction that deploys the contract
        tx_hash = ContractDeploy.constructor().transact(gas)

        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Create the contract instance with the newly-deployed address
        contract_inst = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )

        return (w3, contract_inst,tx_receipt)
    else:
        print("Your using to much gas bro")

class CountyClerk():
    def __init__(self,contract_path):
        self.w3, self.ci = self.createCountyClerk(contract_path)


    def createCountyClerk(self,path):

        input_str = "CountyClerkRepo"
        cwd = os.getcwd()
        contract_source_path = os.path.join(cwd, path)
        #deploy contract
        w3, contract_inst, receipt = get_contract_interface(input_str, contract_source_path)
        if receipt['status'] == 0:
            print('deployment failed!!!')
        w3.enable_strict_bytes_type_checking()
        #mint new token from contract
        print('County Clerk Contract Deployed')
        #print(w3.eth.getCode(contract_inst.address))
        return w3, contract_inst


    def createNewDeed(self,owner, address):
        i = self.ci.functions.retrieveNextAccount().call()
        token_id = self.w3.eth.accounts[i]
        token_id = int(token_id, 16)
        self.ci.functions.registerDeed(token_id, owner, address).transact()
        owner = self.ci.functions.retrieveDeedOwner(token_id).call()
        address = self.ci.functions.retrieveDeedAddress(token_id).call()
        print("{0} was registered to {1}".format(owner, address))

    def changeDeed(self,owner):

        token_id = self.w3.eth.accounts[0]
        token_id = int(token_id, 16)
        self.ci.functions.changeDeedOwner(token_id, owner).transact()
        owner = self.ci.functions.retrieveDeedOwner(token_id).call()
        address = self.ci.functions.retrieveDeedAddress(token_id).call()
        print("Deed name was changed to {0} at {1}".format(owner, address))

#test class for testing deed creation
class DeedCreateTest(unittest.TestCase):
    def test_new_deed(self):
        path = "/Users/shaunhillin/Documents/WebstormProjects/final_project/contracts/CountyClerkRepo.sol"
        county_clerk = CountyClerk(path)
        expected_out = "Shaun Hillin was registered to 1904 Smith Rd\n"
        with patch('sys.stdout', new=StringIO()) as solidity_out:
            county_clerk.createNewDeed("Shaun Hillin", "1904 Smith Rd")
            self.assertEqual(solidity_out.getvalue(), expected_out)

    #create 2 new deeds
    def test_2_new_deeds(self):
        path = "/Users/shaunhillin/Documents/WebstormProjects/final_project/contracts/CountyClerkRepo.sol"
        county_clerk = CountyClerk(path)
        expected_out = "Shaun Hillin was registered to 1904 Smith Rd\n"
        with patch('sys.stdout', new=StringIO()) as solidity_out:
            county_clerk.createNewDeed("Shaun Hillin", "1904 Smith Rd")
            self.assertEqual(solidity_out.getvalue(), expected_out)
        expected_out = "Tina Hillin was registered to 1904 Jones Rd\n"
        with patch('sys.stdout', new=StringIO()) as solidity_out:
            county_clerk.createNewDeed("Tina Hillin", "1904 Jones Rd")
            self.assertEqual(solidity_out.getvalue(), expected_out)

    # def test_creating_existing_deed_fail(self):
    #     path = "/Users/shaunhillin/Documents/WebstormProjects/final_project/contracts/CountyClerkRepo.sol"
    #     county_clerk = CountyClerk(path)
    #     county_clerk.createNewDeed("Shaun Hillin", "1904 Smith Rd")
    #     with self.assertRaises(Exception):
    #         county_clerk.createNewDeed("Shaun Hillin", "1904 Smith Rd")

    #test to change name on deed
    def test_change_deed(self):
        path = "/Users/shaunhillin/Documents/WebstormProjects/final_project/contracts/CountyClerkRepo.sol"
        county_clerk = CountyClerk(path)
        expected_out = "Shaun Hillin was registered to 1904 Smith Rd\n"
        with patch('sys.stdout', new=StringIO()) as solidity_out:
            county_clerk.createNewDeed("Shaun Hillin", "1904 Smith Rd")
            self.assertEqual(solidity_out.getvalue(), expected_out)
        expected_out = "Deed name was changed to Tina Hillin at 1904 Smith Rd\n"
        with patch('sys.stdout', new=StringIO()) as solidity_out:
            county_clerk.changeDeed("Tina Hillin")
            self.assertEqual(solidity_out.getvalue(), expected_out)


def main():
    unittest.main()



if __name__ == '__main__':
    main()
