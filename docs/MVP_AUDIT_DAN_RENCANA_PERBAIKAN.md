# BantengPanel — Audit MVP dan Rencana Perbaikan

> Dibuat Sabtu, 24 Oktober 2026, ±08:40 WIB, dari commit `f9081fd` (sama dengan `origin/main`).
> Dokumen ini menjadi acuan **prioritas dan batas klaim** sampai submission final (Minggu, 25 Oktober 2026, 10:00 WIB, tanpa toleransi waktu).
> Protokol ilmiah tetap di [SCIENTIFIC_PROTOCOL.md](SCIENTIFIC_PROTOCOL.md); provenance data tetap di [DATA_PROVENANCE.md](DATA_PROVENANCE.md).

---

## 0. Jawaban singkat

| Pertanyaan | Jawaban |
|---|---|
| Folder ini melakukan apa? | Repositori tim **Exastra** untuk GENOHACK 2026 Track 2. Isinya ada dua bagian: (1) `DriveKit/`, transkripsi materi bootcamp dan hackathon; (2) **BantengPanel**, pipeline Python yang mengambil dua kohort genotipe sapi publik (Dryad, Figshare), memilih panel SNP khusus sapi Bali di setiap training fold, membandingkannya dengan baseline berukuran sama, lalu menampilkan hasilnya di dashboard statis dan pitch deck. |
| Apakah semua sudah benar? | **Fondasinya benar**: tidak ada leakage seleksi SNP, checksum dan provenance dicatat, klaim jujur, dan hasil negatif dilaporkan. Namun ada **1 masalah arah ilmiah**, **4 gap deliverable wajib**, **13 bug/inkonsistensi**, dan **1 risiko kepatuhan** pada repo publik. Rinciannya ada di §3 dan §4. |
| Apakah MVP sudah selesai? | **Belum.** Prototipe komputasional sudah berjalan: 8 dari 8 fitur inti di ProjectOverview §5 sudah ada dan hasilnya terbukti dapat direproduksi (§10). Yang belum ada adalah analisis populasi (ProjectOverview §3 langkah 3) dan bukti keunggulan (§7). MVP hackathon belum bisa dinyatakan selesai karena: hipotesis inti tidak terbukti dan endpoint-nya jenuh, sehingga nilai produk belum terlihat; deck masih berupa PPTX 7 slide dengan teks `undefined` yang terlihat juri; belum ada PDF, link demo publik, slide tim, atau pemisahan pekerjaan sebelum dan selama hackathon; dan kriteria bisnis/validasi (D+E, 30% nilai babak 1) hampir kosong. |
| Sisa waktu | Draft deck: **16:00 WIB hari ini** (±7 jam). Final: **10:00 WIB besok** (±25 jam). |

Kriteria "selesai" yang tegas ada di **§7 Definition of Done**. Urutan pengerjaannya ada di **§6**.

---

## 1. Apa yang dilakukan repositori ini dan bagaimana

### 1.1 Peta repositori

