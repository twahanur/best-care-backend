import { Injectable, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { User, UserRole } from '../../common/types/schema.types';

@Injectable()
export class AuthService {
  private users: User[] = [
    {
      id: 'usr_admin_1',
      name: 'Shahriar Admin',
      email: 'admin@rentcars.com',
      passwordHash: 'admin123',
      role: 'ADMIN',
      phone: '+8801819000001',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNumber: 'DL-DH-994821',
      address: 'Gulshan 2, Dhaka',
      status: 'ACTIVE',
      createdAt: '2026-01-01T00:00:00Z',
      updatedAt: '2026-01-01T00:00:00Z',
    },
    {
      id: 'usr_cust_1',
      name: 'Shahriar Khan',
      email: 'shahriar@example.com',
      passwordHash: 'user123',
      role: 'CUSTOMER',
      phone: '+8801700112233',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNumber: 'DL-DH-482910',
      address: 'Banani DOHS, Dhaka',
      status: 'ACTIVE',
      createdAt: '2026-02-10T00:00:00Z',
      updatedAt: '2026-02-10T00:00:00Z',
    },
    {
      id: 'usr_cust_2',
      name: 'Nusrat Jahan',
      email: 'nusrat@example.com',
      passwordHash: 'user123',
      role: 'CUSTOMER',
      phone: '+8801711987654',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80',
      drivingLicenseNumber: 'DL-DH-738291',
      address: 'Dhanmondi Road 27, Dhaka',
      status: 'ACTIVE',
      createdAt: '2026-02-15T00:00:00Z',
      updatedAt: '2026-02-15T00:00:00Z',
    }
  ];

  register(data: { name: string; email: string; password: string; phone: string; drivingLicenseNumber?: string; address?: string }) {
    const existing = this.users.find(u => u.email.toLowerCase() === data.email.toLowerCase());
    if (existing) {
      throw new BadRequestException('User with this email already exists.');
    }

    const newUser: User = {
      id: `usr_${Date.now()}`,
      name: data.name,
      email: data.email.toLowerCase(),
      passwordHash: data.password,
      role: 'CUSTOMER',
      phone: data.phone,
      avatar: `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(data.name)}`,
      drivingLicenseNumber: data.drivingLicenseNumber || '',
      address: data.address || '',
      status: 'ACTIVE',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    this.users.push(newUser);
    const token = `jwt_token_${newUser.id}_${Date.now()}`;

    return {
      user: this.sanitizeUser(newUser),
      accessToken: token,
    };
  }

  login(data: { email: string; password?: string }) {
    const user = this.users.find(u => u.email.toLowerCase() === data.email.toLowerCase());
    if (!user) {
      throw new UnauthorizedException('Invalid email or password.');
    }

    if (data.password && user.passwordHash !== data.password) {
      throw new UnauthorizedException('Invalid email or password.');
    }

    if (user.status === 'SUSPENDED') {
      throw new UnauthorizedException('Account suspended. Please contact administrator.');
    }

    const token = `jwt_token_${user.id}_${Date.now()}`;
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

    Object.assign(user, {
      ...data,
      updatedAt: new Date().toISOString()
    });

    return this.sanitizeUser(user);
  }

  getAllUsers(): User[] {
    return this.users.map(u => this.sanitizeUser(u));
  }

  updateUserStatus(userId: string, status: 'ACTIVE' | 'SUSPENDED', role?: UserRole) {
    const user = this.users.find(u => u.id === userId);
    if (!user) {
      throw new BadRequestException('User not found.');
    }
    user.status = status;
    if (role) user.role = role;
    user.updatedAt = new Date().toISOString();
    return this.sanitizeUser(user);
  }

  private sanitizeUser(user: User): User {
    const copy = { ...user };
    delete (copy as any).passwordHash;
    return copy;
  }
}
