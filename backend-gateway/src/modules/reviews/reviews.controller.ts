import { Controller, Get, Post, Put, Body, Query, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ReviewsService } from './reviews.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';
import { CurrentUser, AuthenticatedUser } from '../../common/security/current-user.decorator';

@ApiTags('Reviews & Ratings')
@Controller('reviews')
@UseGuards(JwtAuthGuard, RolesGuard)
export class ReviewsController {
  constructor(private readonly reviewsService: ReviewsService) {}

  @Public()
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
  @ApiBearerAuth()
  @ApiOperation({ summary: 'User: Submit a review and rating for completed rental' })
  create(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Body() body: any,
  ) {
    return this.reviewsService.create({
      ...body,
      userId: currentUser.id,
      userName: currentUser.name || body.userName,
    });
  }

  @Put(':id/moderate')
  @Roles('ADMIN')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Admin: Moderate review approval and reply' })
  moderate(@Param('id') id: string, @Body() body: { isApproved: boolean; adminReply?: string }) {
    return this.reviewsService.moderate(id, body.isApproved, body.adminReply);
  }
}
