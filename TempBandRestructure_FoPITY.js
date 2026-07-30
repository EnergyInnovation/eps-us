// Restructure the FoPITY policy-schedule CSVs for the Industrial Process
// temperature-band change. Renames heating-process rows and inserts rows for
// the new band, copying ramp values verbatim from the adjacent
// "heat 500 to 1000 C" rows. No new data values are invented.
// Run: node TempBandRestructure_FoPITY.js
'use strict';
const fs = require('fs');
const path = require('path');

const DIR = path.join('InputData', 'plcy-schd', 'FoPITY');
const RENAMES = new Map([
  ['boilers', 'heat below 100 C'],
  ['nonboiler low temp', 'heat 100 to 200 C'],
  ['nonboiler med temp', 'heat 200 to 500 C'],
  ['nonboiler high temp', 'heat 500 to 1000 C'],
]);
const LASTBAND = 'heat 500 to 1000 C';
const NEWBAND = 'heat above 1000 C';

// how each policy carries the Industrial Process subscript
const S2_PROCESS = new Set([
  'indst shift to electricity', 'indst shift to alt fuel', 'indst eqpt early retirement',
  'indst fuel efficiency stds', 'indst elec efficiency stds',
]);
const S1_PROCESS_BLOCK = new Set(['indst eqpt cost of capital', 'RnD industry capital cost reduction']);
const S1_HEATING = new Set(['indst clean heat ITC', 'indst clean heat PTC']);

function assert(cond, msg) { if (!cond) { console.error('ASSERTION FAILED: ' + msg); process.exit(1); } }

// transform a list of row objects {fields:[policy,s1,s2,...]}; returns stats
function transform(rows) {
  let renamed = 0;
  for (const r of rows) {
    const policy = r.fields[0];
    let pi = -1; // index of the process field
    if (S2_PROCESS.has(policy)) pi = 2;
    else if (S1_PROCESS_BLOCK.has(policy) || S1_HEATING.has(policy)) pi = 1;
    if (pi >= 0 && RENAMES.has(r.fields[pi])) { r.fields[pi] = RENAMES.get(r.fields[pi]); renamed++; }
  }
  const out = [];
  let inserted = 0;
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    out.push(r);
    const policy = r.fields[0];
    if ((S2_PROCESS.has(policy) && r.fields[2] === LASTBAND) ||
        (S1_HEATING.has(policy) && r.fields[1] === LASTBAND)) {
      const c = { fields: r.fields.slice() };
      c.fields[S2_PROCESS.has(policy) ? 2 : 1] = NEWBAND;
      out.push(c); inserted++;
    } else if (S1_PROCESS_BLOCK.has(policy) && r.fields[1] === LASTBAND) {
      const next = rows[i + 1];
      if (!next || next.fields[0] !== policy || next.fields[1] !== LASTBAND) {
        // end of this policy's 500-1000 block: append the whole block copied for the new band
        let j = i;
        while (j >= 0 && rows[j].fields[0] === policy && rows[j].fields[1] === LASTBAND) j--;
        for (let k = j + 1; k <= i; k++) {
          const c = { fields: rows[k].fields.slice() };
          c.fields[1] = NEWBAND;
          out.push(c); inserted++;
        }
      }
    }
  }
  return { rows: out, renamed, inserted };
}

function processScheduleFile(file) {
  const raw = fs.readFileSync(file, 'latin1');
  const nl = raw.includes('\r\n') ? '\r\n' : '\n';
  const lines = raw.split(/\r?\n/);
  const trailingBlank = [];
  while (lines.length && lines[lines.length - 1].trim() === '') trailingBlank.push(lines.pop());
  const header = lines.shift();
  const rows = lines.map((l) => ({ fields: l.split(',') }));
  const { rows: out, renamed, inserted } = transform(rows);
  assert(renamed === 656, `${file}: expected 656 renamed rows, got ${renamed}`);
  assert(inserted === 164, `${file}: expected 164 inserted rows, got ${inserted}`);
  const text = [header, ...out.map((r) => r.fields.join(','))].join(nl) + trailingBlank.map(() => nl).join('');
  fs.writeFileSync(file, text, 'latin1');
  return out.map((r) => r.fields.filter((f, i) => i < 4 && f !== '').join(' X '));
}

function processElementsFile(file) {
  const raw = fs.readFileSync(file, 'latin1');
  const nl = raw.includes('\r\n') ? '\r\n' : '\n';
  const lines = raw.split(/\r?\n/);
  const trailingBlank = [];
  while (lines.length && lines[lines.length - 1].trim() === '') trailingBlank.push(lines.pop());
  const header = lines.shift();
  const rows = lines.map((l) => ({ fields: l.split(' X ') }));
  const { rows: out, renamed, inserted } = transform(rows);
  assert(renamed === 656, `${file}: expected 656 renamed rows, got ${renamed}`);
  assert(inserted === 164, `${file}: expected 164 inserted rows, got ${inserted}`);
  const text = [header, ...out.map((r) => r.fields.join(' X '))].join(nl) + trailingBlank.map(() => nl).join('');
  fs.writeFileSync(file, text, 'latin1');
  // normalize: subscript-less elements carry a trailing " X" in this file
  return out.map((r) => r.fields.join(' X ').replace(/( X)+$/, ''));
}

// back up, then transform
const files = ['FoPITY-policy-elements.csv'];
for (let i = 1; i <= 9; i++) files.push(`FoPITY-${i}.csv`, `FoPITY-${i}-WebApp.csv`);
for (const f of files) {
  const p = path.join(DIR, f);
  assert(fs.existsSync(p), `missing ${p}`);
  fs.copyFileSync(p, p + '.bak');
}
const elementSeq = processElementsFile(path.join(DIR, 'FoPITY-policy-elements.csv'));
console.log(`FoPITY-policy-elements.csv: ${elementSeq.length} elements (renamed 656, inserted 164)`);
for (const f of files.slice(1)) {
  const seq = processScheduleFile(path.join(DIR, f));
  assert(seq.length === elementSeq.length, `${f}: ${seq.length} rows vs ${elementSeq.length} elements`);
  for (let i = 0; i < seq.length; i++) {
    assert(seq[i] === elementSeq[i], `${f}: row ${i + 2} "${seq[i]}" != policy-elements "${elementSeq[i]}"`);
  }
  console.log(`${f}: OK, sequence matches policy-elements (${seq.length} rows)`);
}
console.log('DONE — .bak copies alongside each file');
