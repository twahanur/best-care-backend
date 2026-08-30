import { Controller, Post, Get, Body, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { AutomationService } from './automation.service';
import { LeadInquiryDto } from './dto/lead-inquiry.dto';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('Automation & Webhooks')
@Controller('automation')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AutomationController {
  constructor(private readonly automationService: AutomationService) {}

  @Public()
  @Post('webhook/lead')
  @ApiOperation({ summary: 'Trigger AI Lead Qualification & Automated Notification Webhook Pipeline' })
  @ApiResponse({ status: 200, description: 'Workflow processed and audit log generated' })
  triggerLeadWorkflow(@Body() dto: LeadInquiryDto) {
    return this.automationService.processLeadAutomation(dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Get('logs')
  @ApiOperation({ summary: 'Get real-time Automation Workflow audit logs for Admin Dashboard' })
  @ApiResponse({ status: 200, description: 'List of executed automation logs' })
  getLogs() {
    return this.automationService.getAutomationLogs();
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post('test-workflow')
  @ApiOperation({ summary: 'Trigger a quick test of the AI Automation pipeline (Admin only)' })
  testWorkflow() {
    return this.automationService.processLeadAutomation({
      customerName: 'Arafat Rahman (Square Pharma)',
      customerEmail: 'arafat.r@squarepharma.com',
      customerPhone: '+8801700998877',
      vehicleCategory: 'Luxury SUV',
      totalDays: 7,
      estimatedBudget: 1200,
      tripPurpose: 'Annual Regional Leadership Summit',
      notes: 'Need 2 luxury SUVs with VIP protection plan and English-speaking drivers.',
      isCorporate: true
    });
  }
}
