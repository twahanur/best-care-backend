import { Controller, Get, Post, Put, Delete, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { CarsService } from './cars.service';
import { Car } from '../../common/types/schema.types';

@ApiTags('Cars & Fleet Management')
@Controller('cars')
export class CarsController {
  constructor(private readonly carsService: CarsService) {}

  @Get()
  @ApiOperation({ summary: 'Browse and search cars with multi-criteria filters' })
  findAll(
    @Query('category') category?: string,
    @Query('search') search?: string,
    @Query('transmission') transmission?: string,
    @Query('fuelType') fuelType?: string,
    @Query('maxPrice') maxPrice?: number,
    @Query('hub') hub?: string,
    @Query('status') status?: string,
  ) {
    return this.carsService.findAll({ category, search, transmission, fuelType, maxPrice, hub, status });
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get single car details, specs, and rating' })
  findOne(@Param('id') id: string) {
    return this.carsService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Admin: Add a new vehicle to fleet' })
  create(@Body() dto: Partial<Car>) {
    return this.carsService.create(dto);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Admin: Update vehicle details and rates' })
  update(@Param('id') id: string, @Body() dto: Partial<Car>) {
    return this.carsService.update(id, dto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Admin: Delete vehicle from fleet' })
  delete(@Param('id') id: string) {
    return this.carsService.delete(id);
  }
}
