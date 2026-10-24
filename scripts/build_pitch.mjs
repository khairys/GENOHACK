// Run a copy inside artifacts/qa/audited-pitch with the bundled artifact-tool node_modules.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const root=process.cwd(), work=path.join(root,'artifacts/qa/audited-pitch');
const publicOut=path.join(root,'artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pptx');
const buildStamp=String(Date.now());
const out=path.join(work,'validated-output',`pitch-${buildStamp}.pptx`);
const receipt=path.join(work,`validation-${buildStamp}.json`);
const skill='C:/Users/agath/.codex/plugins/cache/openai-primary-runtime/presentations/26.1022.11436/skills/presentations';
const runtimePython='C:/Users/agath/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const facts=JSON.parse(await fs.readFile(path.join(root,'artifacts/public/pitch_facts.json'),'utf8'));
const dry=facts.datasets.dryad, fig=facts.datasets.figshare, b=facts.business, v=b.inputs, d=b.derivedScenario;
if(facts.gitDirty!==false)throw Error('Pitch requires a clean-source scientific run');
const C={bg:'#F4F7F3',ink:'#16333A',muted:'#5D7273',teal:'#087E72',navy:'#315779',gold:'#C38E37',line:'#D8E4DE',white:'#FFFFFF'};
const p=Presentation.create({slideSize:{width:1280,height:720}});
const utils=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
function tx(s,value,x,y,w,h,size=26,color=C.ink,bold=false){
  if(value===undefined||String(value).includes('undefined'))throw Error('Unresolved slide value');
  const t=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  t.text=String(value);t.text.style={fontSize:size,typeface:'Arial',color,bold,wrap:'square',autoFit:'shrinkText',verticalAlignment:'middle',insets:{top:2,bottom:2,left:2,right:2}};return t;
}
function base(title,kicker,i){
  const s=p.slides.add();s.background.fill=C.bg;
  tx(s,kicker.toUpperCase(),72,35,1100,28,16,C.teal,true);
  tx(s,title,72,77,1120,88,44,C.ink,true);
  tx(s,'EXASTRA · GENOHACK 2026 · RISET KOMPUTASIONAL',72,677,970,22,13,C.muted);
  tx(s,String(i).padStart(2,'0'),1168,677,40,22,14,C.muted,true);return s;
}
function notes(s,i,sources=[]){s.speakerNotes.text=`${facts.timingsSeconds[i-1]} detik.\n\n${facts.speakerSegments[i-1].text}\n\nSumber: ${sources.join(' ; ')}\nAngka ilmiah: artifacts/public/pitch_facts.json; source ${facts.sourceCommit}.`;}
async function img(s,file,x,y,w,h,alt){const bytes=await fs.readFile(path.join(root,file));s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});}
function table(s,values,x,y,w,h,widths){
  const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});
  t.borders.assign({style:'solid',fill:C.line,width:1});
  for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.teal:C.white;cell.text.style={fontSize:22,typeface:'Arial',color:r===0?C.white:C.ink,bold:r===0,wrap:'square'};}
  return t;
}
const classify=(dataset,size,method)=>dataset.classification.find(r=>r.size===size&&r.method===method).balancedAccuracyMean;
const ancestry=(dataset,donor,size,method)=>dataset.ancestry.find(r=>r.donorBreed===donor&&r.size===size&&r.method===method);
const fmt=n=>Number(n).toFixed(3);

