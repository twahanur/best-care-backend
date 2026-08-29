import { Controller, Get, Post, Put, Body, Query, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PaymentsService } from './payments.service';

@ApiTags('Payments & Transactions')
@Controller('payments')
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @Get()
  @ApiOperation({ summary: 'Get all payments and transaction records' })
  findAll(
    @Query('status') status?: string,
    @Query('search') search?: string,
    @Query('userId') userId?: string,
  ) {
    return this.paymentsService.findAll({ status, search, userId });
  }

  @Post('checkout')
  @ApiOperation({ summary: 'Process payment checkout for booking' })
  create(@Body() body: any) {
    return this.paymentsService.create(body);
  }

  @Post(':id/refund')
  @ApiOperation({ summary: 'Process refund for payment transaction' })
  refund(@Param('id') id: string, @Body() body: { reason?: string }) {
    return this.paymentsService.refund(id, body?.reason);
  }

  @Get('stats')
  @ApiOperation({ summary: 'Get payment financial analytics' })
  getStats() {
    return this.paymentsService.getPaymentStats();
  }
}
