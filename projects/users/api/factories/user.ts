import { Config } from "../config/config";
import { UserController } from "../controllers/user";
import { UserService } from "../services/user";

export function userControllerFactory(): UserController {
    const userService = new UserService(Config.getDbClient());
    
    return new UserController(userService);
}