// 1 Intro
{
const s=base('BantengPanel','GENOHACK 2026 · Track 2',1);
tx(s,'Panel SNP minimal untuk\nriset ancestry sapi Bali',76,215,1100,150,58,C.ink,true);
tx(s,'Bukti dapat diaudit · data publik · prototipe riset',80,409,1060,55,27,C.teal);
tx(s,'Exastra  /  24 Oktober 2026',80,537,960,40,23,C.muted);
tx(s,'Belum merupakan uji kemurnian atau assay tervalidasi',80,598,1080,35,21,C.muted);
notes(s,1);
}
// 2 Story
{
const s=base('Sejarah populasi yang kompleks','Story dan urgensi',2);
tx(s,'Riset ancestry perlu membedakan\nlabel ras, referensi, dan bukti genetik.',78,205,1090,100,36,C.ink,true);
tx(s,'Literatur menunjukkan campuran zebu–banteng pada sejumlah populasi Indonesia.',80,337,1050,65,28,C.teal,true);
tx(s,'Hasil untuk Bali bervariasi menurut populasi dan metode. Status hewan individu perlu dikonfirmasi.',80,427,1050,75,27,C.muted);
tx(s,'Pertanyaan kami: berapa marker yang cukup informatif untuk riset ancestry, sebelum validasi independen?',80,538,1070,75,28,C.ink,true);
tx(s,'Mohamad 2009 · Sudrajad 2020 · Wang 2025',80,628,1080,26,16,C.muted);
notes(s,2,['https://doi.org/10.1371/journal.pone.0005490','https://doi.org/10.1371/journal.pone.0241038','https://doi.org/10.1038/s41467-025-62692-z']);
}
// 3 Customer
{
const s=base('Pengguna dan kebutuhan yang akan diuji','Customer / pain / validasi',3);
tx(s,'PENGGUNA',80,209,450,30,18,C.teal,true);tx(s,'Analis genetika ternak\ndan peneliti pemuliaan',80,254,490,100,31,C.ink,true);
tx(s,'PEMBELI / CHAMPION',666,209,490,30,18,C.teal,true);tx(s,'Kepala lab atau program\n/ peneliti pemuliaan',666,254,490,100,31,C.ink,true);
tx(s,'Hipotesis pain: desain marker dan peninjauan ancestry sulit diaudit ketika metode, data, dan batas klaim terpisah.',80,389,1090,85,28,C.muted);
tx(s,`${b.customerEvidence.customerInterviews} wawancara pelanggan · ${b.customerEvidence.expertInterviews} wawancara pakar · ${b.customerEvidence.lettersOfIntent} LOI`,80,501,1100,55,31,C.gold,true);
tx(s,'BPTU-HPT Denpasar: contoh institusi relevan dari situs resmi; belum menjadi pelanggan atau mitra.',80,578,1100,60,21,C.muted);
notes(s,3,['https://bptuhptdenpasar.ditjenpkh.pertanian.go.id/faq','docs/VALIDATION_LOG.md','configs/business.json']);
}
// 4 Solution and QC
{
const s=base('Dari genotipe menjadi bukti panel','Solusi dan kedalaman teknis',4);
const steps=[['Data','Dryad / Figshare'],['QC','Sampel / SNP'],['Ranking','Training saja'],['Uji','Baseline setara'],['Tinjau','PCA / CSV / S1']];
steps.forEach(([a,b],i)=>{tx(s,String(i+1).padStart(2,'0'),80+i*226,211,170,53,39,C.gold,true);tx(s,a,80+i*226,279,200,42,28,C.teal,true);tx(s,b,80+i*226,330,205,60,22,C.muted);});
tx(s,`${dry.nSamples.toLocaleString('id-ID')} Dryad · ${dry.nBali} Bali          ${fig.nSamples} Figshare · ${fig.nBali} Bali`,80,422,1090,56,34,C.ink,true);
const q=facts.processingQC.dryad;
tx(s,`Dryad: ${q.excludedSamplesAboveMissingThreshold} sampel >10% missing dikeluarkan; ${q.excludedNonAutosomalMarkers} marker non-autosomal dikeluarkan.`,80,496,1100,53,23,C.muted);
tx(s,'Kohort terpisah · SNP 8–200 · 20 fold · 30 random panel · jarak 250 kb untuk semua metode',80,568,1100,60,24,C.teal,true);
notes(s,4,['docs/SCIENTIFIC_PROTOCOL.md','artifacts/public/benchmark.json']);
}
// 5 Live demo
{
const s=base('Demo live: panel, ancestry, dan bukti','Solution & demo · 75 detik',5);
await img(s,'artifacts/public/figures/dashboard_s1.png',70,183,810,455,'Tampilan dashboard aktual: simulasi S1 dengan donor ONG');
tx(s,'01  Pilih kohort\n02  Bandingkan donor\n03  Tinjau PCA\n04  Unduh marker',916,216,300,244,26,C.ink,true);
tx(s,'Cadangan lokal:\nvideo 2 menit\ndan ZIP offline',916,499,285,100,22,C.muted);
tx(s,facts.liveDemo,80,638,1120,26,16,C.teal,true);
notes(s,5,[facts.liveDemo,'docs/RUNBOOK.md']);
}
// 6 Scientific evidence
{
const s=base('Panel informatif pada simulasi S1','Bukti · eksploratif',6);
const sizes=[8,16,24,48,72,96,128,156,200],methods=['BantengPanel','Global-MAF','Random-mean'],colors=[C.teal,C.navy,C.gold];
const chart=s.charts.add('line',{position:{left:72,top:187,width:715,height:345},title:'Dryad × ONG · MAE estimasi q',titleTextStyle:{fontSize:21,fill:C.ink,bold:true},categories:sizes.map(String),series:methods.map((name,i)=>({name,values:sizes.map(k=>Number(ancestry(dry,'ONG',k,name).maeMean.toFixed(3))),line:{fill:colors[i],width:3},marker:{symbol:'circle',size:5,fill:colors[i]}})),hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{fontSize:14,fill:C.ink}},xAxis:{title:{text:'Jumlah SNP',textStyle:{fontSize:14,fill:C.ink}},textStyle:{fontSize:12,fill:C.muted},majorGridlines:null},yAxis:{title:{text:'MAE · lebih rendah lebih baik',textStyle:{fontSize:14,fill:C.ink}},min:0,max:.25,majorUnit:.05,numberFormatCode:'0.00',textStyle:{fontSize:12,fill:C.muted},majorGridlines:{fill:C.line,width:1}},chartFill:C.white,plotAreaFill:C.white});
utils.applyPresentationChartFont(chart,{fontFamily:'Arial'});
await img(s,'artifacts/public/figures/dryad_pca.png',818,194,390,260,'PCA deskriptif Dryad; hewan atipikal perlu konfirmasi');
tx(s,`${dry.atypical.length} hewan Bali perlu konfirmasi\nPCA dan skor bukan bukti introgresi`,835,460,360,73,20,C.muted);
tx(s,`48 SNP: MAE ${fmt(ancestry(dry,'ONG',48,'BantengPanel').maeMean)} vs ${fmt(ancestry(dry,'ONG',48,'Global-MAF').maeMean)} (Global-MAF)`,80,552,1110,36,25,C.teal,true);
tx(s,`Sanity check Dryad 8 SNP: BA ${fmt(classify(dry,8,'BantengPanel'))} vs ${fmt(classify(dry,8,'Global-MAF'))}. Keunggulan biner umum belum terbukti.`,80,594,1110,40,19,C.muted);
tx(s,'Simulasi tanpa linkage; q relatif/pedigree; kontrol sedikit, fold tumpang tindih. Bukan validasi ternak nyata.',80,641,1110,24,15,C.gold,true);
notes(s,6,['artifacts/public/dryad_ancestry.json','artifacts/public/dryad_atypical_samples.csv','docs/SCIENTIFIC_PROTOCOL.md']);
}
// 7 TAM ROI Financials
{
const s=base('Skenario pasar dan ekonomi proyek','TAM / ROI / finansial · semua input asumsi',7);
tx(s,`${v.institutions.value} institusi × ${v.projectsPerInstitutionPerYear.value} proyek × Rp${v.pricePerProject.value} juta`,80,209,1110,58,36,C.ink,true);
tx(s,`= Rp${d.potentialRevenueMillionIDR.toFixed(0)} juta / tahun`,80,278,1110,74,49,C.teal,true);
tx(s,'Skenario ilustratif; jumlah pembeli, frekuensi proyek dan harga belum tervalidasi. TAM/SAM/SOM terukur belum tersedia.',80,365,1090,75,24,C.muted);
tx(s,`Margin kotor ${(d.grossMargin*100).toFixed(0)}%`,80,474,360,56,34,C.ink,true);
tx(s,`CAC Rp${d.cacMillionIDR.toFixed(0)} juta`,468,474,350,56,34,C.ink,true);
tx(s,`LTV/CAC ${d.ltvCacRatio.toFixed(2)}×`,865,474,340,56,34,C.gold,true);
tx(s,`Biaya langsung asumsi Rp${v.directCostPerProject.value} juta/proyek. LTV 2 tahun, diskonto 10%. Rasio belum mencapai sasaran internal 3×.`,80,551,1100,65,22,C.muted);
tx(s,'ROI assay belum dihitung: perlu penawaran biaya dan kinerja laboratorium.',80,627,1100,30,20,C.teal,true);
notes(s,7,['configs/business.json','docs/BUSINESS_MODEL.md']);
}
// 8 Competition, native 2x2
{
const s=base('Alternatif desain dan penggunaan','Kompetisi · peta kualitatif 2 × 2',8);
const t=table(s,[['Target desain','Marker banyak','Marker sedikit / nol'],['Genetik umum','Chip genome-wide\nBovineSNP50','Parentage: tugas pedigree\n(validasi berbeda)'],['Bali / proyek khusus','Analisis genom\noleh peneliti','BantengPanel: desain riset\nFenotipe: tanpa ancestry DNA']],80,210,1120,330,[260,410,450]);
t.rows[0].height=68;t.rows[1].height=131;t.rows[2].height=131;
tx(s,'Diferensiasi yang diuji: panel riset yang mempertimbangkan referensi populasi dan menyimpan bukti per fold.',80,568,1090,65,25,C.teal,true);
tx(s,'Tidak ada klaim harga pesaing, kesetaraan tugas parentage, atau assay lebih murah.',80,636,1090,26,17,C.muted);
notes(s,8,['https://www.illumina.com/products/by-type/microarray-kits/bovine-snp50.html','docs/BUSINESS_MODEL.md']);
}
// 9 GTM
{
const s=base('Adopsi bertahap melalui proyek desain','GTM / DMU / model bisnis',9);
const stages=[['01','Discovery','Wawancara pengguna/pembeli,\nreview genetika dan akses data'],['02','Jasa per proyek','Freeze scope dan kriteria penerimaan;\nharga setelah penawaran nyata'],['03','Pilot assay','Review probe dan uji lab;\nkemudian pilot prospektif']];
stages.forEach(([n,a,b],i)=>{const y=205+i*119;tx(s,n,82,y,90,57,38,C.gold,true);tx(s,a,203,y,285,58,29,C.teal,true);tx(s,b,528,y,650,80,26,C.ink);});
tx(s,'Champion: peneliti · pembeli: kepala lab/program · veto: data, mutu dan pengadaan',80,574,1100,48,23,C.muted);
tx(s,'Langganan setelah penggunaan berulang terbukti. Belum ada pendanaan atau kemitraan yang diklaim.',80,628,1100,34,19,C.muted);
notes(s,9,['docs/BUSINESS_MODEL.md','docs/EXECUTION_ROADMAP.md']);
}
// 10 Team and contribution boundary
{
const s=base('Tim Exastra dan kontribusi hackathon','Tim / pre-existing vs selama hackathon',10);
tx(s,'ANGGOTA TIM',80,201,480,30,18,C.teal,true);
facts.team.members.forEach((name,i)=>tx(s,name,80,249+i*50,510,40,26,C.ink,true));
tx(s,'SEBELUM KICKOFF',670,201,500,30,18,C.teal,true);
tx(s,'Ide/proposal awal, sumber publik\ndan materi referensi bootcamp',670,247,510,80,27,C.ink);
tx(s,'SELAMA HACKATHON',670,366,500,30,18,C.teal,true);
tx(s,'Pipeline, benchmark, S1, PCA,\ndashboard dan paket pitch\nSource tag: mvp-v1.0-source',670,407,510,118,25,C.ink);
tx(s,'Alur kerja yang diusulkan: metode/QC · komputasi/produk · assay/kemitraan · pelanggan/bisnis',80,549,1100,52,21,C.muted);
tx(s,'Advisor: genetika populasi, assay SNP, ekonomi lab. Peran, kualifikasi, dan waktu penulisan perlu konfirmasi tim.',80,611,1100,51,20,C.gold,true);
notes(s,10,['configs/team.json','docs/CONTRIBUTIONS.md']);
}
// 11 Roadmap and ask
{
const s=base('Validasi berikutnya dan dukungan yang dicari','Summary / roadmap / ask',11);
tx(s,'1–3 bulan',80,211,200,43,27,C.teal,true);tx(s,'Kohort independen, metadata kinship, desain kalibrasi',304,207,880,60,28,C.ink);
tx(s,'4–6 bulan',80,307,200,43,27,C.teal,true);tx(s,'Freeze panel, ambang independen, validasi eksternal',304,303,880,60,28,C.ink);
tx(s,'7–12 bulan',80,403,200,43,27,C.teal,true);tx(s,'Review probe, uji assay, lalu pilot prospektif',304,399,880,60,28,C.ink);
tx(s,'ASK: satu kohort Bali bermetadata · satu mitra assay · introduksi calon pembeli',80,510,1110,74,30,C.teal,true);
tx(s,'Bukti dapat diaudit. Hasil negatif tetap terlihat. Keuntungan simulasi diuji lagi pada ternak nyata.',80,610,1100,50,24,C.ink,true);
notes(s,11,['docs/EXECUTION_ROADMAP.md']);
}
await fs.mkdir(work,{recursive:true});await fs.mkdir(path.dirname(out),{recursive:true});
for(const [i,s] of p.slides.items.entries()){
  const blob=await p.export({slide:s,format:'png',scale:1.5});
  await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const draft=path.join(work,'draft.pptx');await(await PresentationFile.exportPptx(p)).save(draft);
const finalization=await utils.finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath:out,pythonExecutable:runtimePython,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','8'],
 explicitTotalSlideCount:11,requiredNativeTableOwnerSlides:[8],requiredNativeChartOwnerSlides:[6],materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:receipt,expectedSlideSizeEmu:'12192000,6858000'});
await fs.mkdir(path.dirname(publicOut),{recursive:true});
await fs.copyFile(out,publicOut);
await fs.copyFile(receipt,path.join(work,'validation.json'));
console.log(JSON.stringify({out:publicOut,slides:p.slides.items.length,finalization}));
