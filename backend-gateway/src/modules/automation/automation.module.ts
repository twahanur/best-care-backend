import { Module } from '@nestjs/common';
import { AutomationService } from './automation.service';
import { AutomationController } from './automation.controller';
import { AiProxyModule } from '../ai-proxy/ai-proxy.module';

@Module({
  imports: [AiProxyModule],
  controllers: [AutomationController],
  providers: [AutomationService],
  exports: [AutomationService]
})
export class AutomationModule {}
