// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const fs = require("fs");
const hre = require("hardhat");

async function main() {
  // const currentTimestampInSeconds = Math.round(Date.now() / 1000);
  // const unlockTime = currentTimestampInSeconds + 60;
  // const lockedAmount = hre.ethers.parseEther("0.001");

  const digiLocker = await hre.ethers.deployContract("digiLocker");

  await digiLocker.waitForDeployment();

  // const digiLockerContract = await digiLocker.deployed();
  const contractAddress = digiLocker.target;
  const ownerAddress = await hre.ethers.getSigner(contractAddress);

  fs.writeFileSync(
    "./config.js",
    `
    export const contractAddress = "${contractAddress}"
    export const ownerAddress = "${ownerAddress}"
`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
