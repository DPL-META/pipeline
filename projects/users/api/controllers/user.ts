import { type Request, type Response } from "express";
import { IUser, IUserService } from "../interfaces/user";


export class UserController {
    constructor(public userService: IUserService) {}

    async createUser(req: Request<Pick<IUser, "email"|"name"|"role">>, res: Response): Promise<Response> {
        await this.userService.createUser(req.body);

        return res.status(201).json({ message: "created" });
    }

    async listUser(req: Request, res: Response): Promise<Response> {
        const result = await this.userService.listUser();

        return res.status(200).json({ data: result });
    }

    async updateUser(req: Request<Pick<IUser, "id">, any, Partial<IUser>>, res: Response): Promise<Response> {
        await this.userService.updateUser(req.params.id as number, req.body);

        return res.status(200).json({ message: "updated" });
    }

    async deleteUser(req: Request<Pick<IUser, "id">>, res: Response): Promise<Response> {
        await this.userService.deleteUser(req.params.id as number);

        return res.status(200).json({ message: "deleted" });
    }
}