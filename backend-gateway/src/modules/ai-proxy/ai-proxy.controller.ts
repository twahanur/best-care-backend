import { Controller, Post, Get, Body } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AiProxyService } from './ai-proxy.service';
import { RagQueryDto } from './dto/rag-query.dto';
import { RecommendCarDto } from './dto/recommend-car.dto';

@ApiTags('AI & RAG Services')
@Controller('ai')
export class AiProxyController {
  constructor(private readonly aiProxyService: AiProxyService) {}

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
