# BantengPanel — GENOHACK 2026 · Exastra

Prototipe riset untuk merancang dan mengevaluasi panel SNP minimal bagi riset ancestry sapi Bali. Pipeline memakai dua kohort genotipe publik secara terpisah, menguji panel dengan baseline setara, lalu menyajikan bukti yang dapat diunduh.

**Demo publik:** https://bantengpanel-genohack.toastygecko1026.chatgpt.site  
**Kode:** https://github.com/khairys/GENOHACK  
**Rilis audited:** tag `mvp-v1.0` · sumber analisis: `mvp-v1.0-source`.

Status: MVP komputasional telah diverifikasi. Wawancara, konfirmasi peran/kontribusi, latihan dan pengiriman kompetisi tetap memerlukan tindakan tim; tidak dilaporkan selesai otomatis.

## Mulai dari sini

- [Paket dan status perbaikan audit](docs/AUDIT_IMPLEMENTATION_STATUS.md)
- [Laporan bukti yang dibuat pipeline](artifacts/public/evidence_report.md)
- [Deck PDF](artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pdf) dan [PPTX](artifacts/pitch/BantengPanel_GENOHACK_2026_Audited.pptx)
- [Video demo cadangan 2 menit](artifacts/demo/BantengPanel_demo_2min.mp4) dan [bundle demo offline](artifacts/demo/BantengPanel_offline.zip)
- [Runbook](docs/RUNBOOK.md), [protokol ilmiah](docs/SCIENTIFIC_PROTOCOL.md), [provenance](docs/DATA_PROVENANCE.md)

## Yang diimplementasikan

1. Verifikasi checksum, ekstraksi ZIP aman, parser sumber terpisah, QC sampel/autosom.
2. Ranking kontras frekuensi alel, baseline Global-MAF dan 30 panel acak; semua memakai aturan jarak 250 kb.
3. Evaluasi 8–200 SNP dengan 4 fold × 5 repeat, imputasi dan seleksi hanya pada training fold.
4. Prediksi held-out per hewan, review hewan atipikal, robustness 48 SNP, PCA deskriptif.
5. S1: simulasi Mendelian F1/BC1/BC2 dari induk fold uji, estimasi q relatif dan perbandingan MAE.
6. Dashboard interaktif, CSV/JSON, figur mandiri, laporan bukti, deck dan cadangan demo.

## Cara membaca hasil

Dryad: 20 Bali dari 1.542 hewan setelah QC, 43.042 SNP autosomal. Figshare: 16 Bali dari 107 hewan, 52.886 SNP. Kedua sumber memakai encoding alel berbeda sehingga tidak digabung.

Klasifikasi biner adalah pemeriksaan awal yang cepat mencapai plafon. Keunggulan umum tidak diasumsikan. Kurva, selisih per fold, S1, serta identitas commit dibaca dari [artefak](artifacts/public/benchmark.json); angka di deck dibangun dari artefak yang sama. Simulasi q mengukur campuran relatif terhadap pasangan referensi dan target pedigree, **belum memverifikasi kemurnian hewan nyata**. Hewan atipikal memerlukan konfirmasi; jangan menyebutnya terbukti introgresi.

Tidak ada wawancara, LOI, penjualan, harga tervalidasi, penghematan assay, atau uji laboratorium yang diklaim. [Model bisnis](docs/BUSINESS_MODEL.md) membedakan sumber, hasil hitung, dan asumsi.

Koreksi penting: frekuensi alel kelas yang tidak terobservasi kini dikecualikan, sehingga angka panel 8 SNP versi lama tidak dipertahankan. [Review kualitas data](artifacts/public/data_quality_review.json) dan [status audit](docs/AUDIT_IMPLEMENTATION_STATUS.md) menjelaskan perubahan tersebut.

## Menjalankan

Python 3.11+. Lihat [runbook](docs/RUNBOOK.md) untuk unduhan Dryad, instalasi, reproduksi dengan sumber bersih, tes dan mode offline.

```powershell
python -m pip install -e ".[dev]"
python -m bantengpanel.cli fetch --dryad PATH_KE_ZIP_DRYAD
python -m bantengpanel.cli prepare
python -m bantengpanel.cli run
python -m bantengpanel.cli figures
python -m pytest -q
python -m http.server 8000
```

Dashboard lokal: http://localhost:8000/apps/dashboard/ . Raw genotype dan cache berada di `data/` yang diabaikan Git; paket demo berisi keluaran riset, bukan data mentah.

## Sebelum vs selama hackathon

Ide/proposal awal dan sumber publik sudah ada sebelum kickoff. Materi referensi tercatat pada commit 22 Oktober. Pipeline, hasil, dashboard dan deck tercatat pada 24 Oktober selama hackathon; implementasi audit ditelusuri melalui tag sumber/rilis. Timestamp Git bukan bukti waktu penulisan. Tim harus mengonfirmasi pembagian kontribusi aktual sebelum submission. Rincian: [CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md).

## Referensi dan privasi

[Decker 2014](https://doi.org/10.1371/journal.pgen.1004254), [Sudrajad 2020](https://doi.org/10.1371/journal.pone.0241038), [Mohamad 2009](https://doi.org/10.1371/journal.pone.0005490), [Wang 2025](https://doi.org/10.1038/s41467-025-62692-z). Data Dryad berlisensi CC0 dan Figshare CC BY 4.0; atribusi dipertahankan.

Materi operasional panitia dan transkripsi bootcamp telah dikeluarkan dari snapshot publik, dengan backup lokal privat. Riwayat Git lama tetap mengandung versi sebelumnya; tidak ada penulisan ulang riwayat. Lihat [catatan penanganan](docs/PRIVACY_AND_RIGHTS.md). Ringkasan persyaratan tersedia di [COMPETITION_REQUIREMENTS.md](docs/COMPETITION_REQUIREMENTS.md).
