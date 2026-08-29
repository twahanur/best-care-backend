import { IsString, IsNotEmpty, IsIn } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { BookingStatus } from '../booking.interface';

export class UpdateBookingStatusDto {
  @ApiProperty({ example: 'Confirmed', enum: ['Pending', 'Confirmed', 'Active', 'Completed', 'Cancelled'] })
  @IsString()
  @IsNotEmpty()
  @IsIn(['Pending', 'Confirmed', 'Active', 'Completed', 'Cancelled'])
  status: BookingStatus;
}
