import { Controller, Get, Post, Delete, Body, Query, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { AvailabilityService } from './availability.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('Car Availability & Maintenance')
@Controller('availability')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AvailabilityController {
  constructor(private readonly availabilityService: AvailabilityService) {}

  @Public()
  @Get()
  @ApiOperation({ summary: 'Get all availability and maintenance blocks' })
  findAll(@Query('carId') carId?: string) {
    return this.availabilityService.findAll(carId);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post()
  @ApiOperation({ summary: 'Admin: Schedule maintenance block or date hold' })
  create(@Body() body: any) {
    return this.availabilityService.create(body);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Delete(':id')
  @ApiOperation({ summary: 'Admin: Remove maintenance block or release hold' })
  delete(@Param('id') id: string) {
    return this.availabilityService.delete(id);
  }

  @Public()
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
