import api from "./client";

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email?: string;
  pesel: string;
  wallet_address: string;
}

export interface UserCreate {
  first_name: string;
  last_name: string;
  email?: string;
  pesel: string;
  wallet_address: string;
}

export const getUsers = async (): Promise<User[]> => {
  const res = await api.get("/users");
  return res.data;
};

export const createUser = async (data: UserCreate): Promise<User> => {
  const res = await api.post("/users", data);
  return res.data;
};
