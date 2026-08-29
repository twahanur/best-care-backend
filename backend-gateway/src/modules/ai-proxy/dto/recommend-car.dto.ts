import { IsString, IsNotEmpty, IsNumber, IsOptional, Min, Max } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class RecommendCarDto {
  @ApiProperty({ example: 'Family trip of 6 people going to Sylhet tea gardens with lots of luggage' })
  @IsString()
  @IsNotEmpty()
  tripDescription: string;

  @ApiPropertyOptional({ example: 6, default: 4 })
  @IsOptional()
  @IsNumber()
  @Min(1)
  @Max(15)
  passengers?: number;

  @ApiPropertyOptional({ example: 150 })
  @IsOptional()
  @IsNumber()
  budgetPerDay?: number;

  @ApiPropertyOptional({ example: 'Hills / Off-road' })
  @IsOptional()
  @IsString()
  terrain?: string;
}
