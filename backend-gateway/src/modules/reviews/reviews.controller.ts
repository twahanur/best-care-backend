import { Controller, Get, Post, Put, Body, Query, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { ReviewsService } from './reviews.service';

@ApiTags('Reviews & Ratings')
@Controller('reviews')
export class ReviewsController {
  constructor(private readonly reviewsService: ReviewsService) {}

  @Get()
  @ApiOperation({ summary: 'Get reviews by car, user, or all' })
  findAll(
    @Query('carId') carId?: string,
    @Query('userId') userId?: string,
    @Query('isApproved') isApproved?: boolean,
  ) {
    return this.reviewsService.findAll({ carId, userId, isApproved });
  }

  @Post()
  @ApiOperation({ summary: 'User: Submit a review and rating for completed rental' })
  create(@Body() body: any) {
    return this.reviewsService.create(body);
  }

  @Put(':id/moderate')
  @ApiOperation({ summary: 'Admin: Moderate review approval and reply' })
  moderate(@Param('id') id: string, @Body() body: { isApproved: boolean; adminReply?: string }) {
    return this.reviewsService.moderate(id, body.isApproved, body.adminReply);
  }
}
