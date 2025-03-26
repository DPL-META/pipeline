import { PrismaClient } from '.prisma/client';
import { IZipCodeService } from '../api/interfaces/zipcode';
import { AddressService } from '../api/services/address';
import { describe, it, beforeAll, expect, afterAll } from '@jest/globals';

const prisma = new PrismaClient();

class MockZipCodeService implements IZipCodeService {
  async searchAddressByZipcode(zipcode: string) {
    return {
      logradouro: 'Rua Teste',
      bairro: 'Bairro Teste',
      localidade: 'Cidade Teste',
      estado: 'Estado Teste',
      cep: zipcode,
    };
  }
}

describe('Test: AddressService', () => {
  let addressService: AddressService;
  
  beforeAll(async () => {
    await prisma.$connect();
    addressService = new AddressService(prisma, new MockZipCodeService());
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it('should create an address in the database', async () => {
    const userId = 1;
    const zipcode = '12345-678';
    const number = '10';

    await addressService.createAddress(zipcode, number, userId);

    const createdAddress = await prisma.address.findFirst({
      where: { userId, zipcode },
    });

    expect(createdAddress).toBeDefined();
    expect(createdAddress?.city).toBe('Cidade Teste');
    expect(createdAddress?.state).toBe('Estado Teste');
    expect(createdAddress?.address).toBe('Rua Teste, Bairro Teste');
    expect(createdAddress?.zipcode).toBe(zipcode);
    expect(createdAddress?.number).toBe(number);
  });

  it('should delete an address from the database', async () => {
    const addressToDelete = await prisma.address.create({
      data: {
        city: 'Cidade Teste',
        state: 'Estado Teste',
        address: 'Rua Teste, Bairro Teste',
        zipcode: '12345-678',
        number: '10',
        userId: 1,
      },
    });

    await addressService.deleteAddress(addressToDelete.id);

    const deletedAddress = await prisma.address.findUnique({
      where: { id: addressToDelete.id },
    });

    expect(deletedAddress).toBeNull();
  });
});