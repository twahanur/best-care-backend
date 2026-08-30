import { Injectable, UnauthorizedException, BadRequestException } from '@nestjs/common';
import * as bcrypt from 'bcryptjs';
import { User, UserRole, UserStatus, KycStatus } from '../../common/types/schema.types';
import { JwtUtil } from '../../common/security/jwt.util';
import { sanitizeText } from '../../common/security/sanitize.util';

@Injectable()
export class AuthService {
  private users: User[] = [
    {
      id: 'usr_admin_1',
      name: 'Shahriar Admin',
      email: 'admin@rentcars.com',
      passwordHash: bcrypt.hashSync('admin123', 10),
      role: 'ADMIN',
      status: 'ACTIVE',
      kycStatus: 'VERIFIED',
      phone: '+8801819000001',
      avatarUrl: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNo: 'DL-DH-994821',
      address: 'Gulshan 2, Dhaka',
      city: 'Dhaka',
      createdAt: '2026-01-01T00:00:00Z',
      updatedAt: '2026-01-01T00:00:00Z',
    },
    {
      id: 'usr_cust_1',
      name: 'Shahriar Khan',
      email: 'shahriar@example.com',
      passwordHash: bcrypt.hashSync('user123', 10),
      role: 'CUSTOMER',
      status: 'ACTIVE',
      kycStatus: 'VERIFIED',
      phone: '+8801700112233',
      avatarUrl: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNo: 'DL-DH-482910',
      address: 'Banani DOHS, Dhaka',
      city: 'Dhaka',
      createdAt: '2026-02-10T00:00:00Z',
      updatedAt: '2026-02-10T00:00:00Z',
    },
    {
      id: 'usr_cust_2',
      name: 'Nusrat Jahan',
      email: 'nusrat@example.com',
      passwordHash: bcrypt.hashSync('user123', 10),
      role: 'CUSTOMER',
      status: 'ACTIVE',
      kycStatus: 'PENDING',
      phone: '+8801711987654',
      avatarUrl: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNo: 'DL-DH-738291',
      address: 'Dhanmondi Road 27, Dhaka',
      city: 'Dhaka',
      createdAt: '2026-02-15T00:00:00Z',
      updatedAt: '2026-02-15T00:00:00Z',
    },
    {
      id: 'usr_driver_1',
      name: 'Rafiqul Islam',
      email: 'rafiqul.driver@rentcars.com',
      passwordHash: bcrypt.hashSync('driver123', 10),
      role: 'CAR_DRIVER',
      status: 'ACTIVE',
      kycStatus: 'VERIFIED',
      phone: '+8801712334455',
      avatarUrl: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNo: 'DL-DH-882910',
      experienceYears: 6,
      isAvailableForTrip: true,
      driverRating: 4.95,
      totalTripsCompleted: 142,
      address: 'Mirpur 10, Dhaka',
      city: 'Dhaka',
      createdAt: '2026-01-20T00:00:00Z',
      updatedAt: '2026-01-20T00:00:00Z',
    }
  ];

  register(data: { name: string; email: string; password: string; phone?: string; drivingLicenseNo?: string; address?: string }) {
    if (!data.email || !data.password || typeof data.password !== 'string' || data.password.length < 6) {
      throw new BadRequestException('Valid email and password (minimum 6 characters) are required.');
    }

    const email = data.email.toLowerCase().trim();
    const existing = this.users.find(u => u.email.toLowerCase() === email);
    if (existing) {
      throw new BadRequestException('User with this email already exists.');
    }

    const cleanName = sanitizeText(data.name) || 'User';
    const cleanPhone = sanitizeText(data.phone) || '';
    const cleanLicense = sanitizeText(data.drivingLicenseNo) || '';
    const cleanAddress = sanitizeText(data.address) || '';

    const newUser: User = {
      id: `usr_${Date.now()}`,
      name: cleanName,
      email,
      passwordHash: bcrypt.hashSync(data.password, 10),
      // SECURITY FIX: Never accept role from user registration payload - force CUSTOMER
      role: 'CUSTOMER',
      status: 'ACTIVE',
      kycStatus: cleanLicense ? 'PENDING' : 'NOT_SUBMITTED',
      phone: cleanPhone,
      avatarUrl: `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(cleanName)}`,
      drivingLicenseNo: cleanLicense,
      address: cleanAddress,
      city: 'Dhaka',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    this.users.push(newUser);
    const token = JwtUtil.sign({
      sub: newUser.id,
      email: newUser.email,
      role: newUser.role,
      name: newUser.name,
    });

    return {
      user: this.sanitizeUser(newUser),
      accessToken: token,
    };
  }

  login(data: { email: string; password?: string }) {
    if (!data.email) {
      throw new UnauthorizedException('Email is required.');
    }
    // SECURITY FIX: Enforce mandatory password presence
    if (!data.password || typeof data.password !== 'string' || data.password.trim() === '') {
      throw new UnauthorizedException('Password is required.');
    }

    const user = this.users.find(u => u.email.toLowerCase() === data.email.toLowerCase().trim());
    if (!user) {
      throw new UnauthorizedException('Invalid email or password.');
    }

    // SECURITY FIX: Verify bcrypt password hash
    let isValidPassword = false;
    try {
      isValidPassword = bcrypt.compareSync(data.password, user.passwordHash);
    } catch {
      isValidPassword = false;
    }

    // Fallback for plain matches during development migration
    if (!isValidPassword && user.passwordHash === data.password) {
      isValidPassword = true;
      user.passwordHash = bcrypt.hashSync(data.password, 10);
    }

    if (!isValidPassword) {
      throw new UnauthorizedException('Invalid email or password.');
    }

    if (user.status === 'SUSPENDED') {
      throw new UnauthorizedException('Account suspended. Please contact administrator.');
    }

    const token = JwtUtil.sign({
      sub: user.id,
      email: user.email,
      role: user.role,
      name: user.name,
    });

    return {
      user: this.sanitizeUser(user),
      accessToken: token,
    };
  }

  getProfile(userId: string) {
    const user = this.users.find(u => u.id === userId);
    if (!user) {
      throw new UnauthorizedException('User not found.');
    }
    return this.sanitizeUser(user);
  }

  updateProfile(userId: string, data: Partial<User>) {
    const user = this.users.find(u => u.id === userId);
    if (!user) {
      throw new UnauthorizedException('User not found.');
    }

    // SECURITY FIX: Strip protected fields from updateProfile
    const safeData = {
      name: data.name ? sanitizeText(data.name) : user.name,
      phone: data.phone ? sanitizeText(data.phone) : user.phone,
      drivingLicenseNo: data.drivingLicenseNo ? sanitizeText(data.drivingLicenseNo) : user.drivingLicenseNo,
      address: data.address ? sanitizeText(data.address) : user.address,
      avatarUrl: data.avatarUrl || user.avatarUrl,
      updatedAt: new Date().toISOString()
    };

    Object.assign(user, safeData);
    return this.sanitizeUser(user);
  }

  getAllUsers(): User[] {
    return this.users.map(u => this.sanitizeUser(u));
  }

  updateUserStatus(userId: string, status: UserStatus, role?: UserRole, kycStatus?: KycStatus) {
    const user = this.users.find(u => u.id === userId);
    if (!user) {
      throw new BadRequestException('User not found.');
    }
    if (status) user.status = status;
    if (role) user.role = role;
    if (kycStatus) user.kycStatus = kycStatus;
    user.updatedAt = new Date().toISOString();
    return this.sanitizeUser(user);
  }

  private sanitizeUser(user: User): User {
    const copy = { ...user };
    delete (copy as any).passwordHash;
    return copy;
  }
}
