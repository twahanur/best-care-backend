import { IsString, IsNotEmpty, IsNumber, IsBoolean, IsArray, IsOptional, Min } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { VehicleCategory, TransmissionType, FuelType } from '../vehicle.interface';

export class CreateVehicleDto {
  @ApiProperty({ example: 'Toyota Land Cruiser Prado TX' })
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty({ example: 'Toyota' })
  @IsString()
  @IsNotEmpty()
  brand: string;

  @ApiProperty({ example: 'SUV', enum: ['SUV', 'Sedan', 'Luxury', 'Electric', 'Van', 'Sports'] })
  @IsString()
  @IsNotEmpty()
  category: VehicleCategory;

  @ApiProperty({ example: 145 })
  @IsNumber()
  @Min(1)
  dailyRate: number;

  @ApiProperty({ example: 7 })
  @IsNumber()
  @Min(1)
  seats: number;

  @ApiProperty({ example: 5 })
  @IsNumber()
  @Min(2)
  doors: number;

  @ApiProperty({ example: 4 })
  @IsNumber()
  @Min(1)
  luggageCapacity: number;

  @ApiProperty({ example: 'Automatic', enum: ['Automatic', 'Manual'] })
  @IsString()
  transmission: TransmissionType;

  @ApiProperty({ example: 'Diesel', enum: ['Petrol', 'Diesel', 'Hybrid', 'Electric'] })
  @IsString()
  fuelType: FuelType;

  @ApiProperty({ example: '12 km/L' })
  @IsString()
  fuelEfficiency: string;

  @ApiProperty({ example: 'Mountainous / 4WD Off-road' })
  @IsString()
  terrainCapability: string;

  @ApiProperty({ example: 'https://images.unsplash.com/photo-1594502184342-2e12f877aa73' })
  @IsString()
  image: string;

  @ApiProperty({ example: ['4x4 Low-Range', 'Dual AC', 'GPS Navigation', 'Hill Descent Control'] })
  @IsArray()
  features: string[];

  @ApiProperty({ example: true })
  @IsBoolean()
  available: boolean;

  @ApiProperty({ example: true })
  @IsBoolean()
  featured: boolean;
}
