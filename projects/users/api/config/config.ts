import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export class Config {
    public static prisma: PrismaClient|null = null;

    static getDbClient(): PrismaClient {
        if (!Config.prisma) {
            Config.prisma = new PrismaClient();
        }

        return Config.prisma;
    }
}

