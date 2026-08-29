import { Injectable, Logger } from '@nestjs/common';
import { AiProxyService } from '../ai-proxy/ai-proxy.service';
import { LeadInquiryDto } from './dto/lead-inquiry.dto';

export interface AutomationLog {
  id: string;
  workflowName: string;
  triggerEvent: string;
  leadName: string;
  leadScore: number;
  classification: string;
  actionTaken: string;
  webhookStatus: 'SUCCESS' | 'DISPATCHED' | 'QUEUED';
  timestamp: string;
  details: any;
}

@Injectable()
export class AutomationService {
  private readonly logger = new Logger(AutomationService.name);
  private automationLogs: AutomationLog[] = [
    {
      id: 'log_auto_101',
      workflowName: 'AI High-Value Lead Fast-Track',
      triggerEvent: 'booking_inquiry_received',
      leadName: 'Shahriar Khan (Apex Holdings)',
      leadScore: 92,
      classification: 'Hot',
      actionTaken: 'High-priority SMS & CRM task dispatched to VIP Corporate Manager',
      webhookStatus: 'SUCCESS',
      timestamp: '2026-08-28T14:31:12Z',
      details: { estimatedValue: '$815', duration: '5 days', vehicle: 'Toyota Prado TX' }
    },
    {
      id: 'log_auto_102',
      workflowName: 'Automated Booking Confirmation & Spec Sheet Dispatch',
      triggerEvent: 'instant_booking_created',
      leadName: 'Nusrat Jahan (Unilever)',
      leadScore: 88,
      classification: 'Hot',
      actionTaken: 'Automated confirmation email with executive driver contact triggered',
      webhookStatus: 'SUCCESS',
      timestamp: '2026-08-28T09:16:04Z',
      details: { estimatedValue: '$380', duration: '2 days', vehicle: 'Mercedes-Benz E-Class' }
    },
    {
      id: 'log_auto_103',
      workflowName: 'AI Standard Lead Follow-up',
      triggerEvent: 'customer_portal_quote_request',
      leadName: 'Farhan Chowdhury',
      leadScore: 68,
      classification: 'Warm',
      actionTaken: 'Sent automated vehicle specifications & online checkout link',
      webhookStatus: 'SUCCESS',
      timestamp: '2026-08-28T16:46:20Z',
      details: { estimatedValue: '$440', duration: '4 days', vehicle: 'Tesla Model Y' }
    }
  ];

  constructor(private readonly aiProxyService: AiProxyService) {}

  async processLeadAutomation(dto: LeadInquiryDto) {
    this.logger.log(`[Automation Pipeline] Triggering workflow for lead: ${dto.customerName}`);

    // Step 1: AI Lead Qualification via Python AI Microservice
    const aiResult = await this.aiProxyService.qualifyLead(dto);

    // Step 2: Determine Workflow Action based on AI score
    let actionTaken = '';
    let webhookStatus: 'SUCCESS' | 'DISPATCHED' | 'QUEUED' = 'SUCCESS';

    if (aiResult.classification === 'Hot') {
      actionTaken = `VIP Priority Escalation: Triggered instant webhook to Sales Director & SMS alert to Account Executive. SLA: 15 mins.`;
    } else if (aiResult.classification === 'Warm') {
      actionTaken = `Standard Automated Nurture: Dispatched vehicle quotation PDF and personalized itinerary suggestions.`;
    } else {
      actionTaken = `Automated Drip: Queued promotional discount code email and fleet catalog link.`;
    }

    // Step 3: Record Audit Log
    const newLog: AutomationLog = {
      id: `log_auto_${Date.now()}`,
      workflowName: `AI Lead Qualification & Dispatch (${aiResult.classification})`,
      triggerEvent: 'lead_inquiry_received',
      leadName: `${dto.customerName} (${dto.customerEmail})`,
      leadScore: aiResult.lead_score,
      classification: aiResult.classification,
      actionTaken,
      webhookStatus,
      timestamp: new Date().toISOString(),
      details: aiResult
    };

    this.automationLogs.unshift(newLog);

    return {
      success: true,
      message: 'Automation pipeline executed successfully',
      workflowLog: newLog,
      aiAnalysis: aiResult
    };
  }

  getAutomationLogs(): AutomationLog[] {
    return this.automationLogs;
  }
}
