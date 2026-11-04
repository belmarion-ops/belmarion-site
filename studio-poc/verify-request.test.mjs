import { test } from 'node:test';
import assert from 'node:assert/strict';
import { generateKeyPairSync, sign, createHash } from 'node:crypto';
import { verifyRequest } from './verify-request.mjs';

const { publicKey, privateKey } = generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
const publicJwk = publicKey.export({ format: 'jwk' });
const now = Date.now(), head = 'a'.repeat(40), content = 'Example';
const payload = { version: 1, id: '12345678-1234-4234-8234-123456789abc', issuedAt: now, expiresAt: now + 60000, baseSha: head, files: [{ path: 'index.html', content, sha256: createHash('sha256').update(content).digest('hex') }] };
function envelope(p = payload) { const text = JSON.stringify(p); return { payload: text, signature: sign('sha256', Buffer.from(text), { key: privateKey, dsaEncoding: 'ieee-p1363' }).toString('base64url') }; }
const options = { publicJwk, head, now };
test('accepts a valid signed request', () => assert.equal(verifyRequest(envelope(), options).id, payload.id));
test('rejects tampering', () => { const e = envelope(); e.payload = e.payload.replace('Example', 'Changed'); assert.throws(() => verifyRequest(e, options), /invalid_signature/); });
test('rejects a different website head', () => assert.throws(() => verifyRequest(envelope(), { ...options, head: 'b'.repeat(40) }), /source_conflict/));
test('rejects expired requests and replays', () => { assert.throws(() => verifyRequest(envelope(), { ...options, now: now + 60001 }), /expired_request/); assert.throws(() => verifyRequest(envelope(), { ...options, seenIds: new Set([payload.id]) }), /invalid_or_replayed_id/); });
test('protects operational paths and workflow files', () => { for (const path of ['office-dossier.html', '.github/workflows/pages.yml', '../index.html']) assert.throws(() => verifyRequest(envelope({ ...payload, files: [{ ...payload.files[0], path }] }), options), /invalid_path/); });
test('rejects mismatched content hashes', () => assert.throws(() => verifyRequest(envelope({ ...payload, files: [{ ...payload.files[0], content: 'changed' }] }), options), /invalid_content/));
