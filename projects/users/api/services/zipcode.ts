import { IZipCodeService, ViaCepAddress } from "../interfaces/zipcode";
import axios, { AxiosInstance } from "axios";

export class ZipCodeService implements IZipCodeService {
    public readonly api: AxiosInstance;
    
    constructor() {
        this.api = axios.create({
            baseURL: process.env.ZIPCODE_API
        });
    }

    async searchAddressByZipcode(zipcode: string): Promise<ViaCepAddress> {
        const response = await this.api.get(`/ws/${zipcode}/json`);

        return response.data;
    }
}