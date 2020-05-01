var CountyClerkRepo = artifacts.require("CountyClerkRepo")

module.exports = function(deployer) {
    //  Deploy county Clerk
    deployer.deploy(CountyClerkRepo)
}