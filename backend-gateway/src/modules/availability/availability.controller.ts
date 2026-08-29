import { Controller, Get, Post, Delete, Body, Query, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { AvailabilityService } from './availability.service';

@ApiTags('Car Availability & Maintenance')
@Controller('availability')
export class AvailabilityController {
  constructor(private readonly availabilityService: AvailabilityService) {}

  @Get()
  @ApiOperation({ summary: 'Get all availability and maintenance blocks' })
  findAll(@Query('carId') carId?: string) {
    return this.availabilityService.findAll(carId);
  }

  @Post()
  @ApiOperation({ summary: 'Admin: Schedule maintenance block or date hold' })
  create(@Body() body: any) {
    return this.availabilityService.create(body);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Admin: Remove maintenance block or release hold' })
  delete(@Param('id') id: string) {
    return this.availabilityService.delete(id);
  }

  @Get('check')
  @ApiOperation({ summary: 'Check car availability for date range' })
  checkCollision(
    @Query('carId') carId: string,
    @Query('startDate') startDate: string,
    @Query('endDate') endDate: string,
  ) {
    return this.availabilityService.checkCollision(carId, startDate, endDate);
  }
}
