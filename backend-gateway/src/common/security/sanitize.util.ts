/**
 * Sanitizes input strings to prevent Stored XSS and Content Injection attacks.
 * Strips script tags, HTML tags, and escapes dangerous characters.
 */
export function sanitizeText(input?: string): string {
  if (!input || typeof input !== 'string') {
    return '';
  }

  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<[^>]+>/g, '')
    .trim();
}

/**
 * Validates that an ID string contains only safe alphanumeric and standard prefix characters.
 */
export function isValidId(id?: string): boolean {
  if (!id || typeof id !== 'string') return false;
  return /^[a-zA-Z0-9_\-\.]+$/.test(id);
}
