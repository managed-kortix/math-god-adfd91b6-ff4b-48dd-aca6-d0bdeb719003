#!/usr/bin/env node
// Independent strict Boolean-matrix verifier.
const fs = require('fs');
const crypto = require('crypto');

function fail(s) { throw new Error(s); }
function decimal(s) { return /^(0|[1-9][0-9]*)$/.test(s); }
function parse(buf) {
  const text = buf.toString('utf8');
  if (Buffer.from(text, 'utf8').compare(buf) !== 0 || text.includes('\0') || text.includes('\r')) fail('bad bytes');
  const lines = text.split('\n');
  if (lines.at(-1) === '') lines.pop();
  if (!lines.length || !decimal(lines[0])) fail('bad n');
  const n = Number(lines[0]);
  if (!Number.isSafeInteger(n) || n < 1) fail('n must be positive safe integer');
  const A = Array.from({length:n}, () => Array(n).fill(false));
  let previous = null;
  const arcs = [];
  for (const line of lines.slice(1)) {
    const f = line.split(' ');
    if (f.length !== 2 || !f.every(decimal)) fail('bad arc line');
    const u = Number(f[0]), v = Number(f[1]);
    if (![u,v].every(Number.isSafeInteger) || u >= n || v >= n || u === v) fail('bad endpoint or loop');
    if (previous && !(previous[0] < u || (previous[0] === u && previous[1] < v))) fail('not sorted');
    if (A[v][u]) fail('digon');
    A[u][v] = true; arcs.push([u,v]); previous = [u,v];
  }
  const normalized = `${n}\n` + arcs.map(e => `${e[0]} ${e[1]}\n`).join('');
  return {n,A,normalized};
}
function neighborhoods(n,A) {
  const n1=[], n2=[];
  for (let v=0; v<n; ++v) {
    const one=[], two=[];
    for (let z=0; z<n; ++z) {
      let r2=false;
      for (let y=0; y<n; ++y) r2 ||= A[v][y] && A[y][z];
      if (A[v][z]) one.push(z);
      if (z !== v && !A[v][z] && r2) two.push(z);
    }
    n1.push(one); n2.push(two);
  }
  return {n1,n2};
}
try {
  const {n,A,normalized}=parse(fs.readFileSync(process.argv[2]));
  const {n1,n2}=neighborhoods(n,A);
  let pass=true;
  for (let v=0; v<n; ++v) {
    const margin=n1[v].length-n2[v].length; pass &&= margin>0;
    console.log(`${v}: N1=[${n1[v]}] N2=[${n2[v]}] d1=${n1[v].length} d2=${n2[v].length} margin=${margin}`);
  }
  console.log('sha256='+crypto.createHash('sha256').update(normalized).digest('hex'));
  console.log(pass?'PASS':'FAIL'); process.exit(pass?0:1);
} catch(e) { console.error('ERROR: '+e.message); process.exit(2); }
