import api from "./client";

export interface OwnershipCreate {
  property_id: string;
  owner_id: string;
  tx_hash: string;
}

export const createOwnership = (data: OwnershipCreate) =>
  api.post("/ownerships/", data);
