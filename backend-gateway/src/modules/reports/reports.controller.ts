import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { ReportsService } from './reports.service';

@ApiTags('Analytics & Reports')
@Controller('analytics')
export class ReportsController {
  constructor(private readonly reportsService: ReportsService) {}

  @Get('dashboard')
  @ApiOperation({ summary: 'Get full executive dashboard telemetry metrics' })
  getDashboard() {
    return this.reportsService.getDashboardMetrics();
  }

  @Get('top-cars')
  @ApiOperation({ summary: 'Get ranking of top booked cars' })
  getTopCars() {
    return this.reportsService.getTopBookedCars();
  }
}
