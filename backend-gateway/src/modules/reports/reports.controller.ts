import { Controller, Get, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ReportsService } from './reports.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';

@ApiTags('Analytics & Reports')
@Controller('analytics')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class ReportsController {
  constructor(private readonly reportsService: ReportsService) {}

  @Roles('ADMIN')
  @Get('dashboard')
  @ApiOperation({ summary: 'Admin: Get full executive dashboard telemetry metrics' })
  getDashboard() {
    return this.reportsService.getDashboardMetrics();
  }

  @Roles('ADMIN')
  @Get('top-cars')
  @ApiOperation({ summary: 'Admin: Get ranking of top booked cars' })
  getTopCars() {
    return this.reportsService.getTopBookedCars();
  }
}
