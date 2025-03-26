import { type Request, type Response } from "express";
import { IAddress, IAddressService } from "../interfaces/address";

export class AddressController {
    constructor(public addressService: IAddressService) {}

    async createAddress(req: Request<any, any, Pick<IAddress, "zipcode"|"number"|"userId">>, res: Response): Promise<Response> {
        const { zipcode, number, userId } = req.body;
        await this.addressService.createAddress(zipcode, number, userId);
    
        return res.status(201).json({ message: "created" });
    }

    async deleteAdrees(req: Request<Pick<IAddress, "id">>, res: Response): Promise<Response> {
        await this.addressService.deleteAddress(req.params.id as number);
        
        return res.status(200).json({ message: "deleted" });
    }
}