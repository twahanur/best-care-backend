import { Injectable } from '@nestjs/common';
import { PricingRule, ProtectionPlan, DiscountCoupon } from '../../common/types/schema.types';
import { CarsService } from '../cars/cars.service';

@Injectable()
export class PricingService {
  constructor(private readonly carsService: CarsService) {}

  private rules: PricingRule[] = [
    {
      id: 'price_rule_1',
      name: 'Weekend Surge Special',
      code: 'WEEKEND_SURGE',
      category: 'Luxury',
      multiplier: 1.15,
      driverDailyRate: 35,
      isActive: true,
      createdAt: '2026-01-01T00:00:00Z'
    },
    {
      id: 'price_rule_2',
      name: 'Long-term 7+ Days Discount',
      code: 'LONG_TERM_7',
      multiplier: 0.90, // 10% off
      driverDailyRate: 30,
      isActive: true,
      createdAt: '2026-01-01T00:00:00Z'
    },
    {
      id: 'price_rule_3',
      name: 'Airport Hub Priority Rate',
      code: 'AIRPORT_HUB',
      multiplier: 1.05,
      driverDailyRate: 40,
      isActive: true,
      createdAt: '2026-02-01T00:00:00Z'
    }
  ];

  private coupons: DiscountCoupon[] = [
    {
      id: 'cpn_1',
      code: 'WEEKEND20',
      discountType: 'PERCENTAGE',
      discountValue: 20,
      minBookingAmount: 150,
      maxDiscountAmount: 100,
      startDate: '2026-01-01T00:00:00Z',
      endDate: '2026-12-31T23:59:59Z',
      usageLimit: 500,
      usedCount: 240,
      isActive: true,
      createdAt: '2026-01-01T00:00:00Z'
    },
    {
      id: 'cpn_2',
      code: 'AIRPORTVIP',
      discountType: 'FIXED_AMOUNT',
      discountValue: 25,
      minBookingAmount: 100,
      startDate: '2026-01-01T00:00:00Z',
      endDate: '2026-12-31T23:59:59Z',
      usageLimit: 300,
      usedCount: 185,
      isActive: true,
      createdAt: '2026-01-10T00:00:00Z'
    },
    {
      id: 'cpn_3',
      code: 'TESLAFUTURE',
      discountType: 'PERCENTAGE',
      discountValue: 15,
      minBookingAmount: 200,
      startDate: '2026-02-01T00:00:00Z',
      endDate: '2026-12-31T23:59:59Z',
      usageLimit: 200,
      usedCount: 92,
      isActive: true,
      createdAt: '2026-02-01T00:00:00Z'
    }
  ];

  findAll(): PricingRule[] {
    return this.rules;
  }

  create(dto: { name: string; code?: string; category?: string; multiplier: number; driverDailyRate?: number; startDate?: string; endDate?: string; isActive?: boolean }): PricingRule {
    const newRule: PricingRule = {
      id: `rule_${Date.now()}`,
      name: dto.name,
      code: dto.code || `RULE_${Date.now().toString().slice(-4)}`,
      category: dto.category,
      multiplier: Number(dto.multiplier) || 1.0,
      driverDailyRate: Number(dto.driverDailyRate) || 30,
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

  findAllCoupons(): DiscountCoupon[] {
    return this.coupons;
  }

  createCoupon(dto: Partial<DiscountCoupon>): DiscountCoupon {
    const newCoupon: DiscountCoupon = {
      id: `cpn_${Date.now()}`,
      code: (dto.code || `SAVE${Math.floor(10 + Math.random() * 90)}`).toUpperCase(),
      discountType: dto.discountType || 'PERCENTAGE',
      discountValue: Number(dto.discountValue) || 10,
      minBookingAmount: Number(dto.minBookingAmount) || 0,
      maxDiscountAmount: dto.maxDiscountAmount ? Number(dto.maxDiscountAmount) : undefined,
      startDate: dto.startDate || new Date().toISOString(),
      endDate: dto.endDate || '2026-12-31T23:59:59Z',
      usageLimit: Number(dto.usageLimit) || 100,
      usedCount: 0,
      isActive: dto.isActive !== undefined ? dto.isActive : true,
      createdAt: new Date().toISOString()
    };
    this.coupons.unshift(newCoupon);
    return newCoupon;
  }

  deleteCoupon(id: string): { success: boolean } {
    const idx = this.coupons.findIndex(c => c.id === id || c.code === id);
    if (idx !== -1) {
      this.coupons.splice(idx, 1);
    }
    return { success: true };
  }

  getProtectionPlans() {
    return [
      {
        id: 'plan_basic',
        name: 'Basic CDW',
        dailyFee: 0,
        deductible: 500,
        coverage: 'Standard Collision Damage Waiver with $500 deductible. Covers third-party liability and basic vehicle exterior.',
        features: ['Third-party liability', '24/7 Roadside Assistance', '$500 Security Deposit']
      },
      {
        id: 'plan_comp',
        name: 'Comprehensive Plus',
        dailyFee: 18,
        deductible: 150,
        coverage: 'Full glass, tyre, scratch & collision protection. Low $150 deductible.',
        features: ['Zero Glass & Tyre Liability', 'Theft Protection', 'Emergency Medical Coverage', 'Fast Track Claims']
      },
      {
        id: 'plan_vip',
        name: 'VIP Full Shield',
        dailyFee: 30,
        deductible: 0,
        coverage: 'Zero deductible VIP coverage. Comprehensive roadside concierge, instant replacement vehicle.',
        features: ['0% Deductible', 'Instant Replacement Guarantee', 'Personal Effects Protection', 'Priority Concierge']
      }
    ];
  }

  calculateQuote(carId: string, totalDays: number, plan: ProtectionPlan = 'Comprehensive Plus', withDriver: boolean = false) {
    const car = this.carsService.findOne(carId);
    let dailyRate = car.dailyRate;

    // Protection fee
    let dailyProtectionFee = 0;
    if (plan === 'Comprehensive Plus') dailyProtectionFee = 18;
    else if (plan === 'VIP Full Shield') dailyProtectionFee = 30;

    let baseTotal = dailyRate * totalDays;
    let driverFee = withDriver ? 30 * totalDays : 0;
    let discount = 0;

    // Apply long-term discount if >= 7 days
    if (totalDays >= 7) {
      discount = baseTotal * 0.10;
    }

    const protectionTotal = dailyProtectionFee * totalDays;
    const grandTotal = (baseTotal - discount) + protectionTotal + driverFee;

    return {
      carId: car.id,
      carName: car.name,
      dailyRate,
      totalDays,
      baseTotal,
      driverFee,
      discount,
      protectionPlan: plan,
      protectionFee: protectionTotal,
      securityDeposit: car.securityDeposit,
      grandTotal: Math.round(grandTotal),
    };
  }
}
