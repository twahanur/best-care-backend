import {
  Controller,
  Get,
  Post,
  Put,
  Body,
  Param,
  Query,
  UseGuards,
  ForbiddenException,
  UnauthorizedException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { BookingsService } from './bookings.service';
import { BookingStatus } from '../../common/types/schema.types';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { CurrentUser, AuthenticatedUser } from '../../common/security/current-user.decorator';

@ApiTags('Bookings & Reservations')
@Controller('bookings')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class BookingsController {
  constructor(private readonly bookingsService: BookingsService) {}

  @Get()
  @ApiOperation({ summary: 'Get bookings (Customers see only own; Admins see all)' })
  findAll(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Query('status') status?: string,
    @Query('search') search?: string,
    @Query('userId') queryUserId?: string,
  ) {
    if (!currentUser) {
      throw new UnauthorizedException('Authentication required');
    }

    // IDOR FIX: If regular customer, always restrict to own userId
    let effectiveUserId = queryUserId;
    if (currentUser.role !== 'ADMIN') {
      effectiveUserId = currentUser.id;
    }

    return this.bookingsService.findAll(status, search, effectiveUserId);
  }

  @Get('driver/:driverId')
  @Roles('CAR_DRIVER', 'ADMIN')
  @ApiOperation({ summary: 'Get all trip requests and assignments for driver' })
  getDriverBookings(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Param('driverId') driverId: string,
  ) {
    if (currentUser.role !== 'ADMIN' && currentUser.id !== driverId) {
      throw new ForbiddenException('You can only view your own driver trip assignments.');
    }
    return this.bookingsService.getDriverBookings(driverId);
  }

  @Post(':id/driver-response')
  @Roles('CAR_DRIVER', 'ADMIN')
  @ApiOperation({ summary: 'Driver Accept or Reject trip request' })
  driverRespond(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Param('id') id: string,
    @Body('driverId') driverId: string,
    @Body('action') action: 'ACCEPT' | 'REJECT',
  ) {
    const effectiveDriverId = currentUser.role === 'ADMIN' ? (driverId || currentUser.id) : currentUser.id;
    return this.bookingsService.driverRespondToTrip(id, effectiveDriverId, action);
  }

  @Post(':id/driver-status')
  @Roles('CAR_DRIVER', 'ADMIN')
  @ApiOperation({ summary: 'Driver update trip lifecycle status' })
  updateDriverStatus(
    @Param('id') id: string,
    @Body('status') status: any,
  ) {
    return this.bookingsService.updateDriverTripStatus(id, status);
  }

  @Get('customer/:userId')
  @ApiOperation({ summary: 'Get customer trip history and active rentals' })
  getCustomerBookings(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Param('userId') userId: string,
  ) {
    // IDOR FIX: verify user is viewing their own bookings or is ADMIN
    if (currentUser.role !== 'ADMIN' && currentUser.id !== userId) {
      throw new ForbiddenException('You are not authorized to view another user\'s booking history.');
    }
    return this.bookingsService.getCustomerBookings(userId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get booking details by ID or code' })
  findOne(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Param('id') id: string,
  ) {
    const booking = this.bookingsService.findOne(id);
    // IDOR FIX: Check ownership
    if (
      currentUser.role !== 'ADMIN' &&
      booking.userId !== currentUser.id &&
      booking.driverId !== currentUser.id
    ) {
      throw new ForbiddenException('Access denied: You are not authorized to view this booking.');
    }
    return booking;
  }

  @Post()
  @ApiOperation({ summary: 'Create a new car rental reservation' })
  create(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Body() body: any,
  ) {
    // Force authenticated user ID and credentials onto booking
    const payload = {
      ...body,
      userId: currentUser.id,
      customerEmail: currentUser.email,
      customerName: currentUser.name || body.customerName,
    };
    return this.bookingsService.create(payload);
  }

  @Post('pos')
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Create instant POS walk-in counter order (Admin/Staff only)' })
  createPos(@Body() body: any) {
    return this.bookingsService.createPosBooking(body);
  }

  @Put(':id/status')
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Update booking status lifecycle (Admin only)' })
  updateStatus(@Param('id') id: string, @Body() body: { status: BookingStatus }) {
    return this.bookingsService.updateStatus(id, body.status);
  }

  @Post(':id/return-inspection')
  @Roles('ADMIN', 'CAR_DRIVER')
  @ApiOperation({ summary: 'Complete rental dropoff return and inspection' })
  processReturn(
    @Param('id') id: string,
    @Body() body: { returnOdometer: number; returnFuelLevel: number; returnDamageNotes?: string; extraCharges?: number },
  ) {
    return this.bookingsService.processRentalReturn(id, body);
  }

  @Post(':id/cancel')
  @ApiOperation({ summary: 'Cancel booking and process refund (Owner or Admin)' })
  cancelBooking(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Param('id') id: string,
    @Body() body: { reason: string },
  ) {
    const booking = this.bookingsService.findOne(id);
    // IDOR FIX: Only owner or admin can cancel booking
    if (currentUser.role !== 'ADMIN' && booking.userId !== currentUser.id) {
      throw new ForbiddenException('You can only cancel your own bookings.');
    }
    return this.bookingsService.cancelBooking(id, body?.reason);
  }
}
