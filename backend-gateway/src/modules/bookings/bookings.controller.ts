import { Controller, Get, Post, Put, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { BookingsService } from './bookings.service';
import { BookingStatus } from '../../common/types/schema.types';

@ApiTags('Bookings & Reservations')
@Controller('bookings')
export class BookingsController {
  constructor(private readonly bookingsService: BookingsService) {}

  @Get()
  @ApiOperation({ summary: 'Get all bookings with optional status, user, and search filters' })
  findAll(
    @Query('status') status?: string,
    @Query('search') search?: string,
    @Query('userId') userId?: string,
  ) {
    return this.bookingsService.findAll(status, search, userId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get booking details by ID or code' })
  findOne(@Param('id') id: string) {
    return this.bookingsService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create a new car rental reservation' })
  create(@Body() body: any) {
    return this.bookingsService.create(body);
  }

  @Put(':id/status')
  @ApiOperation({ summary: 'Update booking status lifecycle' })
  updateStatus(@Param('id') id: string, @Body() body: { status: BookingStatus }) {
    return this.bookingsService.updateStatus(id, body.status);
  }

  @Post(':id/cancel')
  @ApiOperation({ summary: 'Cancel booking and process full refund' })
  cancelBooking(@Param('id') id: string, @Body() body: { reason: string }) {
    return this.bookingsService.cancelBooking(id, body?.reason);
  }
}
