import { Controller, Post, Get, Delete, Body, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiBearerAuth } from '@nestjs/swagger';
import { AiProxyService } from './ai-proxy.service';
import { AgentChatDto } from './dto/agent-chat.dto';
import { RagQueryDto } from './dto/rag-query.dto';
import { RecommendCarDto } from './dto/recommend-car.dto';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';

@ApiTags('AI & RAG Services')
@Controller('ai')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AiProxyController {
  constructor(private readonly aiProxyService: AiProxyService) {}

  @Public()
  @Post('chat')
  @ApiOperation({ summary: 'Agentic Multilingual Chat with Conversational Memory & PostgreSQL RAG Grounding' })
  @ApiResponse({ status: 200, description: 'Agentic AI response with memory perspective and source citations' })
  agenticChat(@Body() dto: AgentChatDto) {
    return this.aiProxyService.agenticChat(dto);
  }

  @Public()
  @Get('sessions/:sessionId/history')
  @ApiOperation({ summary: 'Get conversation history and memory turns for a session' })
  @ApiParam({ name: 'sessionId', description: 'Session UUID or ID' })
  getSessionHistory(@Param('sessionId') sessionId: string) {
    return this.aiProxyService.getSessionHistory(sessionId);
  }

  @Public()
  @Delete('sessions/:sessionId')
  @ApiOperation({ summary: 'Clear memory for a conversation session' })
  @ApiParam({ name: 'sessionId', description: 'Session UUID or ID' })
  clearSessionHistory(@Param('sessionId') sessionId: string) {
    return this.aiProxyService.clearSessionHistory(sessionId);
  }

  @Public()
  @Post('rag-query')
  @ApiOperation({ summary: 'Execute grounded RAG query across rental policies, fleet specs, and FAQs' })
  @ApiResponse({ status: 200, description: 'RAG grounded response with source citations' })
  executeRagQuery(@Body() dto: RagQueryDto) {
    return this.aiProxyService.executeRagQuery(dto);
  }

  @Public()
  @Post('recommend-car')
  @ApiOperation({ summary: 'AI Vehicle Matchmaker: Recommend optimal fleet vehicles based on trip characteristics' })
  @ApiResponse({ status: 200, description: 'Matched primary and alternative car recommendations' })
  recommendCar(@Body() dto: RecommendCarDto) {
    return this.aiProxyService.recommendCar(dto);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Get('knowledge-docs')
  @ApiOperation({ summary: 'Admin: Inspect knowledge base chunks indexed in vector store' })
  @ApiResponse({ status: 200, description: 'List of indexed knowledge documents' })
  getKnowledgeDocs() {
    return this.aiProxyService.getKnowledgeDocs();
  }
}
