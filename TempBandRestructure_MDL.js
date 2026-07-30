// Restructure Industrial Process heating elements into temperature bands.
// Transforms EPS.mdl and GraphDefinitions.vgd IN PLACE (writes EPS.mdl.bak /
// GraphDefinitions.vgd.bak first). Structural/code changes only — no data values.
// Run: node TempBandRestructure_MDL.js
'use strict';
const fs = require('fs');

const RENAMES = [
  ['nonboiler low temp', 'heat 100 to 200 C'],
  ['nonboiler med temp', 'heat 200 to 500 C'],
  ['nonboiler high temp', 'heat 500 to 1000 C'],
  ['boilers', 'heat below 100 C'], // must run after IES filename + doc-text handling
];
const NEWBAND = 'heat above 1000 C';
const FILE_RENAMES = [
  ['IES-boilers-', 'IES-heatbelow100-'],
  ['IES-nonboilerlow-', 'IES-heat100to200-'],
  ['IES-nonboilermed-', 'IES-heat200to500-'],
  ['IES-nonboilerhigh-', 'IES-heat500to1000-'],
];
const NEWBAND_FILE = 'IES-heatabove1000-';

function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function countOf(t, s) { return (t.match(new RegExp(esc(s), 'g')) || []).length; }
function assert(cond, msg) { if (!cond) { console.error('ASSERTION FAILED: ' + msg); process.exit(1); } }

// ---------- EPS.mdl ----------
let t = fs.readFileSync('EPS.mdl', 'latin1');
const NL = t.includes('\r\n') ? '\r\n' : '\n';
fs.writeFileSync('EPS.mdl.bak', t, 'latin1');
console.log('EPS.mdl backed up to EPS.mdl.bak (' + t.length + ' bytes, NL=' + JSON.stringify(NL) + ')');

// 1. IES filename references (12 fuels per process)
for (const [a, b] of FILE_RENAMES) {
  const n = countOf(t, a);
  assert(n === 12, `filename ${a}: expected 12 refs, found ${n}`);
  t = t.split(a).join(b);
}

// 2. Mask documentation prose mentioning boilers, reword after renames
const DOC_MASKS = [
  ['coal-powered boilers', 'coal-powered heating equipment'],
  ['things like ag boilers bc', 'things like ag heating equipment bc'],
];
DOC_MASKS.forEach(([a], i) => {
  const n = countOf(t, a);
  assert(n === 1, `doc phrase "${a}": expected 1, found ${n}`);
  t = t.split(a).join('@@DOCMASK' + i + '@@');
});

// 3. Element renames
for (const [a, b] of RENAMES) {
  const n = countOf(t, a);
  console.log(`rename "${a}" -> "${b}": ${n} occurrences`);
  assert(n > 0, `no occurrences of ${a}`);
  t = t.split(a).join(b);
}
DOC_MASKS.forEach(([, b], i) => { t = t.split('@@DOCMASK' + i + '@@').join(b); });

// 4. Subscript definitions: insert the fifth band
{
  // Industrial Process family: heating elements are followed by "cooling,"
  const target = `\theat 500 to 1000 C,${NL}\tcooling,`;
  const n = countOf(t, target);
  assert(n === 1, `Industrial Process def insert point: expected 1, found ${n}`);
  t = t.split(target).join(`\theat 500 to 1000 C,${NL}\t${NEWBAND},${NL}\tcooling,`);
  // industrial heating process subrange: last element, no trailing comma, then ~ line
  const target2 = `\theat 500 to 1000 C${NL}\t~`;
  const n2 = countOf(t, target2);
  assert(n2 === 1, `heating subrange insert point: expected 1, found ${n2}`);
  t = t.split(target2).join(`\theat 500 to 1000 C,${NL}\t${NEWBAND}${NL}\t~`);
}

