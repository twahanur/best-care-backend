import { Controller, Post, Get, Body } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AutomationService } from './automation.service';
import { LeadInquiryDto } from './dto/lead-inquiry.dto';

@ApiTags('Automation & Webhooks')
@Controller('automation')
export class AutomationController {
  constructor(private readonly automationService: AutomationService) {}

  @Post('webhook/lead')
  @ApiOperation({ summary: 'Trigger AI Lead Qualification & Automated Notification Webhook Pipeline' })
  @ApiResponse({ status: 200, description: 'Workflow processed and audit log generated' })
  triggerLeadWorkflow(@Body() dto: LeadInquiryDto) {
    return this.automationService.processLeadAutomation(dto);
  }

  @Get('logs')
  @ApiOperation({ summary: 'Get real-time Automation Workflow audit logs for Admin Dashboard' })
  @ApiResponse({ status: 200, description: 'List of executed automation logs' })
  getLogs() {
    return this.automationService.getAutomationLogs();
  }

  @Post('test-workflow')
  @ApiOperation({ summary: 'Trigger a quick test of the AI Automation pipeline (Reviewer convenience)' })
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
