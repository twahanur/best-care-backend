import { Controller, Get, Post, Delete, Body, Query, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PricingService } from './pricing.service';

@ApiTags('Pricing & Rules Management')
@Controller('pricing')
export class PricingController {
  constructor(private readonly pricingService: PricingService) {}

  @Get('rules')
  @ApiOperation({ summary: 'Admin: Get all dynamic pricing rules' })
  findAll() {
    return this.pricingService.findAll();
  }

  @Post('rules')
  @ApiOperation({ summary: 'Admin: Create new dynamic pricing rule' })
  create(@Body() body: any) {
    return this.pricingService.create(body);
  }

  @Delete('rules/:id')
  @ApiOperation({ summary: 'Admin: Delete pricing rule' })
  delete(@Param('id') id: string) {
    return this.pricingService.delete(id);
  }

  @Get('quote')
  @ApiOperation({ summary: 'Calculate accurate rental quote with protection & discount' })
  calculateQuote(
    @Query('carId') carId: string,
    @Query('totalDays') totalDays: number,
    @Query('plan') plan?: any,
  ) {
    return this.pricingService.calculateQuote(carId, Number(totalDays) || 1, plan);
  }
}
