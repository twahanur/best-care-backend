import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { IS_PUBLIC_KEY } from './public.decorator';
import { JwtUtil } from './jwt.util';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers['authorization'];

    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      try {
        const payload = JwtUtil.verify(token);
        request.user = {
          id: payload.sub,
          email: payload.email,
          role: payload.role,
          name: payload.name,
        };
        return true;
      } catch (err: any) {
        if (!isPublic) {
          throw new UnauthorizedException(`Unauthorized: ${err.message}`);
        }
      }
    }

    if (isPublic) {
      return true;
    }

    throw new UnauthorizedException('Authentication token required');
  }
}
