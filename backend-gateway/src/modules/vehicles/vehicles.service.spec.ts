import { Test, TestingModule } from '@nestjs/testing';
import { VehiclesService } from './vehicles.service';

describe('VehiclesService', () => {
  let service: VehiclesService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [VehiclesService],
    }).compile();

    service = module.get<VehiclesService>(VehiclesService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should return all seed vehicles', () => {
    const vehicles = service.findAll();
    expect(vehicles.length).toBeGreaterThanOrEqual(8);
  });

  it('should filter vehicles by category', () => {
    const suvs = service.findAll({ category: 'SUV' });
    expect(suvs.length).toBeGreaterThanOrEqual(1);
    expect(suvs.every(v => v.category === 'SUV')).toBe(true);
  });

  it('should find vehicle by ID', () => {
    const vehicle = service.findOne('car_prado_suv');
    expect(vehicle).toBeDefined();
    expect(vehicle.name).toContain('Prado');
  });
});
