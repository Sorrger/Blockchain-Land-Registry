// Chain/scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const LandRegister = await hre.ethers.getContractFactory("LandRegister");
  
  // Deploying with Account #0 (The Admin)
  const [admin] = await hre.ethers.getSigners();
  const landRegister = await LandRegister.deploy(admin.address);

  await landRegister.waitForDeployment();

  const address = await landRegister.getAddress();
  console.log("LandRegister deployed to:", address);

  // Grant Account #1 (The Notary) the NOTARY_ROLE
  // We use Account #1 from your hardhat list: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
  const notaryAddress = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8";
  const NOTARY_ROLE = await landRegister.NOTARY_ROLE();
  await landRegister.grantRole(NOTARY_ROLE, notaryAddress);
  
  console.log(`Notary Role granted to: ${notaryAddress}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});