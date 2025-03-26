import { PrismaClient } from ".prisma/client";
import { IAddress } from "./address";

export type Role = "USER"|"ADMIN";

export interface IUser {
    id:         number|null;
    email:      string;
    name:       string;
    role:       Role;
    address:    IAddress[]|null;
}

export interface IUserService {
    db: PrismaClient;
    
    listUser(): Promise<IUser[]>;
    createUser(user: Partial<IUser>): Promise<void>;
    updateUser(id: number, user: Partial<IUser>): Promise<void>;
    deleteUser(id: number): Promise<void>;
}