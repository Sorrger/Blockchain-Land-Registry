async function main() {
  const [admin] = await ethers.getSigners();

  const LandRegister = await ethers.getContractFactory("LandRegister");
  const contract = await LandRegister.deploy(admin.address);

  await contract.waitForDeployment();
  console.log("LandRegister deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
