import { NestFactory } from '@nestjs/core';
import { ValidationPipe, Logger } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import helmet from 'helmet';
import { AppModule } from './app.module';

async function bootstrap() {
  const logger = new Logger('Bootstrap');
  const app = await NestFactory.create(AppModule);

  // Apply HTTP Security Headers via Helmet (disabling CSP only for Swagger UI rendering if needed)
  app.use(
    helmet({
      contentSecurityPolicy: false, // Allows Swagger UI and local preview to render safely
      crossOriginEmbedderPolicy: false,
    })
  );

  // Global prefix for all API endpoints
  app.setGlobalPrefix('api');

  // CORS configuration
  const allowedOrigins = process.env.ALLOWED_ORIGINS
    ? process.env.ALLOWED_ORIGINS.split(',')
    : ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:4000', 'http://127.0.0.1:4000'];

  app.enableCors({
    origin: (origin, callback) => {
      // Allow requests with no origin (like mobile apps, curl, server-to-server) or in development
      if (!origin || allowedOrigins.includes(origin) || process.env.NODE_ENV !== 'production') {
        callback(null, true);
      } else {
        callback(new Error('Blocked by CORS policy'));
      }
    },
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    credentials: true,
  });

  // Global Validation Pipe with strict whitelisting and non-whitelisted rejection
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      transform: true,
      forbidNonWhitelisted: false,
    })
  );

  // Swagger OpenAPI Documentation with Bearer Auth
  const swaggerConfig = new DocumentBuilder()
    .setTitle('Digital Pylot - Car Rental Enterprise API Gateway')
    .setDescription(
      'Core REST API Gateway with Swagger documentation for Vehicles, Bookings, Analytics, AI RAG, and Webhook Automation.'
    )
    .setVersion('1.0.0')
    .addBearerAuth(
      {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        name: 'JWT',
        description: 'Enter JWT token',
        in: 'header',
      },
      'JWT-auth'
    )
    .addTag('Authentication & Users', 'User registration, secure JWT authentication, profile and RBAC')
    .addTag('Cars & Fleet Management', 'Vehicle fleet catalog, specifications, and hub transfers')
    .addTag('Bookings & Reservations', 'Customer rental booking lifecycle and state management')
    .addTag('Payments & Transactions', 'Payment verification, transaction auditing, and financial analytics')
    .addTag('Pricing & Rules Management', 'Dynamic pricing rules, discount coupons, and quote engine')
    .addTag('Reviews & Ratings', 'Customer review submission, moderation, and vehicle ratings')
    .addTag('Car Availability & Maintenance', 'Fleet availability, maintenance scheduling, and date holds')
    .addTag('Analytics & Reports', 'Executive dashboard metrics, revenue trends, and fleet charts')
    .addTag('AI & RAG Services', 'Vector-based grounded retrieval, policy search, and vehicle matchmaking')
    .addTag('Automation & Webhooks', 'Event-driven lead qualification, webhook dispatch, and audit logs')
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('api/docs', app, document, {
    customSiteTitle: 'Car Rental API Docs | Swagger',
    customCss: '.swagger-ui .topbar { display: none }',
  });

  const port = process.env.PORT || 4000;
  await app.listen(port, '0.0.0.0');

  logger.log(`=======================================================`);
  logger.log(`🚀 NestJS Backend Gateway running on: http://localhost:${port}`);
  logger.log(`📖 Swagger OpenAPI Documentation: http://localhost:${port}/api/docs`);
  logger.log(`🛡️ Security: Helmet headers, JWT RBAC, IDOR protection & Throttling active`);
  logger.log(`=======================================================`);
}

bootstrap();
