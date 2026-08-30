import {
  Controller,
  Post,
  Get,
  Put,
  Body,
  Query,
  UseGuards,
  UnauthorizedException,
  ForbiddenException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { JwtAuthGuard } from '../../common/security/jwt-auth.guard';
import { RolesGuard } from '../../common/security/roles.guard';
import { Roles } from '../../common/security/roles.decorator';
import { Public } from '../../common/security/public.decorator';
import { CurrentUser, AuthenticatedUser } from '../../common/security/current-user.decorator';

@ApiTags('Authentication & Users')
@Controller('auth')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Public()
  @Post('register')
  @ApiOperation({ summary: 'Register a new customer account' })
  register(@Body() body: { name: string; email: string; password: string; phone?: string; drivingLicenseNumber?: string; address?: string }) {
    return this.authService.register({
      name: body.name,
      email: body.email,
      password: body.password,
      phone: body.phone,
      drivingLicenseNo: body.drivingLicenseNumber,
      address: body.address,
    });
  }

  @Public()
  @Post('login')
  @ApiOperation({ summary: 'Login with email & password' })
  login(@Body() body: { email: string; password?: string }) {
    return this.authService.login(body);
  }

  @Get('profile')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Get current user profile (Owner or Admin only)' })
  getProfile(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Query('userId') queryUserId?: string,
  ) {
    if (!currentUser) {
      throw new UnauthorizedException('Authentication required');
    }

    // IDOR FIX: If queryUserId is requested, verify the caller owns it or is an ADMIN
    let targetUserId = currentUser.id;
    if (queryUserId && queryUserId !== currentUser.id) {
      if (currentUser.role !== 'ADMIN') {
        throw new ForbiddenException('You do not have permission to view other users profiles');
      }
      targetUserId = queryUserId;
    }

    return this.authService.getProfile(targetUserId);
  }

  @Put('profile')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update user profile (Owner or Admin only)' })
  updateProfile(
    @CurrentUser() currentUser: AuthenticatedUser,
    @Body() body: { userId?: string; name?: string; phone?: string; drivingLicenseNumber?: string; address?: string; avatar?: string },
  ) {
    if (!currentUser) {
      throw new UnauthorizedException('Authentication required');
    }

    // IDOR FIX: User can only update their own profile unless they are an ADMIN
    let targetUserId = currentUser.id;
    if (body.userId && body.userId !== currentUser.id) {
      if (currentUser.role !== 'ADMIN') {
        throw new ForbiddenException('You do not have permission to update other users profiles');
      }
      targetUserId = body.userId;
    }

    return this.authService.updateProfile(targetUserId, {
      name: body.name,
      phone: body.phone,
      drivingLicenseNo: body.drivingLicenseNumber,
      address: body.address,
      avatarUrl: body.avatar,
    });
  }

  @Get('users')
  @ApiBearerAuth()
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Admin: Get all registered users' })
  getAllUsers() {
    return this.authService.getAllUsers();
  }

  @Put('users/status')
  @ApiBearerAuth()
  @Roles('ADMIN')
  @ApiOperation({ summary: 'Admin: Update user status and role' })
  updateUserStatus(@Body() body: { userId: string; status: 'ACTIVE' | 'SUSPENDED'; role?: any; kycStatus?: any }) {
    return this.authService.updateUserStatus(body.userId, body.status, body.role, body.kycStatus);
  }
}
