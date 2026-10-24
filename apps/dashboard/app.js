const $ = (id) => document.getElementById(id);
let current = null;
const cohortMeta = {
  dryad: {label:'Decker et al. · Dryad 2014', source:'WorldWideCattleDryad · DOI 10.5061/dryad.th092 · CC0. Sumber: 1.543 hewan; setelah QC: 1.542, termasuk 20 Bali. 134 label ras sumber.'},
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
  const eligible=Math.round(data.folds.reduce((s,f)=>s+f.eligibleMarkers,0)/data.folds.length);
  $('stats').innerHTML=[['Hewan setelah QC',data.nSamples,`${data.nBali} hewan Bali`],['Marker autosomal',data.nMarkers.toLocaleString('id-ID'),'posisi UMD3.1'],['SNP eligible',eligible.toLocaleString('id-ID'),'rerata training fold'],['Validasi',`${data.folds.length} fold`,'stratified berulang']].map(x=>`<div class="stat"><div class="stat-label">${x[0]}</div><div class="stat-value">${x[1]}</div><div class="stat-sub">${x[2]}</div></div>`).join('');
  $('source-copy').textContent=m.source;const rows=data.results||[];drawChart(rows);
  const at48=Object.fromEntries(rows.filter(r=>r.size===48).map(r=>[r.method,r]));
  if(at48.BantengPanel&&at48['Global-MAF']&&at48['Random-mean']){
    const bp=at48.BantengPanel.balancedAccuracyMean, gm=at48['Global-MAF'].balancedAccuracyMean, rn=at48['Random-mean'].balancedAccuracyMean;
    const delta=bp-gm;
    const relation=Math.abs(delta)<.0005?'setara pada pembulatan tiga desimal':`${delta>0?'di atas':'di bawah'} Global-MAF sebesar ${Math.abs(delta).toFixed(3)}`;
    const p8=(data.pairedComparisons||[]).find(r=>r.size===8);
    $('finding').textContent=`48 SNP: BantengPanel ${bp.toFixed(3)}, Global-MAF ${gm.toFixed(3)}, acak ${rn.toFixed(3)}; ${relation}. ${p8?`Pada 8 SNP: menang/seri/kalah ${p8.wins}/${p8.ties}/${p8.losses} fold vs Global-MAF.`:''} Fold saling tumpang tindih; hasil eksploratif.`;
  }else $('finding').textContent='Hasil 48 SNP belum tersedia untuk kohort ini.';
  $('results').innerHTML=rows.sort((a,b)=>a.size-b.size||a.method.localeCompare(b.method)).map(r=>`<tr><td>${r.size}</td><td><span class="method">${esc(r.method)}</span></td><td>${r.balancedAccuracyMean.toFixed(3)} ± ${(r.balancedAccuracySD||0).toFixed(3)}</td><td>${r.baliRecallMean.toFixed(3)}</td></tr>`).join('');
  $('robustness').innerHTML=(data.robustness||[]).map(r=>`<tr><td>${r.scenario.startsWith('missing')?'Genotipe hilang':'Kesalahan genotipe'} ${Number(r.scenario.split('_').at(-1))}%</td><td>${Number(r.balancedAccuracyMean).toFixed(3)} ± ${(r.balancedAccuracySD||0).toFixed(3)}</td><td>${Number(r.baliRecallMean).toFixed(3)}</td><td>${r.folds}</td></tr>`).join('');
  const panel=Number($('panel-size').value), candidates=(data.selectedMarkers||[]).slice(0,panel);
  $('markers').innerHTML=candidates.map((r,i)=>`<tr><td>${i+1}</td><td>${esc(r.markerId)}</td><td>${esc(r.chromosome)}</td><td>${Number(r.position).toLocaleString('id-ID')}</td><td>${Number(r.score).toFixed(3)}</td></tr>`).join('');
  $('marker-link').href=`../../artifacts/public/${data.dataset}_panel_candidates.csv`;
  $('limitations').innerHTML=(data.limitations||[]).map(t=>`<div class="limit"><b>•</b><span>${esc(t)}</span></div>`).join('');
  $('csv-link').href=`../../artifacts/public/${data.dataset}_fold_results.csv`; $('error').classList.add('hidden');
  renderAncestry();renderPca(data);
}
function renderAncestry(){
  if(!current?.ancestry)throw Error('Artefak S1 belum tersedia. Gunakan bundle protokol 2.0.');
  const donor=$('donor').value, rows=current.ancestry.results.filter(r=>r.donorBreed===donor), keys=[...new Set(rows.map(r=>r.size))].sort((a,b)=>a-b);
  const W=840,H=330,L=55,R=18,T=18,B=48,pw=W-L-R,ph=H-T-B;
  const maximum=Math.max(.10,...rows.map(r=>r.maeMean))*1.15;
  const x=v=>L+keys.indexOf(v)/(keys.length-1)*pw,y=v=>T+(1-v/maximum)*ph;
  let html='';for(let i=0;i<=5;i++){const v=maximum*i/5;html+=`<line x1="${L}" y1="${y(v)}" x2="${W-R}" y2="${y(v)}" stroke="#e0e9e6"/><text x="${L-9}" y="${y(v)+4}" text-anchor="end" fill="#6b7d80" font-size="11">${v.toFixed(2)}</text>`}
  for(const k of keys)html+=`<text x="${x(k)}" y="${H-20}" text-anchor="middle" fill="#6b7d80" font-size="11">${k}</text>`;
  html+=`<text x="420" y="327" text-anchor="middle" fill="#6b7d80" font-size="11">Jumlah SNP · MAE lebih rendah lebih baik</text>`;
  for(const [method,color] of Object.entries({'BantengPanel':'#087e72','Global-MAF':'#315779','Random-mean':'#c38e37'})){
    const pts=rows.filter(r=>r.method===method).sort((a,b)=>a.size-b.size);html+=`<polyline fill="none" stroke="${color}" stroke-width="2.5" points="${pts.map(p=>`${x(p.size)},${y(p.maeMean)}`).join(' ')}"/>`;
    for(const p of pts)html+=`<circle cx="${x(p.size)}" cy="${y(p.maeMean)}" r="4" fill="${color}"><title>${method}, ${p.size} SNP; MAE ${p.maeMean.toFixed(3)}</title></circle>`;
  }
  $('ancestry-chart').innerHTML=html;
  $('ancestry-results').innerHTML=rows.map(r=>`<tr><td>${r.size}</td><td>${esc(r.method)}</td><td>${r.maeMean.toFixed(3)} ± ${(r.maeSD||0).toFixed(3)}</td><td>${r.bc2SensitivityAt95SpecificityMean.toFixed(3)}</td><td>${r.achievedSpecificityMean.toFixed(3)}</td></tr>`).join('');
  const at48=rows.filter(r=>r.size===48);$('ancestry-finding').textContent=`Simulasi Bali × ${donor}, 48 SNP: ${at48.map(r=>`${r.method} MAE ${r.maeMean.toFixed(3)}`).join(' · ')}. ${current.ancestry.offspringPerGenerationPerFold} keturunan per generasi/donor/fold; metode memakai hewan simulasi yang sama.`;
  $('ancestry-link').href=`../../artifacts/public/${current.dataset}_ancestry_summary.csv`;
}
function renderPca(data){
  const pop=data.population;if(!pop)throw Error('Artefak PCA belum tersedia.');
  const points=pop.points, breeds=pop.includedBreeds, colors=['#087e72','#c38e37','#315779','#a25b70','#5b8e8e','#7063a1','#90742f','#7a9d47','#9b6545','#676a70'];
  const xs=points.map(p=>p.pc1),ys=points.map(p=>p.pc2),xmin=Math.min(...xs),xmax=Math.max(...xs),ymin=Math.min(...ys),ymax=Math.max(...ys),x=v=>65+(v-xmin)/(xmax-xmin||1)*720,y=v=>355-(v-ymin)/(ymax-ymin||1)*300;
  let svg=`<line x1="55" y1="365" x2="800" y2="365" stroke="#cad9d3"/><line x1="55" y1="40" x2="55" y2="365" stroke="#cad9d3"/>`;
  for(const p of points){svg+=`<circle cx="${x(p.pc1)}" cy="${y(p.pc2)}" r="${p.atypicalReview?6:4}" fill="${colors[breeds.indexOf(p.breed)%colors.length]}" stroke="${p.atypicalReview?'#152b32':'white'}" stroke-width="${p.atypicalReview?2:0.6}"><title>${esc(p.sampleId)} · ${esc(p.breed)}${p.atypicalReview?' · perlu konfirmasi':''}</title></circle>`;}
  svg+=`<text x="420" y="398" text-anchor="middle" font-size="13" fill="#6b7d80">PC1 (${(100*pop.explainedVarianceRatio[0]).toFixed(1)}%)</text><text x="12" y="205" transform="rotate(-90 12 205)" text-anchor="middle" font-size="13" fill="#6b7d80">PC2 (${(100*pop.explainedVarianceRatio[1]).toFixed(1)}%)</text>`;
  $('pca-chart').innerHTML=svg;$('pca-copy').textContent=`${pop.nAnimals} hewan · ${pop.nMarkers} SNP dengan jarak minimum 250 kb · QC dan imputasi rerata pada subset seluruh kohort untuk deskripsi. PCA ini tidak dipakai untuk memilih atau memvalidasi panel.`;
  $('pca-legend').innerHTML=breeds.map((b,i)=>`<span><i class="dot" style="background:${colors[i%colors.length]}"></i>${esc(b)}</span>`).join('');
  const reviewed=(data.atypicalSamples||[]).filter(r=>r.breed==='BALI').sort((a,b)=>b.misclassifiedRepeats-a.misclassifiedRepeats||a.baliSimilarity-b.baliSimilarity);
  $('atypical').innerHTML=reviewed.slice(0,5).map(r=>`<tr><td>${esc(r.sampleId)}${r.atypicalReview?' · tinjau':''}</td><td>${r.misclassifiedRepeats} / ${r.evaluations}</td><td>${r.baliSimilarity.toFixed(3)}</td></tr>`).join('');
  $('pca-link').href=`../../artifacts/public/${data.dataset}_pca.csv`;
}
function business(){
  const read=id=>{const e=$(id),n=Number(e.value);return Math.min(Number(e.max),Math.max(Number(e.min),Number.isFinite(n)?n:Number(e.min)))};
  const n=read('biz-institutions'),projects=read('biz-projects'),price=read('biz-price'),cost=read('biz-cost'),sales=read('biz-sales'),customers=read('biz-customers');
  const market=n*projects*price,margin=(price-cost)/price,cac=sales/customers,ltv=(price-cost)*projects*(1/1.1+1/1.1**2);
  $('business-output').textContent=`Skenario pendapatan potensial: Rp${market.toLocaleString('id-ID')} juta/tahun (${n} × ${projects} × Rp${price} juta). Margin kotor ${(margin*100).toFixed(1)}%. CAC Rp${cac.toFixed(1)} juta. LTV 2 tahun Rp${ltv.toFixed(1)} juta; LTV/CAC ${cac>0?(ltv/cac).toFixed(2)+'×':'tidak terdefinisi saat CAC nol'}. Semua input adalah asumsi; bukan traksi atau proyeksi tervalidasi.`;
}
let manifestPromise;
async function load(){try{
  manifestPromise ||= fetch('../../artifacts/public/benchmark.json',{cache:'no-cache'}).then(async r=>{if(!r.ok)throw Error('Laporan benchmark tidak tersedia');const m=await r.json();if(m.protocolVersion!=='2.0.0'||!Array.isArray(m.datasets))throw Error('Versi artefak tidak cocok dengan dashboard');return m});
  const m=await manifestPromise,name=$('cohort').value,data=m.datasets.find(d=>d.dataset===name);if(!data?.ancestry||!data?.population)throw Error('Bundle analisis belum lengkap');render(data);
  $('provenance-copy').textContent=`Protokol ${m.protocolVersion} · source commit ${m.gitCommit.slice(0,12)} · dirty saat run: ${m.gitDirty} · dibuat ${m.generatedAt}.`;
}catch(e){manifestPromise=null;$('error').textContent=`Hasil belum dapat dimuat: ${e.message}. Lihat docs/RUNBOOK.md untuk build lokal.`;$('error').classList.remove('hidden')}}
$('cohort').addEventListener('change',load);$('panel-size').addEventListener('change',()=>current&&render(current));$('donor').addEventListener('change',()=>current&&renderAncestry());
document.querySelectorAll('.calculator input').forEach(e=>e.addEventListener('input',business));business();load();
