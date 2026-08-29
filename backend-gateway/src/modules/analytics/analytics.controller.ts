import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AnalyticsService } from './analytics.service';

@ApiTags('Analytics')
@Controller('analytics')
export class AnalyticsController {
  constructor(private readonly analyticsService: AnalyticsService) {}

  @Get('dashboard')
  @ApiOperation({ summary: 'Get aggregated metrics, revenue trends, and fleet distribution for Admin Dashboard' })
  @ApiResponse({ status: 200, description: 'Aggregated analytics payload for dashboard' })
  getDashboardMetrics() {
    return this.analyticsService.getDashboardMetrics();
  }
}
