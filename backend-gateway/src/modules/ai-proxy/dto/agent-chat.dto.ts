import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsNotEmpty, IsOptional, IsString } from 'class-validator';

export class AgentChatDto {
  @ApiProperty({
    description: 'User inquiry in English, Bangla (বাংলা), or Banglish',
    example: 'amader 6 joner family niye sajek jabo kon gari bhalo hobe?'
  })
  @IsNotEmpty()
  @IsString()
  query: string;

  @ApiPropertyOptional({
    description: 'Session identifier for conversation memory context',
    example: 'session_user_456'
  })
  @IsOptional()
  @IsString()
  sessionId?: string;

  @ApiPropertyOptional({
    description: 'User ID for long-term preference personalization',
    example: 'usr_1001'
  })
  @IsOptional()
  @IsString()
  userId?: string;

  @ApiPropertyOptional({
    description: 'Optional category filter',
    example: 'Fleet Specs'
  })
  @IsOptional()
  @IsString()
  category?: string;
}
