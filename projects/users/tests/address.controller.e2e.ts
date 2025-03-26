import request from 'supertest';
import express from 'express';
import { IAddressService } from '../api/interfaces/address';
import { describe, it, expect, jest, beforeEach } from '@jest/globals';
import { AddressController } from '../api/controllers/address';

jest.mock('../api/services/address');

const app = express();
app.use(express.json());

describe('AddressController Integration Tests', () => {
  let mockAddressService: jest.Mocked<IAddressService>;
  let addressController: AddressController;

  beforeEach(() => {
    mockAddressService = {
      createAddress: jest.fn(),
      deleteAddress: jest.fn(),
    };

    addressController = new AddressController(mockAddressService);
    app.post('/addresses', (req, res) => addressController.createAddress(req, res));
    app.delete('/addresses/:id', (req, res) => addressController.deleteAdrees(req, res));
  });

  it('should create an address and return status 201', async () => {
    const mockAddressData = {
      zipcode: '12345-678',
      number: '10',
      userId: 1,
    };

    mockAddressService.createAddress.mockResolvedValue(undefined);

    const response = await request(app)
      .post('/addresses')
      .send(mockAddressData);

    expect(response.status).toBe(201);
    expect(response.body.message).toBe('created');
    expect(mockAddressService.createAddress).toHaveBeenCalledWith('12345-678', '10', 1);
  });
});
