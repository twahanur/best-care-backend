import { IsOptional, IsString, IsNumber, IsBoolean, Min, Max } from 'class-validator';
import { Type, Transform } from 'class-transformer';
import { ApiPropertyOptional } from '@nestjs/swagger';
import { VehicleCategory, TransmissionType, FuelType } from '../vehicle.interface';

export class FilterVehicleDto {
  @ApiPropertyOptional({ description: 'Filter by category', enum: ['SUV', 'Sedan', 'Luxury', 'Electric', 'Van', 'Sports'] })
  @IsOptional()
  @IsString()
  category?: VehicleCategory;

  @ApiPropertyOptional({ description: 'Filter by search term in name or brand' })
  @IsOptional()
  @IsString()
  search?: string;

  @ApiPropertyOptional({ description: 'Minimum daily rental price' })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  minPrice?: number;

  @ApiPropertyOptional({ description: 'Maximum daily rental price' })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  maxPrice?: number;

  @ApiPropertyOptional({ description: 'Minimum passenger seats' })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(1)
  seats?: number;

  @ApiPropertyOptional({ description: 'Transmission type', enum: ['Automatic', 'Manual'] })
  @IsOptional()
  @IsString()
  transmission?: TransmissionType;

  @ApiPropertyOptional({ description: 'Fuel type', enum: ['Petrol', 'Diesel', 'Hybrid', 'Electric'] })
  @IsOptional()
  @IsString()
  fuelType?: FuelType;

  @ApiPropertyOptional({ description: 'Filter only available vehicles' })
  @IsOptional()
  @Transform(({ value }) => value === 'true' || value === true)
  @IsBoolean()
  available?: boolean;

  @ApiPropertyOptional({ description: 'Filter featured vehicles only' })
  @IsOptional()
  @Transform(({ value }) => value === 'true' || value === true)
  @IsBoolean()
  featured?: boolean;
}
