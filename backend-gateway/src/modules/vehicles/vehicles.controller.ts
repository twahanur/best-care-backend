import { Controller, Get, Post, Body, Param, Query, Patch, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { VehiclesService } from './vehicles.service';
import { CreateVehicleDto } from './dto/create-vehicle.dto';
import { FilterVehicleDto } from './dto/filter-vehicle.dto';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('Vehicles')
@Controller('vehicles')
@UseGuards(JwtAuthGuard, RolesGuard)
export class VehiclesController {
  constructor(private readonly vehiclesService: VehiclesService) {}

  @Public()
  @Get()
  @ApiOperation({ summary: 'List and filter vehicles catalog' })
  @ApiResponse({ status: 200, description: 'Filtered list of fleet vehicles' })
  findAll(@Query() filters: FilterVehicleDto) {
    return this.vehiclesService.findAll(filters);
  }

  @Public()
  @Get(':id')
  @ApiOperation({ summary: 'Get vehicle specifications by ID' })
  @ApiResponse({ status: 200, description: 'Vehicle details' })
  @ApiResponse({ status: 404, description: 'Vehicle not found' })
  findOne(@Param('id') id: string) {
    return this.vehiclesService.findOne(id);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post()
  @ApiOperation({ summary: 'Add a new vehicle to fleet (Admin)' })
  @ApiResponse({ status: 201, description: 'Vehicle successfully created' })
  create(@Body() dto: CreateVehicleDto) {
    return this.vehiclesService.create(dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Patch(':id/availability')
  @ApiOperation({ summary: 'Toggle vehicle availability status (Admin)' })
  updateAvailability(@Param('id') id: string, @Body('available') available: boolean) {
    return this.vehiclesService.updateStatus(id, available);
  }
}
