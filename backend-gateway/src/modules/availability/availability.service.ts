import { Injectable, BadRequestException } from '@nestjs/common';
import { AvailabilityBlock, AvailabilityBlockType } from '../../common/types/schema.types';
import { CarsService } from '../cars/cars.service';

@Injectable()
export class AvailabilityService {
  constructor(private readonly carsService: CarsService) {}

  private blocks: AvailabilityBlock[] = [
    {
      id: 'blk_1',
      carId: 'car_hiace_vip',
      carName: 'Toyota HiAce VIP Super Grandia',
      startDate: '2026-09-10T00:00:00Z',
      endDate: '2026-09-12T23:59:59Z',
      type: 'MAINTENANCE',
      notes: 'Scheduled 20,000 km periodic engine and brake overhaul.',
      createdAt: '2026-08-25T00:00:00Z'
    },
    {
      id: 'blk_2',
      carId: 'car_mustang_gt',
      carName: 'Ford Mustang GT V8 Convertible',
      startDate: '2026-09-05T00:00:00Z',
      endDate: '2026-09-06T23:59:59Z',
      type: 'ADMIN_HOLD',
      notes: 'VIP auto salon showroom display booking hold.',
      createdAt: '2026-08-26T00:00:00Z'
    }
  ];

  findAll(carId?: string): AvailabilityBlock[] {
    if (carId) {
      return this.blocks.filter(b => b.carId === carId);
    }
    return this.blocks;
  }

  create(dto: { carId: string; carName?: string; startDate: string; endDate: string; type: AvailabilityBlockType; notes?: string }): AvailabilityBlock {
    const start = new Date(dto.startDate).getTime();
    const end = new Date(dto.endDate).getTime();

    if (start >= end) {
      throw new BadRequestException('End date must be strictly after start date.');
    }

    let carName = dto.carName;
    if (!carName) {
      try {
        const car = this.carsService.findOne(dto.carId);
        carName = car.name;
      } catch {
        carName = 'Fleet Vehicle';
      }
    }

    const newBlock: AvailabilityBlock = {
      id: `blk_${Date.now()}`,
      carId: dto.carId,
      carName: carName || 'Fleet Vehicle',
      startDate: dto.startDate,
      endDate: dto.endDate,
      type: dto.type,
      notes: dto.notes || '',
      createdAt: new Date().toISOString()
    };

    this.blocks.unshift(newBlock);
    return newBlock;
  }

  delete(id: string): { success: boolean } {
    const idx = this.blocks.findIndex(b => b.id === id);
    if (idx !== -1) {
      this.blocks.splice(idx, 1);
    }
    return { success: true };
  }

  checkCollision(carId: string, startDate: string, endDate: string): { available: boolean; conflictingBlock?: AvailabilityBlock } {
    const reqStart = new Date(startDate).getTime();
    const reqEnd = new Date(endDate).getTime();

    const conflict = this.blocks.find(b => {
      if (b.carId !== carId) return false;
      const bStart = new Date(b.startDate).getTime();
      const bEnd = new Date(b.endDate).getTime();

      // Check if ranges overlap
      return reqStart < bEnd && reqEnd > bStart;
    });

    return {
      available: !conflict,
      conflictingBlock: conflict
    };
  }
}