// helper: locate a variable's equation block [start, end) — from the LHS at
// column 0 through the next unit-annotation line ("\n\t~")
function block(name) {
  const key = NL + name;
  const i = t.indexOf(key);
  assert(i >= 0, `variable not found: ${name}`);
  assert(t.indexOf(key, i + 1) === -1, `variable name not unique: ${name}`);
  const j = t.indexOf(NL + '\t~', i);
  assert(j > i, `no unit annotation after ${name}`);
  return [i, j];
}
function editBlock(name, fn) {
  const [i, j] = block(name);
  t = t.slice(0, i) + fn(t.slice(i, j)) + t.slice(j);
}

// 5. Five [Industry Category x Industrial Process] zero matrices: 10 -> 11 columns
const ROW10 = /(^|\r?\n)(\s*)((?:0,\s*){9})0;/g;
for (const v of [
  'Fraction of Eligible Industrial Energy Use Shifted to Electricity[',
  'Fraction of Eligible Industrial Energy Use Shifted to Alternate Fuel[',
  'Minimum Share of Start Year Industrial Equipment Retired[',
  'Perc Improvement in Eqpt Efficiency Stds Above BAU for Combustible Fuels[',
  'Perc Improvement in Eqpt Efficiency Stds Above BAU for Electricity[',
]) {
  editBlock(v, (b) => {
    let rows = 0;
    b = b.replace(ROW10, (m, p1, p2, p3) => { rows++; return `${p1}${p2}${p3}0,\t0;`; });
    assert(rows === 25, `${v}: expected 25 rows, transformed ${rows}`);
    return b;
  });
  console.log(`expanded 25x10 -> 25x11: ${v}`);
}

// 6. Perc Decrease in Cost of Capital for Clean Industrial Equipment [Process x Industry]: add row 5
editBlock('Perc Decrease in Cost of Capital for Clean Industrial Equipment[', (b) => {
  const re = /(\r?\n)(\s*)((?:0,\s*){24}0;)(\s*)\{heat 500 to 1000 C\}/;
  const m = b.match(re);
  assert(m, 'cost-of-capital: heat 500 to 1000 C row not found');
  return b.replace(re, `$1$2$3$4{heat 500 to 1000 C}$1$2$3$4{${NEWBAND}}`);
});
console.log('expanded 10x25 -> 11x25: Perc Decrease in Cost of Capital for Clean Industrial Equipment');

// 7. RnD Industry Capital Cost Perc Reduction [Process x Fuel]: rename comments, add row 5
editBlock('RnD Industry Capital Cost Perc Reduction[', (b) => {
  for (const [a, c] of [['{boilr}', '{<100 C}'], ['{low ht}', '{100-200 C}'], ['{med ht}', '{200-500 C}'], ['{hi ht}', '{500-1000 C}']]) {
    assert(b.includes(a), `RnD matrix: comment ${a} not found`);
    b = b.split(a).join(c);
  }
  const re = /(\r?\n)(\s*)((?:0,\s*){11}0;)(\s*)\{500-1000 C\}/;
  const m = b.match(re);
  assert(m, 'RnD matrix: 500-1000 C row not found');
  return b.replace(re, `$1$2$3$4{500-1000 C}$1$2$3$4{>1000 C}`);
});
console.log('expanded 10x12 -> 11x12: RnD Industry Capital Cost Perc Reduction');

// 8. Two [industrial heating process] levers: 4 -> 5 entries
for (const v of ['Perc Subsidy for Clean Industrial Heat Equipment[', 'Subsidy for Clean Industrial Heat Production[']) {
  editBlock(v, (b) => {
    const re = /(\r?\n)(\s*)0(\s*)\{heat 500 to 1000 C\}/;
    assert(re.test(b), `${v}: final heating entry not found`);
    return b.replace(re, `$1$2` + '0,' + `$3{heat 500 to 1000 C}$1$2` + '0' + `$3{${NEWBAND}}`);
  });
  console.log(`expanded 4 -> 5 entries: ${v}`);
}

