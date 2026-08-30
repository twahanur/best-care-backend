import { Controller, Get, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { AnalyticsService } from './analytics.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';

@ApiTags('Analytics')
@Controller('analytics')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class AnalyticsController {
  constructor(private readonly analyticsService: AnalyticsService) {}

  @Roles('ADMIN')
  @Get('dashboard')
  @ApiOperation({ summary: 'Admin: Get aggregated metrics, revenue trends, and fleet distribution for Admin Dashboard' })
  @ApiResponse({ status: 200, description: 'Aggregated analytics payload for dashboard' })
  getDashboardMetrics() {
    return this.analyticsService.getDashboardMetrics();
  }
}
