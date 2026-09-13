// Render each narration block in script.md to vo/NN_name.mp3 via ElevenLabs.
const fs = require('fs');
const path = require('path');
const https = require('https');

const KEY = process.env.ELEVENLABS_API_KEY;
if (!KEY) { console.error('ELEVENLABS_API_KEY not set'); process.exit(1); }
const VOICE = process.argv[2] || 'CwhRBWXzGAHq8TQ4Fs17';   // Roger
const DIR = __dirname;
const OUT = path.join(DIR, 'vo');
fs.mkdirSync(OUT, { recursive: true });

const md = fs.readFileSync(path.join(DIR, 'script.md'), 'utf8');
const blocks = [];
const re = /^##\s+(\S+)\s*(?:\(([^)]*)\))?\s*$/gm;
let m, last = null;
while ((m = re.exec(md)) !== null) {
  if (last) last.text = md.slice(last.end, m.index).trim();
  last = { name: m[1], note: m[2] || '', end: re.lastIndex };
  blocks.push(last);
}
if (last) last.text = md.slice(last.end).trim();

const clean = (t) => t
  .replace(/^---$/gm, '')
  .replace(/\s*\n\s*/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

function tts(text, file) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      text,
      model_id: 'eleven_multilingual_v2',
      voice_settings: { stability: 0.45, similarity_boost: 0.75, style: 0.1, use_speaker_boost: true },
    });
    const req = https.request({
      hostname: 'api.elevenlabs.io',
      path: `/v1/text-to-speech/${VOICE}?output_format=mp3_44100_128`,
      method: 'POST',
      headers: {
        'xi-api-key': KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        if (res.statusCode !== 200) return reject(new Error(res.statusCode + ' ' + buf.toString().slice(0, 300)));
        fs.writeFileSync(file, buf);
        resolve(buf.length);
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

const only = process.argv[3] ? process.argv[3].split(',') : null;

(async () => {
  for (const b of blocks) {
    if (only && !only.includes(b.name)) continue;
    const text = clean(b.text);
    if (!text) continue;
    const file = path.join(OUT, b.name + '.mp3');
    try {
      const n = await tts(text, file);
      console.log(`${b.name.padEnd(14)} ${String(text.split(/\s+/).length).padStart(4)} words  ${(n / 1024).toFixed(0).padStart(4)} KB`);
    } catch (e) {
      console.log(`${b.name.padEnd(14)} FAILED: ${e.message}`);
    }
  }
})();
