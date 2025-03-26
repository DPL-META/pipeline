import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {
    const user = await prisma.user.upsert({
      where: { email: 'jhon.doe@aiqfome.com' },
      update: {},
      create: {
        email: 'jhon.doe@aiqfome.com',
        name: 'Jhon Doe',
        role: "ADMIN"
      },
    })
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })