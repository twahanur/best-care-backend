import { NestFactory } from '@nestjs/core';
import { ValidationPipe, Logger } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const logger = new Logger('Bootstrap');
  const app = await NestFactory.create(AppModule);

  // Global prefix for all API endpoints
  app.setGlobalPrefix('api');

  // Enable CORS
  app.enableCors({
    origin: true,
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    credentials: true,
  });

  // Global Validation Pipe for strict DTO checking
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      transform: true,
      forbidNonWhitelisted: false,
    })
  );

  // Swagger OpenAPI Documentation
  const swaggerConfig = new DocumentBuilder()
    .setTitle('Digital Pylot - Car Rental Enterprise API Gateway')
    .setDescription(
      'Core REST API Gateway with Swagger documentation for Vehicles, Bookings, Analytics, AI RAG, and Webhook Automation.'
    )
    .setVersion('1.0.0')
    .addTag('Vehicles', 'Vehicle fleet catalog, specifications and real-time filters')
    .addTag('Bookings', 'Customer rental booking lifecycle and state management')
    .addTag('Analytics', 'Executive dashboard metrics, revenue trends and fleet charts')
    .addTag('AI & RAG Services', 'Vector-based grounded retrieval, policy search and vehicle matchmaking')
    .addTag('Automation & Webhooks', 'Event-driven lead qualification, webhook dispatch and audit logs')
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('api/docs', app, document, {
    customSiteTitle: 'Car Rental API Docs | Swagger',
    customCss: '.swagger-ui .topbar { display: none }',
  });

  const port = process.env.PORT || 4000;
  await app.listen(port);

  logger.log(`=======================================================`);
  logger.log(`🚀 NestJS Backend Gateway running on: http://localhost:${port}`);
  logger.log(`📖 Swagger OpenAPI Documentation: http://localhost:${port}/api/docs`);
  logger.log(`=======================================================`);
}

bootstrap();
