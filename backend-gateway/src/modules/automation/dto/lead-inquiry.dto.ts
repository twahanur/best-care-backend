import { IsString, IsNotEmpty, IsEmail, IsNumber, IsOptional, Min, IsBoolean } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class LeadInquiryDto {
  @ApiProperty({ example: 'Tanvir Ahmed' })
  @IsString()
  @IsNotEmpty()
  customerName: string;

  @ApiProperty({ example: 'tanvir.ahmed@grameenphone.com' })
  @IsEmail()
  customerEmail: string;

  @ApiProperty({ example: '+8801711223344' })
  @IsString()
  @IsNotEmpty()
  customerPhone: string;

  @ApiPropertyOptional({ example: 'Luxury SUV' })
  @IsOptional()
  @IsString()
  vehicleCategory?: string;

  @ApiProperty({ example: 6 })
  @IsNumber()
  @Min(1)
  totalDays: number;

  @ApiPropertyOptional({ example: 870 })
  @IsOptional()
  @IsNumber()
  estimatedBudget?: number;

  @ApiPropertyOptional({ example: 'Corporate Delegation Roadshow' })
  @IsOptional()
  @IsString()
  tripPurpose?: string;

  @ApiPropertyOptional({ example: 'Need VIP Prado TX with executive chauffeur for 5 days in Sylhet' })
  @IsOptional()
  @IsString()
  notes?: string;

  @ApiPropertyOptional({ example: true })
  @IsOptional()
  @IsBoolean()
  isCorporate?: boolean;
}
