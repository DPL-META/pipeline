import { PrismaClient } from ".prisma/client";

export interface IAddress {
    id:          number|null;
    city:        string;
    state:       string;
    address:     string;
    zipcode:     string;
    number:      string;
    userId:      number;    
    createdAt:   Date|null;  
    updatedAt:   Date|null;
}

export interface IAddressService {
    db: PrismaClient;

    createAddress(zipcode: string, number: string, userId: number): Promise<void>
    deleteAddress(id: number): Promise<void>
}