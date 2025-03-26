import { PrismaClient } from ".prisma/client";
import { IAddressService } from "../interfaces/address";
import { IZipCodeService } from "../interfaces/zipcode";

export class AddressService implements IAddressService{
    constructor(public db: PrismaClient, public zipcodeService: IZipCodeService) {
        this.db = db;
        this.zipcodeService = zipcodeService;
    }
    
    async createAddress(zipcode: string, number: string, userId: number): Promise<void> {
        const address = await this.zipcodeService.searchAddressByZipcode(zipcode);
        
        await this.db.address.create({
            data: {
                city: address.localidade,
                state: address.estado,
                address: `${address.logradouro}, ${address.bairro}`,
                zipcode: address.cep,
                number: number,
                userId: userId
            },
        });
    }

    async deleteAddress(id: number): Promise<void> {
        await this.db.address.delete({
            where: { id }
        });
    }
}