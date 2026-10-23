const $ = (id) => document.getElementById(id);
let current = null;
const cohortMeta = {
  dryad: {label:'Decker et al. · Dryad 2014', source:'WorldWideCattleDryad · DOI 10.5061/dryad.th092 · CC0. Bali: 20 hewan; total: 1.543 hewan dari 134 label ras.'},
  figshare: {label:'Sudrajad et al. · Figshare 2020', source:'Dataset pendamping sapi Indonesia · DOI 10.6084/m9.figshare.13083587 · CC BY 4.0. Bali: 16 hewan; total: 107 hewan dari lima populasi.'}
};
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function drawChart(rows){
  const svg=$('chart'), W=840,H=330,L=55,R=18,T=18,B=48, pw=W-L-R, ph=H-T-B;
  const ks=[...new Set(rows.map(r=>r.size))].sort((a,b)=>a-b); if(!ks.length){svg.innerHTML='';return}
  const x=(v)=>L+(ks.length===1?pw/2:ks.indexOf(v)/(ks.length-1)*pw), y=(v)=>T+(1-(v-.4)/.6)*ph;
  let html='';
  for(let tick=.4;tick<=1.0001;tick+=.1){const yy=y(tick);html+=`<line x1="${L}" y1="${yy}" x2="${W-R}" y2="${yy}" stroke="#e8efeb"/><text x="${L-10}" y="${yy+4}" text-anchor="end" fill="#80908d" font-size="10">${tick.toFixed(1)}</text>`}
  const chance=y(.5);html+=`<line x1="${L}" y1="${chance}" x2="${W-R}" y2="${chance}" stroke="#bac6c1" stroke-dasharray="5 5"/>`;
  for(const k of ks)html+=`<text x="${x(k)}" y="${H-20}" text-anchor="middle" fill="#80908d" font-size="10">${k}</text>`;
  html+=`<text x="${W/2}" y="${H-3}" text-anchor="middle" fill="#80908d" font-size="10">Jumlah SNP</text>`;
  const colors={'BantengPanel':'#087e72','Global-MAF':'#315779','Random-mean':'#c38e37'};
  for(const [method,color] of Object.entries(colors)){
    const pts=ks.map(k=>rows.find(r=>r.size===k&&r.method===method)).filter(Boolean);
    if(!pts.length)continue;
    html+=`<polyline fill="none" stroke="${color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points="${pts.map(p=>`${x(p.size)},${y(p.balancedAccuracyMean)}`).join(' ')}"/>`;
    for(const p of pts)html+=`<circle cx="${x(p.size)}" cy="${y(p.balancedAccuracyMean)}" r="4" fill="${color}"><title>${method}, ${p.size} SNP: ${p.balancedAccuracyMean.toFixed(3)} ± ${(p.balancedAccuracySD||0).toFixed(3)}</title></circle>`;
  }
  svg.innerHTML=html;
}
function render(data){
  current=data;const m=cohortMeta[data.dataset];
  $('stats').innerHTML=[['Hewan',data.nSamples,`${data.nBali} sampel Bali`],['Marker sumber',data.nMarkers.toLocaleString('id-ID'),'posisi UMD3.1'],['SNP Bali',data.nBali,'label BALI'],['Validasi',`${data.folds.length} fold`,'stratified berulang']].map(x=>`<div class="stat"><div class="stat-label">${x[0]}</div><div class="stat-value">${x[1]}</div><div class="stat-sub">${x[2]}</div></div>`).join('');
  $('source-copy').textContent=m.source;const rows=data.results||[];drawChart(rows);
  const at48=Object.fromEntries(rows.filter(r=>r.size===48).map(r=>[r.method,r]));
  if(at48.BantengPanel&&at48['Global-MAF']&&at48['Random-mean']){
    const bp=at48.BantengPanel.balancedAccuracyMean, gm=at48['Global-MAF'].balancedAccuracyMean, rn=at48['Random-mean'].balancedAccuracyMean;
    const delta=bp-gm, sign=delta>0?'di atas':'di bawah';
    $('finding').textContent=`Temuan pada 48 SNP: BantengPanel ${bp.toFixed(3)}, Global-MAF ${gm.toFixed(3)}, acak ${rn.toFixed(3)}. BantengPanel ${sign} Global-MAF sebesar ${Math.abs(delta).toFixed(3)}; hasil ini eksploratif.`;
  }else $('finding').textContent='Hasil 48 SNP belum tersedia untuk kohort ini.';
  $('results').innerHTML=rows.sort((a,b)=>a.size-b.size||a.method.localeCompare(b.method)).map(r=>`<tr><td>${r.size}</td><td><span class="method">${esc(r.method)}</span></td><td>${r.balancedAccuracyMean.toFixed(3)} ± ${(r.balancedAccuracySD||0).toFixed(3)}</td><td>${r.baliRecallMean.toFixed(3)}</td></tr>`).join('');
  $('robustness').innerHTML=(data.robustness||[]).map(r=>`<tr><td>${esc(r.scenario.replaceAll('_',' '))}</td><td>${Number(r.balancedAccuracyMean).toFixed(3)} ± ${(r.balancedAccuracySD||0).toFixed(3)}</td><td>${Number(r.baliRecallMean).toFixed(3)}</td><td>${r.folds}</td></tr>`).join('');
  const panel=Number($('panel-size').value), candidates=(data.selectedMarkers||[]).slice(0,panel);
  $('markers').innerHTML=candidates.map((r,i)=>`<tr><td>${i+1}</td><td>${esc(r.markerId)}</td><td>${esc(r.chromosome)}</td><td>${Number(r.position).toLocaleString('id-ID')}</td><td>${Number(r.score).toFixed(3)}</td></tr>`).join('');
  $('marker-link').href=`../../artifacts/public/${data.dataset}_panel_candidates.csv`;
  $('limitations').innerHTML=(data.limitations||[]).map(t=>`<div class="limit"><b>•</b><span>${esc(t)}</span></div>`).join('');
  $('csv-link').href=`../../artifacts/public/${data.dataset}_fold_results.csv`; $('error').classList.add('hidden');
}
async function load(){try{const name=$('cohort').value;const response=await fetch(`../../artifacts/public/${name}_benchmark.json`);if(!response.ok)throw Error(`Belum ada hasil untuk kohort ${name}. Jalankan pipeline lokal terlebih dahulu.`);render(await response.json())}catch(e){$('error').textContent=`Hasil belum dapat dimuat: ${e.message} Jalankan perintah di docs/RUNBOOK.md.`;$('error').classList.remove('hidden')}}
$('cohort').addEventListener('change',load);$('panel-size').addEventListener('change',()=>current&&render(current));load();
