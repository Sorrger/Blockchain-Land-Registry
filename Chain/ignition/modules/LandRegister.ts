import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("LandRegisterModule", (m) => {
  const admin = m.getParameter(
    "admin",
    "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
  );

  const landRegister = m.contract("LandRegister", [admin]);

  return { landRegister };
});
