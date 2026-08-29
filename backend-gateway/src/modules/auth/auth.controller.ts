import { Controller, Post, Get, Put, Body, Query, Headers } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { AuthService } from './auth.service';

@ApiTags('Authentication & Users')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  @ApiOperation({ summary: 'Register a new customer account' })
  register(@Body() body: { name: string; email: string; password: string; phone: string; drivingLicenseNumber?: string; address?: string }) {
    return this.authService.register(body);
  }

  @Post('login')
  @ApiOperation({ summary: 'Login with email & password' })
  login(@Body() body: { email: string; password?: string }) {
    return this.authService.login(body);
  }

  @Get('profile')
  @ApiOperation({ summary: 'Get current user profile' })
  getProfile(@Query('userId') userId: string) {
    return this.authService.getProfile(userId || 'usr_cust_1');
  }

  @Put('profile')
  @ApiOperation({ summary: 'Update user profile and driving documents' })
  updateProfile(@Body() body: { userId: string; name?: string; phone?: string; drivingLicenseNumber?: string; address?: string; avatar?: string }) {
    return this.authService.updateProfile(body.userId, body);
  }

  @Get('users')
  @ApiOperation({ summary: 'Admin: Get all registered users' })
  getAllUsers() {
    return this.authService.getAllUsers();
  }

  @Put('users/status')
  @ApiOperation({ summary: 'Admin: Update user status and role' })
  updateUserStatus(@Body() body: { userId: string; status: 'ACTIVE' | 'SUSPENDED'; role?: any }) {
    return this.authService.updateUserStatus(body.userId, body.status, body.role);
  }
}
