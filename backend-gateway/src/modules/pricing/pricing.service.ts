import { Injectable } from '@nestjs/common';
import { PricingRule, ProtectionPlan } from '../../common/types/schema.types';
import { CarsService } from '../cars/cars.service';

@Injectable()
export class PricingService {
  constructor(private readonly carsService: CarsService) {}

  private rules: PricingRule[] = [
    {
      id: 'price_rule_1',
      name: 'Weekend Surge Special',
      category: 'Luxury',
      multiplier: 1.15,
      isActive: true,
      createdAt: '2026-01-01T00:00:00Z'
    },
    {
      id: 'price_rule_2',
      name: 'Long-term 7+ Days Discount',
      multiplier: 0.90, // 10% off
      isActive: true,
      createdAt: '2026-01-01T00:00:00Z'
    }
  ];

  findAll(): PricingRule[] {
    return this.rules;
  }

  create(dto: { name: string; category?: string; multiplier: number; startDate?: string; endDate?: string; isActive?: boolean }): PricingRule {
    const newRule: PricingRule = {
      id: `rule_${Date.now()}`,
      name: dto.name,
      category: dto.category,
      multiplier: Number(dto.multiplier) || 1.0,
      startDate: dto.startDate,
      endDate: dto.endDate,
      isActive: dto.isActive !== undefined ? dto.isActive : true,
      createdAt: new Date().toISOString()
    };

    this.rules.unshift(newRule);
    return newRule;
  }

  delete(id: string): { success: boolean } {
    const idx = this.rules.findIndex(r => r.id === id);
    if (idx !== -1) {
      this.rules.splice(idx, 1);
    }
    return { success: true };
  }

  calculateQuote(carId: string, totalDays: number, plan: ProtectionPlan = 'Comprehensive Plus') {
    const car = this.carsService.findOne(carId);
    let dailyRate = car.dailyRate;

    // Protection fee
    let dailyProtectionFee = 0;
    if (plan === 'Comprehensive Plus') dailyProtectionFee = 18;
    else if (plan === 'VIP Full Shield') dailyProtectionFee = 30;

    let baseTotal = dailyRate * totalDays;
    let discount = 0;

    // Apply long-term discount if >= 7 days
    if (totalDays >= 7) {
      discount = baseTotal * 0.10;
    }

    const protectionTotal = dailyProtectionFee * totalDays;
    const grandTotal = (baseTotal - discount) + protectionTotal;

    return {
      carId: car.id,
      carName: car.name,
      dailyRate,
      totalDays,
      baseTotal,
      discount,
      protectionPlan: plan,
      protectionFee: protectionTotal,
      securityDeposit: car.securityDeposit,
      grandTotal: Math.round(grandTotal),
    };
  }
}
