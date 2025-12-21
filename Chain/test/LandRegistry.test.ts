import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { expect } from "chai";
import { ethers } from "hardhat";

describe("LandRegister", function () {
  async function deployLandRegisterFixture() {
    const [admin, notary, user1, user2] = await ethers.getSigners();

    const LandRegister = await ethers.getContractFactory("LandRegister");
    const contract = await LandRegister.deploy(admin.address);

    const NOTARY_ROLE = await contract.NOTARY_ROLE();
    const DEFAULT_ADMIN_ROLE = await contract.DEFAULT_ADMIN_ROLE();

    await contract.connect(admin).addNotary(notary.address);

    return { 
      contract, 
      admin, 
      notary, 
      user1, 
      user2, 
      NOTARY_ROLE, 
      DEFAULT_ADMIN_ROLE 
    };
  }

  describe("Deployment & Access Control", function () {
    it("Should set the right admin", async function () {
      const { contract, admin, DEFAULT_ADMIN_ROLE } = await loadFixture(deployLandRegisterFixture);
      expect(await contract.hasRole(DEFAULT_ADMIN_ROLE, admin.address)).to.be.true;
    });

    it("Admin can add a notary", async function () {
      const { contract, notary, NOTARY_ROLE } = await loadFixture(deployLandRegisterFixture);
      expect(await contract.hasRole(NOTARY_ROLE, notary.address)).to.be.true;
    });

    it("Non-admin cannot add a notary", async function () {
      const { contract, user1, user2, DEFAULT_ADMIN_ROLE } = await loadFixture(deployLandRegisterFixture);
      
      await expect(
        contract.connect(user1).addNotary(user2.address)
      ).to.be.revertedWithCustomError(contract, "AccessControlUnauthorizedAccount")
       .withArgs(user1.address, DEFAULT_ADMIN_ROLE);
    });
  });

  describe("Registering Property", function () {
    it("Notary can register a new property", async function () {
      const { contract, notary, user1 } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("doc-ipfs"));

      await expect(contract.connect(notary).registerProperty("KW123", hash, user1.address))
        .to.emit(contract, "PropertyRegistered")
        .withArgs("KW123", user1.address, hash);

      const prop = await contract.getProperty("KW123");
      expect(prop.owner).to.equal(user1.address);
      expect(prop.dataHash).to.equal(hash);
    });

    it("Should fail if Property ID already exists", async function () {
      const { contract, notary, user1 } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("doc"));

      await contract.connect(notary).registerProperty("KW123", hash, user1.address);

      await expect(
        contract.connect(notary).registerProperty("KW123", hash, user1.address)
      ).to.be.revertedWith("Property exists");
    });

    it("Non-notary cannot register property", async function () {
      const { contract, user1, user2, NOTARY_ROLE } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("test"));

      await expect(
        contract.connect(user1).registerProperty("KW999", hash, user2.address)
      ).to.be.revertedWithCustomError(contract, "AccessControlUnauthorizedAccount")
       .withArgs(user1.address, NOTARY_ROLE);
    });
  });

  describe("Transferring Property", function () {
    it("Notary can transfer property", async function () {
      const { contract, notary, user1, user2 } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("doc"));
      
      await contract.connect(notary).registerProperty("KW100", hash, user1.address);

      await expect(contract.connect(notary).transferProperty("KW100", user2.address))
        .to.emit(contract, "PropertyTransferred")
        .withArgs("KW100", user1.address, user2.address);

      const prop = await contract.getProperty("KW100");
      expect(prop.owner).to.equal(user2.address);
    });

    it("Should fail if property does not exist", async function () {
      const { contract, notary, user1 } = await loadFixture(deployLandRegisterFixture);
      
      await expect(
        contract.connect(notary).transferProperty("NON_EXISTENT", user1.address)
      ).to.be.revertedWith("Not found");
    });

    it("Non-notary cannot transfer property", async function () {
      const { contract, notary, user1, user2, NOTARY_ROLE } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("doc"));
      await contract.connect(notary).registerProperty("KW100", hash, user1.address);

      await expect(
        contract.connect(user1).transferProperty("KW100", user2.address)
      ).to.be.revertedWithCustomError(contract, "AccessControlUnauthorizedAccount")
       .withArgs(user1.address, NOTARY_ROLE);
    });
  });

  describe("Updating Property Data", function () {
    it("Notary can update property data", async function () {
      const { contract, notary, user1 } = await loadFixture(deployLandRegisterFixture);
      const oldHash = ethers.keccak256(ethers.toUtf8Bytes("old"));
      const newHash = ethers.keccak256(ethers.toUtf8Bytes("new"));

      await contract.connect(notary).registerProperty("KW555", oldHash, user1.address);

      await expect(contract.connect(notary).updatePropertyData("KW555", newHash))
        .to.emit(contract, "PropertyUpdated")
        .withArgs("KW555", newHash);

      const prop = await contract.getProperty("KW555");
      expect(prop.dataHash).to.equal(newHash);
    });

    it("Should fail if property does not exist", async function () {
      const { contract, notary } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("new"));

      await expect(
        contract.connect(notary).updatePropertyData("NON_EXISTENT", hash)
      ).to.be.revertedWith("Not found");
    });

    it("Non-notary cannot update property", async function () {
      const { contract, notary, user1, NOTARY_ROLE } = await loadFixture(deployLandRegisterFixture);
      const hash = ethers.keccak256(ethers.toUtf8Bytes("data"));
      await contract.connect(notary).registerProperty("KW555", hash, user1.address);

      await expect(
        contract.connect(user1).updatePropertyData("KW555", hash)
      ).to.be.revertedWithCustomError(contract, "AccessControlUnauthorizedAccount")
       .withArgs(user1.address, NOTARY_ROLE);
    });
  });

  describe("View Functions", function () {
    it("Should revert when getting a non-existent property", async function () {
      const { contract } = await loadFixture(deployLandRegisterFixture);
      await expect(contract.getProperty("404")).to.be.revertedWith("Not found");
    });
  });
});
