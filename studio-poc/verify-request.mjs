import { createPublicKey, verify, createHash } from 'node:crypto';

// The signed payload is a UTF-8 JSON string. Never reserialize it before verification.
const PAGE_PATHS = new Set(['index.html', 'membership.html', 'purpose.html', 'communicate.html', 'privacy.html', 'legal-compliance.html']);
const sha = value => createHash('sha256').update(value).digest('hex');

export function verifyRequest(envelope, { publicJwk, head, now = Date.now(), seenIds = new Set() }) {
  if (!envelope || typeof envelope.payload !== 'string' || envelope.payload.length > 8_000_000 || typeof envelope.signature !== 'string') throw Error('invalid_envelope');
  const key = createPublicKey({ key: publicJwk, format: 'jwk' });
  if (!verify('sha256', Buffer.from(envelope.payload), { key, dsaEncoding: 'ieee-p1363' }, Buffer.from(envelope.signature, 'base64url'))) throw Error('invalid_signature');
  let p; try { p = JSON.parse(envelope.payload); } catch { throw Error('invalid_payload'); }
  if (p.version !== 1 || typeof p.id !== 'string' || !/^[a-f0-9-]{36}$/.test(p.id) || seenIds.has(p.id)) throw Error('invalid_or_replayed_id');
  if (!Number.isSafeInteger(p.issuedAt) || !Number.isSafeInteger(p.expiresAt) || p.issuedAt > now + 60_000 || p.expiresAt <= now || p.expiresAt - p.issuedAt > 86_400_000) throw Error('expired_request');
  if (!/^[a-f0-9]{40}$/.test(p.baseSha) || p.baseSha !== head) throw Error('source_conflict');
  if (!Array.isArray(p.files) || !p.files.length || p.files.length > 20) throw Error('invalid_files');
  const paths = new Set();
  for (const f of p.files) {
    if (!f || typeof f.path !== 'string' || !PAGE_PATHS.has(f.path) || paths.has(f.path)) throw Error('invalid_path');
    paths.add(f.path);
    if (typeof f.content !== 'string' || Buffer.byteLength(f.content, 'utf8') > 1_000_000 || !/^[a-f0-9]{64}$/.test(f.sha256) || sha(f.content) !== f.sha256) throw Error('invalid_content');
  }
  return p;
}
