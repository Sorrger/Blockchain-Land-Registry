import api from "./client";

// Must match app.schemas.ownership.OwnershipCreate
export interface OwnershipCreate {
  property_id: string;
  owner_wallet: string; // Backend expects wallet, not ID
}

export interface OwnershipResponse {
  id: string;
  tx_hash: string;
  tx_status: string;
}

export const createOwnership = async (data: OwnershipCreate): Promise<OwnershipResponse> => {
  const res = await api.post("/ownerships/", data);
  return res.data;
};