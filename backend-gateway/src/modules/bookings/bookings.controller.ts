import { Controller, Get, Post, Body, Param, Query, Patch } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiQuery } from '@nestjs/swagger';
import { BookingsService } from './bookings.service';
import { CreateBookingDto } from './dto/create-booking.dto';
import { UpdateBookingStatusDto } from './dto/update-booking-status.dto';

@ApiTags('Bookings')
@Controller('bookings')
export class BookingsController {
  constructor(private readonly bookingsService: BookingsService) {}

  @Get()
  @ApiOperation({ summary: 'List and filter customer bookings' })
  @ApiQuery({ name: 'status', required: false, description: 'Filter by booking status' })
  @ApiQuery({ name: 'search', required: false, description: 'Search by code, customer name or email' })
  findAll(@Query('status') status?: string, @Query('search') search?: string) {
    return this.bookingsService.findAll(status, search);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get booking details by ID or Booking Code' })
  @ApiResponse({ status: 200, description: 'Booking record' })
  @ApiResponse({ status: 404, description: 'Booking not found' })
  findOne(@Param('id') id: string) {
    return this.bookingsService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create a new car rental booking' })
  @ApiResponse({ status: 201, description: 'Booking successfully confirmed' })
  create(@Body() dto: CreateBookingDto) {
    return this.bookingsService.create(dto);
  }

  @Patch(':id/status')
  @ApiOperation({ summary: 'Update booking status (Admin)' })
  updateStatus(@Param('id') id: string, @Body() dto: UpdateBookingStatusDto) {
    return this.bookingsService.updateStatus(id, dto);
  }
}
