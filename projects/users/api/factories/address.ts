import { Config } from "../config/config";
import { AddressController } from "../controllers/address";
import { AddressService } from "../services/address";
import { ZipCodeService } from "../services/zipcode";

export function addressControllerFactory(): AddressController {
    const zipcodeService = new ZipCodeService();
    const addressService = new AddressService(
        Config.getDbClient(),
        zipcodeService
    );

    return new AddressController(addressService);
}