| Lokasi | Fungsi | Status |
|---|---|---|
| `DriveKit/` | Transkripsi materi bootcamp D1–D6, guidebook, aturan hackathon, dan pedoman pitch | Referensi. Memuat data sensitif (§4.3) |
| `ProjectOverview.md` | Deskripsi produk, scope MVP, dan deliverable | Sebagian usang (§4.2 #9) |
| `deep-research-report.md` | Blueprint awal (FastAPI/Next.js, 102 sampel Bali) | Sudah digantikan oleh `docs/`; tidak perlu diubah |
| `bantengpanel/data.py` | `fetch` (unduh/verifikasi MD5, ekstraksi aman), parser Figshare & Dryad, `prepare` (autosom 1–29, sampel missing >10% dibuang) | Berfungsi |
| `bantengpanel/analysis.py` | Benchmark cross-validation, baseline, robustness, kandidat marker full-cohort, manifest | Berfungsi |
| `bantengpanel/report.py` | Menyusun `artifacts/public/evidence_report.md` | Berfungsi |
| `bantengpanel/cli.py` | Perintah `fetch`, `prepare`, `run`, `report` | Berfungsi |
| `configs/mvp.yaml` | Seed 20261024, 4 fold × 5 repeat, 30 panel acak, ukuran 8–200 | Dipakai |
| `artifacts/public/` | JSON/CSV hasil dan laporan bukti (di-commit) | Dibuat dari working tree kotor (§4.2 #2) |
| `artifacts/pitch/*.pptx` | Deck 7 slide | Ada bug `undefined`; struktur belum sesuai pedoman |
| `apps/dashboard/` | Dashboard HTML/JS statis yang membaca artefak; `package_static.py` membundel ke `out/` | Berfungsi; ada bug kecil |
| `data/` | Data mentah dan matriks olahan | Di-ignore Git (benar) |
| `docs/` | Spesifikasi, protokol, provenance, runbook, rencana bisnis, panduan wawancara, dan roadmap | Kualitas baik; perlu dokumen ini sebagai prioritas |

### 1.2 Alur kerja

```text
fetch    → unduh Figshare + baca ZIP Dryad lokal → verifikasi MD5 → ekstraksi aman → data/raw/manifest.json
prepare  → parse PED/MAP (Dryad) dan tabel panjang (Figshare) → dosis 0/1/2, -1 = missing
           → autosom 1–29 → buang sampel missing >10% → data/processed/*.npy + summary.json
run      → per kohort, RepeatedStratifiedKFold 4×5 (20 fold):
             training fold: call rate ≥90%, MAF ≥1%, skor Δ = |p_Bali − p_pembanding|
             BantengPanel  = ranking Δ + jarak minimum 250 kb per kromosom
             Global-MAF    = ranking MAF tertinggi + jarak 250 kb
             Random-mean   = rerata 30 panel acak (tanpa aturan jarak)
             model         = LogisticRegression(class_weight="balanced", C=0.1), imputasi modus
             metrik        = balanced accuracy + recall Bali pada fold uji
             robustness    = panel 48 SNP; missing 5/10/20% + error genotipe 1% hanya di fold uji
           → kandidat marker full-cohort (untuk ditinjau, bukan hasil validasi)
           → artifacts/public/{benchmark.json, *_benchmark.json, *_fold_results.csv, *_robustness.csv,
                               *_panel_candidates.csv, evidence_report.md}
dashboard → apps/dashboard/ membaca artefak; package_static.py menyalin ke out/ untuk hosting statis
```

### 1.3 Hasil saat ini (dari artefak yang di-commit)

| Kohort | Bali / total | 8 SNP (BP · G-MAF · acak) | 48 SNP | 200 SNP |
|---|---|---|---|---|
| Dryad | 20 / 1.542 | **0,962** · 0,940 · 0,915 | 0,960 · **0,969** · 0,962 | 0,960 · **0,980** · 0,966 |
| Figshare | 16 / 107 | **0,996** · 0,969 · 0,910 | 1,000 · 1,000 · 0,996 | 1,000 · 1,000 · 1,000 |

BP = BantengPanel, G-MAF = Global-MAF. Nilai yang ditampilkan adalah balanced accuracy rerata dari 20 fold yang saling tumpang tindih, jadi sifatnya deskriptif.

---

## 2. Target yang berlaku (sumber kebenaran)

### 2.1 Wajib dari panitia ([Participant Guide](../DriveKit/Hackathon/03_GENOHACK_2026_Hackathon_Participant_Guide.md) §5–§6)

| ID | Kewajiban |
|---|---|
| W1 | **Pitch deck final dalam format PDF** sesuai pedoman pitch |
| W2 | **Prototipe yang bisa didemokan**: link demo, build lokal, atau keduanya. Demo live wajib ada di dalam pitch |
| W3 | **Bukti ilmiah/teknis**: hasil benchmark, figur validasi, sitasi |
| W4 | **Link repositori kode** |
| W5 | **Pemisahan tegas** antara pekerjaan sebelum hackathon dan pekerjaan selama 40 jam hackathon |
| W6 | Tidak ada fabrikasi data, metrik, wawancara, atau traksi (pelanggaran berarti diskualifikasi) |
| W7 | Draft deck masuk sebelum 24 Okt 16:00; final masuk sebelum 25 Okt 10:00 |

### 2.2 Kriteria penilaian ([README](../README.md))

| Kode | Kriteria | Babak 1 | Final |
|---|---|---:|---:|
| A | Kejelasan masalah & urgensi | 15% | 10% |
| B | Keunggulan solusi & diferensiasi | 15% | 15% |
| C | Kedalaman teknis & eksekusi | 20% | 20% |
| D | Kelayakan bisnis & monetisasi | 15% | 15% |
| E | Validasi & bukti empiris (wawancara, LOI) | 15% | 10% |
| F | Tim | 10% | 15% |
| G | Jalur ke pasar & skalabilitas | 10% | 15% |

[Pedoman pitch](../DriveKit/Hackathon/02_GENOHACK_2026_Pitch_Guidelines.md) meminta 10 bagian: Intro, Story, Customer/Pain, Solution & Demo, TAM & ROI, Kompetisi (2×2), GTM & DMU, Finansial, Tim, Summary & Ask.

### 2.3 Target internal ([ProjectOverview §5 & §9](../ProjectOverview.md), [MVP_SPEC](MVP_SPEC.md))

Pipeline yang dapat direproduksi, kandidat panel multi-ukuran, benchmark dengan baseline setara, dashboard, laporan bukti, dan demo end-to-end dengan data nyata. Kriteria keberhasilan ilmiahnya: ada bukti empiris peningkatan performa, efisiensi, atau robustness dibanding baseline. Jika tidak ada, hasil dilaporkan apa adanya.

---

## 3. Hasil audit: target vs kondisi

Legenda: ✅ terpenuhi · ⚠️ sebagian · ❌ belum ada

| # | Target | Status | Bukti / masalah | Tindakan (§6) |
|---|---|:---:|---|---|
| 1 | Pipeline dapat direproduksi | ⚠️ | CLI berjalan dan hasil reproducible (§10). Namun artefak berasal dari `gitDirty: true` dengan `gitCommit: 4db10d1`, yaitu commit sebelum kode ada | A1 |
| 2 | QC sampel/SNP | ✅ | Per training fold; sampel missing >10% dibuang | — |
| 3 | Analisis genetika populasi (PCA/FST/struktur) | ❌ | Dijanjikan di ProjectOverview §3 dan diagram alur, tetapi tidak diimplementasikan | B7 |
| 4 | Mesin optimasi SNP | ✅ | Ranking Δ AF + jarak 250 kb | — |
| 5 | Benchmark dengan baseline setara | ✅ | Global-MAF + 30 panel acak, ukuran identik, tanpa leakage | — |
| 6 | Bukti keunggulan (kriteria sukses ilmiah) | ❌ | Tidak unggul pada ≥16 SNP (Dryad); Figshare mentok di plafon. Lihat §4.1 | B6 |
| 7 | Robustness | ⚠️ | Hanya pada 48 SNP; Figshare 1,000 di semua skenario sehingga tidak informatif | B6 |
| 8 | Dashboard | ⚠️ | Berfungsi; label "SNP Bali" salah; tidak ada visual populasi | A1, B7 |
| 9 | Laporan bukti | ✅ | `artifacts/public/evidence_report.md` | A1 (regenerasi) |
| 10 | W1 Deck PDF sesuai pedoman | ❌ | Hanya PPTX 7 slide; slide 4 menampilkan "**undefined** sampel dikeluarkan"; tidak ada TAM, kompetisi, tim, ask, atau screenshot demo | A2 |
| 11 | W2 Demo publik + cadangan | ⚠️ | Lokal berjalan. `.openai/hosting.json` ada, tetapi URL publiknya tidak tercatat; GitHub Pages belum aktif; tidak ada video cadangan | B4, D |
| 12 | W3 Bukti ilmiah + sitasi | ⚠️ | Benchmark ada; belum ada sitasi literatur di deck/dashboard | A2, B6 |
| 13 | W4 Repo | ⚠️ | Publik (`github.com/khairys/GENOHACK`). README root berisi DriveKit, bukan produk; memuat data sensitif | B5 |
| 14 | W5 Pemisahan pre-existing vs hackathon | ❌ | Belum ada di dokumen, deck, maupun dashboard | A3 |
| 15 | Validasi pelanggan (E) | ❌ | 0 wawancara, 0 LOI | B1 |
| 16 | TAM & unit economics (D) | ❌ | Deck menyatakan "belum dihitung" | B2 |
| 17 | Kompetisi & diferensiasi (B) | ❌ | Tidak ada di deck | B3 |
| 18 | Tim (F) | ❌ | Tidak ada slide tim | A4 |
| 19 | Tes otomatis | ❌ | `pyproject.toml` merujuk `tests/`, tetapi foldernya tidak ada | C2 |
| 20 | Kejujuran klaim (W6) | ✅ | Konsisten di docs, deck, dan dashboard. **Pertahankan.** | — |

**Kesimpulan:** 5 dari 20 target ✅, 6 ⚠️, dan 9 ❌. Bagian yang paling lemah justru yang menentukan kelulusan administratif (W1, W5) dan 50% nilai babak 1 (B, D, E, F, G).

---

## 4. Temuan penting

### 4.1 Temuan ilmiah: mengapa arah perlu dikoreksi

**(a) Hipotesis utama tidak didukung pada endpoint saat ini.** Selisih per fold (BantengPanel − Global-MAF) dalam balanced accuracy:

| SNP | Dryad: rerata Δ (menang/seri/kalah) | Figshare: rerata Δ (menang/seri/kalah) |
|---:|---|---|
| 8 | **+0,022** (15/0/5) | **+0,026** (13/6/1) |
| 16 | −0,016 (11/0/9) | +0,004 (4/16/0) |
| 24 | −0,009 (14/2/4) | +0,001 (1/19/0) |
| 48 | −0,009 (10/7/3) | 0,000 (0/20/0) |
| 200 | −0,020 (0/16/4) | 0,000 (0/20/0) |

**(b) Kekalahan di Dryad hampir seluruhnya berasal dari dua hewan berlabel BALI.** Analisis ulang pada panel 48 SNP (5 repeat):

| Sampel Dryad | Gagal dikenali sebagai Bali | Skor "kemiripan-Bali"* |
|---|---|---:|
| `615:615520670` | 5 dari 5 repeat | 0,37 |
| `615:615520690` | 3 dari 5 repeat | 0,44 |
| `615:615520680` | 0 dari 5 | 0,64 |
| 17 hewan Bali lainnya | 0 | 0,85–0,93 |
| Madura (MAD, n=7), rerata | 1 hewan (`618:618521080`) salah diprediksi Bali 2 kali | 0,26 |

\* Proporsi dari 200 marker Δ tertinggi (full cohort) di mana dosis hewan lebih dekat ke rerata Bali daripada ke rerata pembanding. Angka ini deskriptif dan bukan hasil cross-validation.

Analisis sensitivitas post-hoc dengan dua hewan teratas dikeluarkan (Bali n=18): 8 SNP **0,972** vs 0,957; 24 SNP 0,990 vs 0,991; 48 SNP 0,994 vs 0,993. Artinya, **kedua metode seri di plafon** begitu dua hewan atipikal itu tidak ada.

**(c) Artinya:** endpoint biner "Bali vs bukan Bali" **terlalu mudah** sehingga tidak bisa menunjukkan nilai produk. Sapi Bali adalah bentuk domestik banteng (*Bos javanicus*) (Mohamad et al., 2009), sehingga hampir semua panel mencapai plafon. Kesalahan yang tersisa ditentukan oleh **hewan yang komposisi genetiknya tidak murni atau labelnya meragukan**, bukan oleh kualitas ranking marker.

**(d) Justru di sini masalah nyatanya.** Literatur mencatat bahwa ternak Indonesia terbentuk dari campuran zebu dan banteng, misalnya Madura dengan kontribusi banteng hingga 36,6% (Wang et al., 2025) dan PO dengan komponen *B. javanicus* sekitar 6–7% (Hartati et al., 2015). Sudrajad et al. (2020), sumber data Figshare, menemukan hewan hibrida dan menyatakan bahwa upaya menjaga **kemurnian** masih diperlukan. Pertanyaan bernilai bagi pengguna bukan "apakah ini Bali?", melainkan **"berapa proporsi ancestry Bali/banteng hewan ini, dan apakah ada introgresi?"**. Panel minimal dengan marker yang informatif terhadap ancestry adalah tempat seleksi population-aware secara teori paling unggul dibanding marker MAF tinggi.

**Batas klaim:** Mohamad et al. (2009) **tidak** menemukan introgresi zebu pada lima populasi sapi Bali (marker mikrosatelit/mtDNA/Y). Jadi dua hewan atipikal itu **tidak boleh** disebut "terbukti introgresi". Kemungkinannya ada tiga: introgresi, salah label, atau masalah sampel. Sebut mereka "hewan atipikal yang perlu konfirmasi".

### 4.2 Bug dan inkonsistensi teknis

| # | Masalah | Lokasi | Dampak | Perbaikan |
|---|---|---|---|---|
| 1 | Slide 4 berbunyi "Dryad: **undefined** sampel dikeluarkan". Builder membaca `excludedSamplesAboveMissingThreshold`, sedangkan `data/processed/summary.json` (dibuat oleh kode versi lama) memakai `excludedSamplesMissingOver10Pct` | [data.py:177](../bantengpanel/data.py:177), `artifacts/qa/pitch/build_deck.mjs:96` | Terlihat juri; menandakan artefak dan kode tidak sinkron | Jalankan ulang `prepare` + `run` dari kode yang di-commit, lalu rebuild deck |
| 2 | `benchmark.json` mencatat `gitCommit: 4db10d1`, `gitDirty: true` | `artifacts/public/benchmark.json` | Klaim reproduksibilitas tidak bisa ditelusuri ke commit | Jalankan ulang di tree bersih, lalu buat tag `mvp-v0.1` |
| 3 | Kartu statistik berlabel "SNP Bali" padahal menampilkan jumlah **hewan** Bali | [app.js:28](../apps/dashboard/app.js:28) | Membingungkan juri | Ganti dengan "Eligible SNP" (rerata `eligibleMarkers` per fold) atau "Hewan Bali" |
| 4 | Teks "total: 1.543 hewan" padahal 1.542 setelah QC | [app.js:4](../apps/dashboard/app.js:4) | Inkonsisten dengan kartu statistik | Tulis "1.543 di sumber · 1.542 setelah QC" |
| 5 | Redirect `out/index.html` memakai path absolut `/apps/dashboard/` | [package_static.py:28](../apps/dashboard/package_static.py:28) | Rusak di GitHub Pages yang disajikan di bawah `/GENOHACK/` | Gunakan `url=apps/dashboard/` (relatif) |
| 6 | Baseline acak tidak memakai aturan jarak 250 kb, sedangkan dua metode lain memakainya | [analysis.py:119](../bantengpanel/analysis.py:119) | Asimetri kecil pada perbandingan | Dokumentasikan di protokol, atau terapkan aturan jarak pada sampel acak |
| 7 | Komentar "fitted model stay fixed", padahal model di-fit ulang (deterministik, hasil sama) | [analysis.py:124](../bantengpanel/analysis.py:124) | Menyesatkan reviewer kode | Perbaiki komentar |
| 8 | Imputasi modus dihitung dari training gabungan (≈99% pembanding di Dryad), sehingga genotipe hilang pada hewan Bali diisi alel pembanding | `analysis.py` `_fit_score` | Ikut menurunkan recall Bali pada skenario missing 20% | Catat sebagai keterbatasan. Alternatif: imputasi netral, yaitu nilai tengah antara rerata dosis Bali dan pembanding dari training |
| 9 | ProjectOverview menyebut ukuran 48–200 dan langkah "Population genetic analysis"; implementasi memakai 8–200 dan tidak ada PCA/FST | [ProjectOverview.md:73](../ProjectOverview.md:73) | Dokumen tidak sesuai produk | Perbarui setelah B7 |
| 10 | Arsip Dryad tidak diunduh otomatis dan `*.zip` di-ignore, sedangkan runbook tidak memberi URL unduhan | [RUNBOOK.md](RUNBOOK.md) | Juri yang clone repo tidak bisa mereproduksi | Tambahkan URL DOI Dryad dan langkah unduhnya |
| 11 | `pyproject.toml` merujuk `tests/` yang tidak ada; dependensi `pydantic` dan `scipy` tidak dipakai | [pyproject.toml:10](../pyproject.toml:10), [:22](../pyproject.toml:22) | Kesan belum rapi | Tambahkan tes minimal (C2); hapus dependensi yang tidak dipakai |
| 12 | `apps/dashboard/out/` berisi salinan basi (di-ignore) | lokal | Membingungkan | Hapus folder lokal tersebut |
| 13 | `_git_dirty()` dipanggil di `run_all` **setelah** `benchmark()` menimpa file yang ter-track di `artifacts/public/`. Akibatnya, setiap run yang mengubah output (atau menambah file baru) melaporkan `gitDirty: true` walaupun kodenya bersih | [analysis.py:184](../bantengpanel/analysis.py:184) | A1 bisa gagal mendapatkan `gitDirty: false` | Rekam `gitCommit`/`gitDirty` di awal `run_all`, sebelum menulis output, atau kecualikan `artifacts/public/` dari pemeriksaan |

### 4.3 Risiko kepatuhan pada repo publik

- `github.com/khairys/GENOHACK` **publik**. Di dalam `DriveKit/` terdapat **kredensial Wi-Fi panitia** ([Participant Guide](../DriveKit/Hackathon/03_GENOHACK_2026_Hackathon_Participant_Guide.md), bagian Wi-Fi), **nomor telepon panitia**, daftar nama anggota tim lain, dan transkripsi materi bootcamp yang hak ciptanya milik penyelenggara. Aturan hackathon menyebut pelanggaran privasi data (UU PDP) dan hak kekayaan intelektual sebagai pelanggaran.
- **Rekomendasi:** sebelum link repo dikirim ke juri, minimal hapus atau sensor kredensial dan nomor telepon dari branch `main`, lalu tanyakan ke panitia apakah materi bootcamp boleh dipublikasikan. Pilihan terbersih adalah memindahkan `DriveKit/` ke repo privat. Menulis ulang riwayat Git bersifat destruktif dan harus diputuskan bersama tim.
- README root saat ini adalah README DriveKit beserta "system prompt untuk agen LLM", sehingga juri tidak langsung melihat produk. Lihat B5.

### 4.4 Gap bisnis dan validasi

Deck menyatakan dengan jujur bahwa belum ada wawancara, harga, LOI, TAM, maupun unit economics. Kejujuran itu benar (W6), tetapi pada kondisi sekarang kriteria D, E, F, dan G (50% nilai babak 1) hampir nol. Perbaikannya **bukan** mengarang angka. Perbaikannya adalah **mengumpulkan bukti nyata hari ini**: mentor dan pakar tersedia pukul 08:00–23:00, lalu menyajikan formula dengan input bersumber (B1–B3).

---

## 5. Arah yang benar

### 5.1 Reposisi produk

| | Sebelum | Sesudah (direkomendasikan) |
|---|---|---|
| Pertanyaan | "Apakah panel khusus Bali lebih akurat membedakan Bali?" | "Berapa SNP minimum yang cukup untuk **memverifikasi kemurnian dan memperkirakan ancestry** sapi Bali, dan apakah seleksi population-aware lebih efisien daripada panel generik?" |
| Endpoint | Balanced accuracy biner (jenuh) | (1) Error estimasi proporsi ancestry; (2) deteksi hewan introgresi pada spesifisitas tetap; (3) akurasi biner tetap dilaporkan sebagai sanity check |
| Nilai bagi pengguna | Belum jelas | Penyaringan bibit/pejantan dan audit kemurnian dengan panel kecil yang murah, dengan bukti yang dapat diaudit |
| Posisi temuan sekarang | Disajikan sebagai "tidak unggul" | Disajikan sebagai **pembelajaran**: endpoint biner jenuh; kesalahan berpusat pada hewan atipikal; keunggulan muncul di regime panel sangat kecil (8 SNP) |

### 5.2 Tiga pesan yang harus diingat juri

1. **Rigor:** pipeline bebas leakage, dengan provenance tercatat, baseline setara, dan hasil negatif yang dilaporkan.
2. **Insight:** membedakan sapi Bali dari ras lain itu mudah. Yang sulit, dan yang dibutuhkan pengguna, adalah mendeteksi hewan yang tidak murni. Data kami menandai dua hewan "Bali" atipikal yang perlu dikonfirmasi.
3. **Arah nilai:** pada 8 SNP, seleksi population-aware lebih baik di 15/20 fold (Dryad) dan 13/20 fold (Figshare). Regime panel kecil ini relevan untuk assay SNP berbiaya rendah. Ini masih hipotesis dan akan diuji dengan kohort independen dan laboratorium.

### 5.3 Yang tidak boleh dilakukan

- Mengklaim BantengPanel "lebih akurat" atau "lebih hemat biaya" tanpa ukuran yang mendukung.
- Mencantumkan angka TAM, harga, atau populasi tanpa sumber. Setiap angka harus diberi label *terukur*, *dikutip (sumber)*, atau *asumsi*.
- Menyebut obrolan dengan mentor sebagai "validasi pelanggan". Sebut "wawancara pakar".
- Menyebut hewan atipikal "terbukti introgresi".
- Menyebut hasil simulasi admixture sebagai bukti pada ternak nyata.

### 5.4 Hipotesis pelanggan untuk diuji (bukan fakta)

| Peran DMU | Kandidat (verifikasi dalam wawancara) |
|---|---|
| Pengguna | Analis genetika atau peneliti ternak yang menyusun panel/menilai kemurnian |
| Champion | Peneliti pemuliaan sapi Bali di lembaga riset atau balai pembibitan |
| Pembeli ekonomi | Kepala laboratorium/kepala balai; pemilik anggaran program pembibitan |
| Veto | Pemilik data genotipe, kepatuhan data, standar mutu bibit |
| Organisasi awal untuk didekati | Pusat Riset Peternakan BRIN (afiliasi Sudrajad dalam Wang et al., 2025); Genetic Conservation and Genome Laboratory IPB (afiliasi dalam Wang et al., 2025); balai pembibitan dan inseminasi buatan yang memelihara sapi Bali; laboratorium genotyping layanan. **Verifikasi nama, peran, dan kebutuhan masing-masing sebelum dimasukkan ke deck.** |

---

## 6. Rencana perbaikan berprioritas

Kolom PIC diisi oleh tim. Estimasi waktu adalah perkiraan; batas waktu bersifat keras.

### Blok A — sampai 15:30 WIB (draft deck masuk 16:00)

| ID | Tugas | Estimasi | Hasil |
|---|---|---:|---|
| A1 | **Bekukan kode.** Perbaiki bug §4.2 #3, #4, #5, #7, dan **#13 (wajib, agar `gitDirty` benar)**. Commit. Jalankan `python -m bantengpanel.cli prepare` lalu `run` di tree bersih. Run berlangsung ±40 menit, jadi jalankan di latar sambil mengerjakan A2. Pastikan `gitDirty: false`. Commit artefak. Buat tag `mvp-v0.1` | 90–120 menit | Artefak yang dapat ditelusuri; `summary.json` memakai key baru |
| A1b | Jadikan analisis hewan atipikal (§4.1b) bagian dari pipeline, misalnya artefak `dryad_atypical_samples.csv` berisi skor kemiripan-Bali dan frekuensi salah klasifikasi, agar temuan di pitch dapat direproduksi | 45 menit | Bukti untuk pesan #2 |
| A2 | **Bangun ulang deck** mengikuti §8 (10–11 slide). Hilangkan `undefined`. Sisipkan screenshot dashboard. Tambahkan sitasi (§11). Ekspor **PDF** | 2–3 jam | Draft PDF |
| A3 | Slide dan bagian README **"Sebelum vs selama hackathon"**. Contoh isi: ide dan proposal (diserahkan sebelum 23 Okt 16:00), dataset publik, dan DriveKit (commit 22 Okt) sudah ada sebelumnya. Pipeline, artefak, dashboard, dan deck dibuat setelah kickoff 23 Okt 20:30 (commit 24 Okt 01:42 dan 02:39). **Tim wajib memastikan sendiri**, karena waktu commit bukan bukti waktu penulisan | 20 menit | W5 terpenuhi |
| A4 | Slide tim: peran, keahlian yang relevan, dan kebutuhan advisor 6–12 bulan | 20 menit | Kriteria F |
| A5 | Pesan slot mentor sekarang juga (lihat B1) | 10 menit | Jadwal |
| A6 | Kirim draft paling lambat 15:30 | — | W7 |

### Blok B — 16:00–23:00 WIB (gunakan umpan balik pitch clinic)

| ID | Tugas | Estimasi | Hasil |
|---|---|---:|---|
| B1 | **Wawancara 3–5 orang** memakai [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md). Prioritas mentor: **Sabhrina Gita Aninta** (genetika populasi; ikut menulis Wang et al., 2025 tentang introgresi ternak Indonesia); **Farania Rangkuti** (genomik populasi); **Bugi Ratno Budiantoro** (BRIN, assay PCR/SNP: kelayakan panel kecil dan biaya); **Shelly Natalia** (unit economics); **Nabila Safira** atau **Agustina Ciptarahayu** (model bisnis). Hubungi juga 1–2 calon pengguna di luar mentor. Catat tanggal, peran, kutipan (dengan izin), dan langkah lanjut | 3–4 jam | Kriteria E dengan bukti nyata; label "pakar" vs "calon pelanggan" |
| B2 | **TAM bottom-up** = jumlah institusi/program yang relevan × proyek atau sampel per tahun × nilai per proyek atau sampel. Ambil input dari statistik resmi (misalnya publikasi Statistik Peternakan dan Kesehatan Hewan Ditjen PKH/BPS) dan dari harga yang dikutip laboratorium dalam wawancara. Beri label setiap input. Jika input belum ada, tampilkan formulanya dan nyatakan input mana yang sedang dikumpulkan | 1,5 jam | Kriteria D tanpa fabrikasi |
| B3 | Peta kompetisi 2×2. Alternatif: chip SNP genome-wide via laboratorium layanan (misalnya kelas BovineSNP50, platform sumber data); panel parentage/mikrosatelit standar; seleksi fenotipik; tidak melakukan apa-apa. Usulan sumbu: *spesifik populasi lokal* × *biaya/jumlah marker per sampel*. Hindari klaim harga pesaing tanpa sumber | 45 menit | Kriteria B |
| B4 | **Demo publik**: perbaiki redirect (§4.2 #5), jalankan `python apps/dashboard/package_static.py`, publikasikan `out/` (GitHub Pages dari branch `gh-pages`, atau hosting yang sudah dikonfigurasi di `.openai/hosting.json`), uji di laptop dan ponsel, catat URL di README. Rekam **video cadangan 2 menit** dan simpan salinan offline | 1,5 jam | W2 |
| B5 | **README root**: BantengPanel di bagian atas (masalah, demo, hasil, cara menjalankan, batas klaim, pemisahan pre-existing/hackathon). Putuskan penanganan DriveKit (§4.3) | 45 menit | W4 |
| B6 | **Eksperimen S1, simulasi admixture** (timebox 4 jam, **cut-off 22:00**). Detail di bawah | 4 jam | Uji yang adil untuk proposisi nilai baru |
| B7 | **Visual populasi**: PCA (PC1/PC2) untuk Figshare dan subset Asia di Dryad, dengan hewan Bali atipikal dan Madura disorot. Tambahkan ke dashboard dan deck (timebox 1 jam) | 1 jam | Target #3; demo lebih meyakinkan |

**Desain eksperimen S1 (B6):**

1. Gunakan fold yang sama dengan benchmark. Frekuensi alel dan ranking panel dihitung dari **training fold saja**.
2. Ambil hewan Bali dan pembanding Indonesia (Figshare: ONG/MAD; Dryad: zebu Asia/MAD) dari **fold uji**. Bangkitkan genotipe keturunan secara Mendelian per SNP: F1 (50%), BC1 (25% non-Bali), BC2 (12,5%), dan Bali murni sebagai kontrol.
3. Perkirakan proporsi ancestry Bali *q* per hewan dengan likelihood dua populasi (grid *q* ∈ [0,1]) memakai frekuensi alel training.
4. Bandingkan BantengPanel, Global-MAF, dan acak pada 8–200 SNP. Metrik: MAE(*q*), serta sensitivitas deteksi BC2 pada spesifisitas ≥95% terhadap Bali murni.
5. Labeli hasilnya sebagai **simulasi komputasional**. Catat asumsi marker tidak terpaut (aturan jarak 250 kb mengurangi tetapi tidak menghilangkan LD). Laporkan hasil apa pun yang muncul, termasuk bila tidak unggul.
6. Jika sampai 22:00 belum selesai: hentikan, dan sajikan S1 sebagai eksperimen berikutnya bersama temuan §4.1b.

### Blok C — 23:00–02:00 WIB (bekukan klaim)

| ID | Tugas |
|---|---|
| C1 | Jalankan ulang pipeline final di tree bersih; tag `mvp-v1.0`; perbarui `evidence_report.md`, dashboard, dan angka di deck **dari artefak, bukan diketik manual** |
| C2 | Tes minimal `tests/`: `encode_alleles`, penolakan path traversal di `safe_extract`, dan uji bahwa seleksi SNP tidak menyentuh indeks fold uji |
| C3 | Perbarui [ProjectOverview.md](../ProjectOverview.md), [MVP_SPEC.md](MVP_SPEC.md), [PITCH_SCRIPT.md](PITCH_SCRIPT.md), dan [RUNBOOK.md](RUNBOOK.md) (URL Dryad) agar sesuai keputusan §5 |

### Blok D — 02:00–08:00 WIB

Latihan pitch minimal 3 kali dengan timer (versi 6 menit untuk track, 7 menit untuk final). Demo di dalam pitch (bukan lampiran) maksimal 90 detik. Drill Q&A (§9). Uji video cadangan dan demo offline.

### Blok E — 08:00–09:30 WIB

Periksa PDF final, semua link (demo, repo, tag), lalu **submit paling lambat 09:30**.

### Urutan pemotongan bila tertinggal

Potong B7, lalu B6 (jadikan "eksperimen berikutnya"), lalu C2. **Jangan pernah memotong** A1–A4, B1, B4, B5, dan pemeriksaan klaim C1.

---

## 7. Definition of Done: kapan MVP boleh dinyatakan selesai

MVP **selesai** hanya bila semua butir **Wajib** tercentang.

**Wajib**
- [ ] Artefak `artifacts/public/` dibuat dari commit bertag dengan `gitDirty: false`
- [ ] Tidak ada `undefined`, `NaN`, atau angka yang berbeda antara deck, dashboard, dan `evidence_report.md`
- [ ] Deck **PDF** mencakup 10 bagian pedoman (boleh digabung) termasuk Tim dan Ask yang spesifik
- [ ] Slide dan README berisi pemisahan pekerjaan sebelum vs selama hackathon
- [ ] Link demo publik berfungsi, plus video cadangan dan salinan offline
- [ ] README root menjelaskan BantengPanel; data sensitif sudah ditangani
- [ ] Setiap angka bisnis diberi label terukur/dikutip/asumsi; nol angka tanpa sumber
- [ ] Wawancara yang dilaporkan sama dengan wawancara yang benar-benar terjadi (catatan tersimpan di `docs/`)
- [ ] Temuan ilmiah disajikan sesuai §5.2 dan §5.3
- [ ] Pitch dilatih dengan timer dan muat dalam 6:00

**Sangat dianjurkan**
- [ ] Eksperimen S1 (simulasi admixture) dengan hasil yang dilaporkan apa adanya
- [ ] Visual PCA di dashboard
- [ ] ≥3 wawancara dengan minimal 1 calon pengguna di luar mentor
- [ ] Tes minimal lulus

---

## 8. Struktur deck revisi (±11 slide, 6 menit)

| # | Bagian pedoman | Isi | Kriteria | Waktu |
|---:|---|---|:---:|---:|
| 1 | Intro & hook | BantengPanel · Exastra · Track 2. Tagline: verifikasi kemurnian sapi Bali dengan panel SNP minimal yang buktinya dapat diaudit | A | 0:15 |
| 2 | Story & urgensi | Sapi Bali sebagai sumber daya genetik lokal; ternak Indonesia terbentuk dari campuran zebu-banteng (Wang 2025; Hartati 2015); Sudrajad 2020 menyatakan kemurnian perlu dijaga. **Tanpa statistik yang tidak bersumber** | A | 0:30 |
| 3 | Pelanggan & masalah | DMU (§5.4) + **hasil wawancara nyata** (jumlah, peran, 1–2 kutipan berizin) | A, E | 0:35 |
| 4 | Solusi | Diagram pipeline 5 langkah; bebas leakage; baseline setara | B, C | 0:25 |
| 5 | **Demo live** | Dashboard: pilih kohort, kurva, panel 8 SNP, marker explorer, unduh CSV | C | 1:15 |
| 6 | Bukti | Tabel menang/seri/kalah per fold (§4.1a); plafon; dua hewan atipikal (dan hasil S1 bila ada) | C, E | 0:45 |
| 7 | TAM & ROI | Formula bottom-up dengan input berlabel | D | 0:25 |
| 8 | Kompetisi | 2×2 + alternatif "tidak melakukan apa-apa" | B | 0:20 |
| 9 | GTM & model bisnis | Jasa desain/audit panel per proyek, lalu langganan bila alur berulang terbukti; proses pembelian; watering holes | D, G | 0:25 |
| 10 | Tim + pre-existing vs hackathon | Peran, keahlian, kebutuhan advisor; tabel W5 | F | 0:20 |
| 11 | Roadmap & Ask | 12 bulan ([EXECUTION_ROADMAP.md](EXECUTION_ROADMAP.md)), ask spesifik: akses kohort Bali independen, laboratorium mitra untuk uji panel kecil, introduksi ke balai pembibitan. Tutup dengan 3 pesan di §5.2 | G | 0:25 |

Versi final 7 menit: tambah 30 detik di demo dan 30 detik di bukti.

---

## 9. Tambahan Q&A juri

**"Sapi Bali itu banteng domestik. Bukankah membedakannya dari ras lain itu trivial?"**
Ya, dan itu salah satu temuan kami. Pada ≥24 SNP semua metode mendekati plafon. Kesalahan yang tersisa berpusat pada hewan yang tidak tampak murni. Karena itu kami mengalihkan endpoint ke estimasi ancestry dan deteksi introgresi.

**"Dua hewan atipikal itu apa?"**
Belum diketahui. Kemungkinannya introgresi, salah label, atau masalah sampel. Studi mikrosatelit sebelumnya tidak menemukan introgresi zebu pada populasi Bali (Mohamad et al., 2009), jadi kami tidak mengklaim apa-apa sampai ada konfirmasi dari pemilik data atau genotipe ulang.

**"Mengapa tidak memakai FST atau ADMIXTURE?"**
Δ frekuensi alel adalah statistik kontras dua populasi yang sederhana dan cepat. Untuk dua kelompok, urutan rankingnya sejalan dengan FST. ADMIXTURE/PCA adalah langkah berikutnya untuk validasi struktur populasi (B7/S1).

**"Apakah hasil simulasi bisa dipercaya untuk ternak nyata?"**
Tidak sebagai bukti lapangan. Simulasi hanya menguji apakah panel cukup informatif dalam kondisi terkontrol. Bukti nyata memerlukan kohort independen dengan status ancestry yang diketahui.

**"Dari mana uangnya?"**
Jawab hanya dengan apa yang ditemukan dalam wawancara B1, dan bedakan dengan jelas antara hipotesis dan bukti.

---

## 10. Bukti verifikasi audit ini

| Pemeriksaan | Hasil |
|---|---|
| Re-run pipeline dari kode `f9081fd` ke folder sementara (konfigurasi `configs/mvp.yaml`, Python 3.13 / scikit-learn 1.9.1) | **Identik bit demi bit** dengan artefak yang di-commit untuk kedua kohort: selisih balanced accuracy, recall, dan robustness = 0; daftar 200 marker kandidat sama; CSV per fold sama persis. Durasi ±38 menit di laptop tim. Masalahnya hanya pada **ketertelusuran** (§4.2 #2), bukan hasilnya |
| Analisis salah klasifikasi Dryad 48 SNP | Lihat §4.1b |
| Sensitivitas tanpa 2 hewan atipikal | Lihat §4.1b |
| Status repo | `main` = `origin/main` = `f9081fd`; repo publik; GitHub Pages belum aktif |
| Isi deck | 7 slide; slide 4 memuat `undefined`; tidak ada slide tim/TAM/kompetisi/ask |

Analisis §4.1b dilakukan dengan skrip sementara di luar repo. Tugas A1b memindahkannya ke pipeline agar dapat direproduksi.

---

## 11. Referensi (diambil dari PubMed)

- Decker, J. E., et al. (2014). Worldwide patterns of ancestry, divergence, and admixture in domesticated cattle. *PLoS Genetics*, 10(3), e1004254. https://doi.org/10.1371/journal.pgen.1004254 — sumber kohort Dryad.
- Hartati, H., et al. (2015). Evidence of *Bos javanicus* × *Bos indicus* hybridization and major QTLs for birth weight in Indonesian Peranakan Ongole cattle. *BMC Genetics*, 16, 75. https://doi.org/10.1186/s12863-015-0229-5
- Mohamad, K., et al. (2009). On the origin of Indonesian cattle. *PLoS ONE*, 4(5), e5490. https://doi.org/10.1371/journal.pone.0005490
- Sudrajad, P., et al. (2020). An insight into the evolutionary history of Indonesian cattle assessed by whole genome data analysis. *PLoS ONE*, 15(11), e0241038. https://doi.org/10.1371/journal.pone.0241038 — sumber kohort Figshare.
- Wang, X., Nursyifa, C., Aninta, S. G., et al. (2025). The genetic diversity of Indonesian cattle has been shaped by multiple introductions and adaptive introgression. *Nature Communications*, 16, 8192. https://doi.org/10.1038/s41467-025-62692-z
