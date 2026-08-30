import { Controller, Post, Get, Delete, Body, Param, UseGuards, Req } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiBearerAuth } from '@nestjs/swagger';
import { AiProxyService } from './ai-proxy.service';
import { AgentChatDto } from './dto/agent-chat.dto';
import { RagQueryDto } from './dto/rag-query.dto';
import { RecommendCarDto } from './dto/recommend-car.dto';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';
import { CurrentUser, AuthenticatedUser } from '../../common/security/current-user.decorator';

@ApiTags('AI & RAG Services')
@Controller('ai')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AiProxyController {
  constructor(private readonly aiProxyService: AiProxyService) {}

  @Public()
  @Post('chat')
  @ApiOperation({ summary: 'Agentic Multilingual Chat with Conversational Booking, SQL Grounding & Vector Search' })
  @ApiResponse({ status: 200, description: 'Grounded response with live SQL query results or conversational booking steps' })
  agenticChat(
    @Body() dto: AgentChatDto,
    @CurrentUser() currentUser?: AuthenticatedUser,
    @Req() req?: any
  ) {
    const authHeader = req?.headers?.authorization;
    return this.aiProxyService.agenticChat(dto, currentUser, authHeader);
  }

  @Roles('ADMIN')
  @ApiBearerAuth()
  @Post('admin/chat')
  @ApiOperation({ summary: 'Admin Fleet & Revenue Analytics Chat' })
  @ApiResponse({ status: 200, description: 'Admin analytics grounded response' })
  adminChat(
    @Body() dto: AgentChatDto,
    @CurrentUser() currentUser?: AuthenticatedUser,
    @Req() req?: any
  ) {
    const authHeader = req?.headers?.authorization;
    return this.aiProxyService.agenticChat({ ...dto, category: 'admin' }, currentUser || { id: 'usr_admin_1', role: 'ADMIN', email: 'admin@bestcare.com' }, authHeader);
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
