import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { CarsService } from './cars.service';
import { Car } from '../../common/types/schema.types';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('Cars & Fleet Management')
@Controller('cars')
@UseGuards(JwtAuthGuard, RolesGuard)
export class CarsController {
  constructor(private readonly carsService: CarsService) {}

  @Public()
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

  @Public()
  @Get('categories/stats')
  @ApiOperation({ summary: 'Get category distribution, car counts, and rates' })
  getCategoriesStats() {
    return this.carsService.getCategoriesStats();
  }

  @Public()
  @Get('brands/stats')
  @ApiOperation({ summary: 'Get brand statistics and market share' })
  getBrandsStats() {
    return this.carsService.getBrandsStats();
  }

  @Public()
  @Get('hubs/all')
  @ApiOperation({ summary: 'Get all airport and downtown hub locations' })
  getHubs() {
    return this.carsService.getHubs();
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Get('maintenance/list')
  @ApiOperation({ summary: 'Admin: Get all vehicles currently in maintenance' })
  getMaintenanceFleet() {
    return this.carsService.getMaintenanceFleet();
  }

  @Roles('ADMIN', 'CAR_DRIVER')
  @ApiBearerAuth()
  @Get('owner/:ownerId')
  @ApiOperation({ summary: 'Get vehicles owned or assigned to specific driver' })
  getOwnerCars(@Param('ownerId') ownerId: string) {
    return this.carsService.getOwnerCars(ownerId);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post(':id/transfer-hub')
  @ApiOperation({ summary: 'Admin: Relocate vehicle to another hub' })
  transferCarHub(@Param('id') id: string, @Body('targetHub') targetHub: string) {
    return this.carsService.transferCarHub(id, targetHub);
  }

  @Public()
  @Get(':id')
  @ApiOperation({ summary: 'Get single car details, specs, and rating' })
  findOne(@Param('id') id: string) {
    return this.carsService.findOne(id);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post()
  @ApiOperation({ summary: 'Admin: Add a new vehicle to fleet' })
  create(@Body() dto: Partial<Car>) {
    return this.carsService.create(dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Put(':id')
  @ApiOperation({ summary: 'Admin: Update vehicle details and rates' })
  update(@Param('id') id: string, @Body() dto: Partial<Car>) {
    return this.carsService.update(id, dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Delete(':id')
  @ApiOperation({ summary: 'Admin: Delete vehicle from fleet' })
  delete(@Param('id') id: string) {
    return this.carsService.delete(id);
  }
}
