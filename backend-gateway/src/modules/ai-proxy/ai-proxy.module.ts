import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { AiProxyService } from './ai-proxy.service';
import { AiProxyController } from './ai-proxy.controller';
import { CarsModule } from '../cars/cars.module';

@Module({
  imports: [HttpModule, CarsModule],
  controllers: [AiProxyController],
  providers: [AiProxyService],
  exports: [AiProxyService]
})
export class AiProxyModule {}

