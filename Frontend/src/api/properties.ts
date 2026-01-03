import api from "./client";

export interface PropertyCreate {
  kw_id: string;
  metadata_hash: string;
}

export const createProperty = (data: PropertyCreate) =>
  api.post("/properties/", data);

export const getProperty = (id: string) =>
  api.get(`/properties/${id}`);
