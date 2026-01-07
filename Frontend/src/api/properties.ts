import api from "./client";

export interface Property {
  id: string;
  property_number: string;
  address: string;
  area: number;
  is_onchain: boolean;
  contract_address?: string;
  token_id?: number;
}

// Must match app.schemas.property.PropertyCreate
export interface PropertyCreate {
  property_number: string;
  address: string;
  area: number;
}

export const createProperty = async (data: PropertyCreate): Promise<Property> => {
  const res = await api.post("/properties/", data);
  return res.data;
};

export const getProperties = async (): Promise<Property[]> => {
  const res = await api.get("/properties/");
  return res.data;
};

export const getProperty = async (id: string): Promise<Property> => {
  const res = await api.get(`/properties/${id}`);
  return res.data;
};