// 9. Clone the 12 IES blocks of the 500-1000 band for the new >1000 band
{
  const re = /IES Industrial Equipment Shareweights\[Industry Category,[^\]]*?heat 500 to 1000 C[\s\\]*\][\s\S]*?\)\s*~~\|/g;
  const matches = t.match(re) || [];
  assert(matches.length === 12, `IES heat 500 to 1000 C blocks: expected 12, found ${matches.length}`);
  const clones = matches.map((m) =>
    m.split('heat 500 to 1000 C').join(NEWBAND).split('IES-heat500to1000-').join(NEWBAND_FILE)
  );
  const anchor = 'IES Industrial Equipment Shareweights[Industry Category,low carbon hydrogen if,other nonprocess';
  const i = t.indexOf(anchor);
  assert(i >= 0, 'final IES block anchor not found');
  t = t.slice(0, i) + clones.join(NL) + NL + t.slice(i);
  console.log('inserted 12 new IES equation blocks for ' + NEWBAND);
}

// 10. Sketch subscript-selection entries: add the new band next to the renamed one
{
  const target = `6:heat 500 to 1000 C${NL}`;
  const n = countOf(t, target);
  assert(n === 1, `sketch 6: entry: expected 1, found ${n}`);
  t = t.split(target).join(target + `6:${NEWBAND}${NL}`);
}

// 11. Post-conditions
{
  const leftovers = t.match(/^.*(nonboiler|\bboilers\b).*$/gim) || [];
  assert(leftovers.length === 0, 'leftover element-name lines:\n' + leftovers.join('\n'));
  const prose = t.match(/^.*boiler.*$/gim) || [];
  console.log('post-check: zero remaining element references; prose mentions of singular "boiler" left as-is: ' + prose.length);
  for (const [, b] of RENAMES) console.log(`  "${b}": ${countOf(t, b)} occurrences`);
  console.log(`  "${NEWBAND}": ${countOf(t, NEWBAND)} occurrences`);
}
fs.writeFileSync('EPS.mdl', t, 'latin1');
console.log('EPS.mdl written (' + t.length + ' bytes)');

// ---------- GraphDefinitions.vgd ----------
let g = fs.readFileSync('GraphDefinitions.vgd', 'latin1');
const GNL = g.includes('\r\n') ? '\r\n' : '\n';
fs.writeFileSync('GraphDefinitions.vgd.bak', g, 'latin1');
const VGD_RENAMES = [
  ['[boilers]|Boilers & Steam', '[heat below 100 C]|Heat Below 100 C'],
  ['[nonboiler low temp]|Nonboiler Low Temp', '[heat 100 to 200 C]|Heat 100-200 C'],
  ['[nonboiler med temp]|Nonboiler Med Temp', '[heat 200 to 500 C]|Heat 200-500 C'],
  ['[nonboiler high temp]|Nonboiler High Temp', '[heat 500 to 1000 C]|Heat 500-1000 C'],
];
for (const [a, b] of VGD_RENAMES) {
  const n = countOf(g, a);
  assert(n === 2, `vgd "${a}": expected 2, found ${n}`);
  g = g.split(a).join(b);
}
{
  const re = /(:VAR (Output [^\[\r\n]+)\[heat 500 to 1000 C\]\|Heat 500-1000 C\r?\n:Y-MIN 0\r?\n:DATASET \r?\n:LINE-COLOR 192-27-0)/g;
  let inserts = 0;
  g = g.replace(re, (m, whole, varname) => {
    inserts++;
    return whole + GNL + `:VAR ${varname}[${NEWBAND}]|Heat Above 1000 C${GNL}:Y-MIN 0${GNL}:DATASET ${GNL}:LINE-COLOR 128-27-96`;
  });
  assert(inserts === 2, `vgd inserts: expected 2, got ${inserts}`);
  assert(!/boiler/i.test(g), 'vgd still contains boiler references');
}
fs.writeFileSync('GraphDefinitions.vgd', g, 'latin1');
console.log('GraphDefinitions.vgd written: 8 series renamed, 2 new series added');
console.log('DONE');
