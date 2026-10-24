"""Publish business assumptions and pitch facts from measured artifacts only."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "artifacts/public"
m = json.loads((PUBLIC / "benchmark.json").read_text())
business = json.loads((ROOT / "configs/business.json").read_text())
team = json.loads((ROOT / "configs/team.json").read_text())
v = {k: s["value"] for k, s in business["inputs"].items()}
gross = v["pricePerProject"] - v["directCostPerProject"]
cac = v["salesMarketingPerPeriod"] / v["newCustomersPerPeriod"]
ltv = sum(gross*v["projectsPerInstitutionPerYear"]/(1+v["discountRate"])**year for year in range(1, int(v["retentionYears"])+1))
business["derivedScenario"] = {"potentialRevenueMillionIDR": v["institutions"]*v["projectsPerInstitutionPerYear"]*v["pricePerProject"],
                               "grossMargin": gross/v["pricePerProject"], "cacMillionIDR": cac,
                               "ltvMillionIDR": ltv, "ltvCacRatio": ltv/cac,
                               "evidence": "calculated_from_unvalidated_assumptions"}
(PUBLIC / "business_scenario.json").write_text(json.dumps(business, indent=2), encoding="utf-8")
facts = {"sourceCommit": m["gitCommit"], "gitDirty": m["gitDirty"], "protocolVersion": m["protocolVersion"],
         "processingQC": m["processingQC"], "business": business, "team": team,
         "liveDemo": "https://bantengpanel-genohack.toastygecko1026.chatgpt.site",
         "repository": "https://github.com/khairys/GENOHACK", "timingsSeconds": [15,30,35,25,75,45,25,20,25,20,25],
         "datasets": {}}
for d in m["datasets"]:
    facts["datasets"][d["dataset"]] = {
        "nBali": d["nBali"], "nSamples": d["nSamples"], "nMarkers": d["nMarkers"],
        "classification": d["results"], "paired": d["pairedComparisons"],
        "atypical": [r for r in d["atypicalSamples"] if r["atypicalReview"]],
        "ancestry": d["ancestry"]["results"], "pca": {k: val for k, val in d["population"].items() if k != "points"}}
(PUBLIC / "pitch_facts.json").write_text(json.dumps(facts, indent=2, allow_nan=False), encoding="utf-8")
dry = facts["datasets"]["dryad"]
f8 = next(r for r in dry["paired"] if r["size"] == 8)
f48 = {r["method"]: r for r in dry["classification"] if r["size"] == 48}
s1 = {r["method"]: r for r in dry["ancestry"] if r["size"] == 48 and r["donorBreed"] == "ONG"}
segments = [
 ("Intro", "Kami tim Exastra, membangun BantengPanel: prototipe desain panel SNP minimal untuk riset ancestry sapi Bali. Hari ini kami menunjukkan pipeline, data, dan batas buktinya."),
 ("Story", "Ternak Indonesia mempunyai sejarah campuran zebu dan banteng yang kompleks. Literatur memberi alasan untuk menilai referensi populasi dengan hati-hati. Sebagian studi tidak menemukan introgresi zebu pada Bali yang diteliti, sedangkan studi genom terbaru menemukan beberapa individu hibrida. Kita tidak boleh menggeneralisasi bahwa semua Bali tidak murni."),
 ("Pelanggan dan pain", "Calon pengguna kami adalah analis genetika dan peneliti ternak, dengan kepala lab atau program sebagai calon pembeli. BPTU-HPT Denpasar adalah contoh institusi pembibitan Bali yang relevan menurut situs resminya, belum pelanggan kami. Saat ini ada nol wawancara, nol LOI dan nol pilot berbayar. Validasi kebutuhan serta anggaran tetap perlu dilakukan."),
 ("Solusi", "Dua kohort publik diverifikasi dan dianalisis terpisah karena kode alelnya berbeda. Setiap fold memilih marker hanya di training. BantengPanel dibandingkan dengan Global-MAF dan tiga puluh panel acak pada ukuran dan aturan jarak yang sama. Kami menambahkan simulasi Mendelian dan PCA deskriptif."),
 ("Demo live", "Buka demo. Tunjukkan sumber commit dan jumlah hewan. Pilih referensi ONG, baca kurva MAE simulasi: lebih rendah lebih baik. Ganti donor MAD untuk menunjukkan pengaruh referensi. Buka PCA dan hewan yang perlu konfirmasi. Tunjukkan benchmark 8 SNP, ubah ukuran marker, unduh CSV. Ganti kohort ke Figshare. Bila jaringan gagal, gunakan video dua menit atau bundle offline."),
 ("Bukti", f"Di Dryad, panel delapan SNP menang atas Global-MAF pada {f8['wins']} dari {f8['folds']} fold, seri {f8['ties']} dan kalah {f8['losses']}. Pada empat puluh delapan SNP, balanced accuracy BantengPanel {f48['BantengPanel']['balancedAccuracyMean']:.3f}, dibanding {f48['Global-MAF']['balancedAccuracyMean']:.3f} untuk Global-MAF. S1 Dryad versus ONG pada ukuran sama memberi MAE {s1['BantengPanel']['maeMean']:.3f} dan {s1['Global-MAF']['maeMean']:.3f}. Hasil lengkap tetap ditampilkan untuk semua donor dan metode. Hewan atipikal bukan bukti introgresi. Simulasi bukan validasi lapangan."),
 ("TAM, ROI dan finansial", f"Jumlah pasar dan willingness-to-pay belum tervalidasi. Skenario asumsi sepuluh institusi, dua proyek per tahun, harga lima belas juta menghasilkan potensi {business['derivedScenario']['potentialRevenueMillionIDR']:.0f} juta per tahun. Margin skenario {100*business['derivedScenario']['grossMargin']:.0f} persen dan LTV terhadap CAC {ltv/cac:.2f} kali. Angka ini memperlihatkan hipotesis yang perlu diperbaiki, bukan bisnis yang sudah terbukti. ROI assay memerlukan penawaran lab."),
 ("Kompetisi", "Alternatifnya chip genome-wide, panel parentage untuk tugas berbeda, analisis khusus, serta seleksi fenotipik atau status quo. Kami menawarkan desain riset yang dapat diaudit. Kami belum mengklaim assay lebih murah atau lebih baik dari produk komersial."),
 ("GTM", "Mulai dari wawancara dan akses kohort, lanjut ke proyek desain dengan kriteria penerimaan, baru pilot bersama laboratorium. Penjualan mengikuti peneliti sebagai champion, kepala program sebagai pembeli, serta izin data dan pengadaan. Langganan hanya dipertimbangkan setelah penggunaan berulang terbukti."),
 ("Tim dan kontribusi", "Exastra terdiri dari Bramantyo, Agathan, Bowo dan Bagus. Pembagian peran dan kualifikasi individual perlu dikonfirmasi tim. Ide dan referensi sudah ada sebelum kickoff; pipeline, eksperimen, dashboard dan deck tercatat selama hackathon. Timestamp Git menunjukkan pencatatan, bukan waktu setiap bagian ditulis."),
 ("Roadmap dan ask", "Langkah berikutnya adalah kalibrasi serta validasi independen, review probe dan uji assay, lalu pilot prospektif. Kami meminta akses satu kohort Bali dengan metadata, satu mitra lab untuk menilai kelayakan panel kecil, dan introduksi kepada calon pembeli program pembibitan. Bukti dapat diaudit, hasil negatif tetap terlihat, dan batas simulasi dinyatakan jelas.")]
lines = ["# Skrip pitch BantengPanel audited", "", "Target slot 340 detik + buffer 20 detik = 6 menit. Ini alokasi rancangan, **bukan bukti latihan**. Versi final 7 menit: tambah 30 detik demo dan 30 detik bukti.", ""]
elapsed = 0
for i, ((title, speech), seconds) in enumerate(zip(segments, facts["timingsSeconds"]), 1):
    lines += [f"## {i}. {title} — {elapsed//60}:{elapsed%60:02d} sampai {(elapsed+seconds)//60}:{(elapsed+seconds)%60:02d}", "", speech, ""]
    elapsed += seconds
lines += ["## Q&A", "", "- Apakah hewan atipikal terbukti introgresi? Belum; label, sampel dan variasi biologis masih kemungkinan lain.", "- Apakah q adalah kemurnian? S1 memakai q relatif dan target ekspektasi pedigree, bukan ancestry banteng absolut.", "- Apakah sensitivitas bisa dipakai langsung? Tidak; itu titik ROC oracle pada kontrol uji yang kecil. Ambang perlu kalibrasi independen.", "- Mengapa ada hasil negatif? Endpoint klasifikasi jenuh; semua baseline dan donor dilaporkan. Tidak ada pembuangan hewan agar hasil naik.", "- Berapa penghematan assay? Belum diketahui; belum ada quote laboratorium atau uji assay.", "- Berapa wawancara/LOI? Nol pada paket ini; hanya catatan percakapan nyata berizin boleh mengubahnya.", "", "Catat latihan nyata di REHEARSAL_LOG.md dan cek SUBMISSION_CHECKLIST.md sebelum mengunggah."]
(ROOT / "docs/PITCH_SCRIPT.md").write_text("\n".join(lines), encoding="utf-8")
facts["speakerSegments"] = [{"title": title, "text": speech, "seconds": seconds} for (title, speech), seconds in zip(segments, facts["timingsSeconds"])]
(PUBLIC / "pitch_facts.json").write_text(json.dumps(facts, indent=2, allow_nan=False), encoding="utf-8")
print(f"Pitch facts and script from {m['gitCommit']} (dirty={m['gitDirty']}); {elapsed}s + 20s buffer")
