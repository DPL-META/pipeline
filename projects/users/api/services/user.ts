import { PrismaClient } from ".prisma/client";
import { IUser, IUserService } from "../interfaces/user";

export class UserService  implements IUserService {
    constructor(public db: PrismaClient) {}
    
    async listUser(): Promise<IUser[]> {
        const result = await this.db.user.findMany({});
        
        return result as IUser[];
    }
    
    async createUser(user: Partial<IUser>): Promise<void> {
        await this.db.user.create({
            data: user as any,
        });
    }
    
    async updateUser(id: number, user: Partial<IUser>): Promise<void> {
        await this.db.user.update({
            data: user as any,
            where: { id }
        });
    }
    
    async deleteUser(id: number): Promise<void> {
        await this.db.user.delete({
            where: { id }
        });
    }
}