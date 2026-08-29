import { IsString, IsNotEmpty, IsOptional } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class RagQueryDto {
  @ApiProperty({ example: 'What are the insurance options and security deposit rules?' })
  @IsString()
  @IsNotEmpty()
  query: string;

  @ApiPropertyOptional({ example: 'Rental Policy' })
  @IsOptional()
  @IsString()
  category?: string;
}
