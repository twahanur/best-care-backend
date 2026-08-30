import { Controller, Get, Post, Delete, Body, Query, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { PricingService } from './pricing.service';
import { DiscountCoupon } from '../../common/types/schema.types';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('Pricing & Rules Management')
@Controller('pricing')
@UseGuards(JwtAuthGuard, RolesGuard)
export class PricingController {
  constructor(private readonly pricingService: PricingService) {}

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Get('rules')
  @ApiOperation({ summary: 'Admin: Get all dynamic pricing rules' })
  findAll() {
    return this.pricingService.findAll();
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post('rules')
  @ApiOperation({ summary: 'Admin: Create new dynamic pricing rule' })
  create(@Body() body: any) {
    return this.pricingService.create(body);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Delete('rules/:id')
  @ApiOperation({ summary: 'Admin: Delete pricing rule' })
  delete(@Param('id') id: string) {
    return this.pricingService.delete(id);
  }

  @Public()
  @Get('coupons')
  @ApiOperation({ summary: 'Get all active promo discount coupons' })
  findAllCoupons() {
    return this.pricingService.findAllCoupons();
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post('coupons')
  @ApiOperation({ summary: 'Admin: Create new discount coupon' })
  createCoupon(@Body() dto: Partial<DiscountCoupon>) {
    return this.pricingService.createCoupon(dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Delete('coupons/:id')
  @ApiOperation({ summary: 'Admin: Delete or expire coupon' })
  deleteCoupon(@Param('id') id: string) {
    return this.pricingService.deleteCoupon(id);
  }

  @Public()
  @Get('protection-plans')
  @ApiOperation({ summary: 'Get all protection and insurance plan tiers' })
  getProtectionPlans() {
    return this.pricingService.getProtectionPlans();
  }

  @Public()
  @Get('quote')
  @ApiOperation({ summary: 'Calculate accurate rental quote with protection & discount' })
  calculateQuote(
    @Query('carId') carId: string,
    @Query('totalDays') totalDays: number,
    @Query('plan') plan?: any,
    @Query('withDriver') withDriver?: boolean,
  ) {
    return this.pricingService.calculateQuote(carId, Number(totalDays) || 1, plan, Boolean(withDriver));
  }
}
