import { IsString, IsNotEmpty, IsEmail, IsNumber, IsOptional, Min } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { ProtectionPlan } from '../booking.interface';

export class CreateBookingDto {
  @ApiProperty({ example: 'car_prado_suv' })
  @IsString()
  @IsNotEmpty()
  vehicleId: string;

  @ApiProperty({ example: 'Toyota Land Cruiser Prado TX' })
  @IsString()
  @IsNotEmpty()
  vehicleName: string;

  @ApiProperty({ example: 'Rahim Ahmed' })
  @IsString()
  @IsNotEmpty()
  customerName: string;

  @ApiProperty({ example: 'rahim@enterprise.com' })
  @IsEmail()
  customerEmail: string;

  @ApiProperty({ example: '+8801712345678' })
  @IsString()
  @IsNotEmpty()
  customerPhone: string;

  @ApiProperty({ example: '2026-09-01T10:00:00Z' })
  @IsString()
  @IsNotEmpty()
  pickupDate: string;

  @ApiProperty({ example: '2026-09-05T18:00:00Z' })
  @IsString()
  @IsNotEmpty()
  dropoffDate: string;

  @ApiProperty({ example: 'Dhaka Hazrat Shahjalal International Airport (DAC)' })
  @IsString()
  @IsNotEmpty()
  pickupLocation: string;

  @ApiProperty({ example: 'Sylhet City Center Hub' })
  @IsString()
  @IsNotEmpty()
  dropoffLocation: string;

  @ApiProperty({ example: 4 })
  @IsNumber()
  @Min(1)
  totalDays: number;

  @ApiProperty({ example: 145 })
  @IsNumber()
  dailyRate: number;

  @ApiPropertyOptional({ example: 'Comprehensive Plus', enum: ['Basic CDW', 'Comprehensive Plus', 'VIP Full Shield'] })
  @IsOptional()
  @IsString()
  protectionPlan?: ProtectionPlan;

  @ApiPropertyOptional({ example: 'Need toddler child seat and English speaking driver' })
  @IsOptional()
  @IsString()
  notes?: string;
}
