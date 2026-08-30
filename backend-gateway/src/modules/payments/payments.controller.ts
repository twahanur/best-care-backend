import {
  Controller,
  Get,
  Post,
  Body,
  Query,
  Param,
  UseGuards,
  UnauthorizedException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { PaymentsService } from './payments.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { CurrentUser, AuthenticatedUser } from '../../common/security/current-user.decorator';

@ApiTags('Payments & Transactions')
@Controller('payments')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class PaymentsController {
  constructor(private readonly paymentsService: PaymentsService) {}

  @Get()
  @ApiOperation({ summary: 'Get transactions (Customers see own; Admins see all)' })
  findAll(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Query('status') status?: string,
    @Query('search') search?: string,
    @Query('userId') queryUserId?: string,
  ) {
    if (!currentUser) {
      throw new UnauthorizedException('Authentication required');
    }

    // IDOR FIX: Restrict customer to only their own payments
    let effectiveUserId = queryUserId;
    if (currentUser.role !== 'ADMIN') {
      effectiveUserId = currentUser.id;
    }

    return this.paymentsService.findAll({ status, search, userId: effectiveUserId });
  }

  @Post('checkout')
  @ApiOperation({ summary: 'Process payment checkout for booking' })
  create(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Body() body: any,
  ) {
    return this.paymentsService.create({
      ...body,
      userId: currentUser.id,
      customerName: currentUser.name || body.customerName,
    });
  }

  @Post(':id/refund')
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Admin: Process refund for payment transaction' })
  refund(@Param('id') id: string, @Body() body: { reason?: string }) {
    return this.paymentsService.refund(id, body?.reason);
  }

  @Get('stats')
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Admin: Get payment financial analytics' })
  getStats() {
    return this.paymentsService.getPaymentStats();
  }
}
