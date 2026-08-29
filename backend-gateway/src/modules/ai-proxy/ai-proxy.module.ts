import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { AiProxyService } from './ai-proxy.service';
import { AiProxyController } from './ai-proxy.controller';

@Module({
  imports: [HttpModule],
  controllers: [AiProxyController],
  providers: [AiProxyService],
  exports: [AiProxyService]
})
export class AiProxyModule {}
