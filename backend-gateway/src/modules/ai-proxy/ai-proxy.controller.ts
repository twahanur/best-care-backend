import { Controller, Post, Get, Delete, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam } from '@nestjs/swagger';
import { AiProxyService } from './ai-proxy.service';
import { AgentChatDto } from './dto/agent-chat.dto';
import { RagQueryDto } from './dto/rag-query.dto';
import { RecommendCarDto } from './dto/recommend-car.dto';

@ApiTags('AI & RAG Services')
@Controller('ai')
export class AiProxyController {
  constructor(private readonly aiProxyService: AiProxyService) {}

  @Post('chat')
  @ApiOperation({ summary: 'Agentic Multilingual Chat with Conversational Memory & PostgreSQL RAG Grounding' })
  @ApiResponse({ status: 200, description: 'Agentic AI response with memory perspective and source citations' })
  agenticChat(@Body() dto: AgentChatDto) {
    return this.aiProxyService.agenticChat(dto);
  }

  @Get('sessions/:sessionId/history')
  @ApiOperation({ summary: 'Get conversation history and memory turns for a session' })
  @ApiParam({ name: 'sessionId', description: 'Session UUID or ID' })
  getSessionHistory(@Param('sessionId') sessionId: string) {
    return this.aiProxyService.getSessionHistory(sessionId);
  }

  @Delete('sessions/:sessionId')
  @ApiOperation({ summary: 'Clear memory for a conversation session' })
  @ApiParam({ name: 'sessionId', description: 'Session UUID or ID' })
  clearSessionHistory(@Param('sessionId') sessionId: string) {
    return this.aiProxyService.clearSessionHistory(sessionId);
  }

  @Post('rag-query')
  @ApiOperation({ summary: 'Execute grounded RAG query across rental policies, fleet specs, and FAQs' })
  @ApiResponse({ status: 200, description: 'RAG grounded response with source citations' })
  executeRagQuery(@Body() dto: RagQueryDto) {
    return this.aiProxyService.executeRagQuery(dto);
  }

  @Post('recommend-car')
  @ApiOperation({ summary: 'AI Vehicle Matchmaker: Recommend optimal fleet vehicles based on trip characteristics' })
  @ApiResponse({ status: 200, description: 'Matched primary and alternative car recommendations' })
  recommendCar(@Body() dto: RecommendCarDto) {
    return this.aiProxyService.recommendCar(dto);
  }

  @Get('knowledge-docs')
  @ApiOperation({ summary: 'Inspect knowledge base chunks indexed in vector store' })
  @ApiResponse({ status: 200, description: 'List of indexed knowledge documents' })
  getKnowledgeDocs() {
    return this.aiProxyService.getKnowledgeDocs();
  }
}
