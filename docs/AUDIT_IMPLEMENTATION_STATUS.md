# Status implementasi audit MVP

Dokumen ini menutup tindak lanjut terhadap `MVP_AUDIT_DAN_RENCANA_PERBAIKAN.md` tanpa mengubah laporan audit historis. Bukti teknis final disimpan dalam `artifacts/public/release_verification.json` setelah pemeriksaan selesai.

| Audit | Perbaikan yang diimplementasikan | Bukti / batas |
|---|---|---|
| A1, C1; bug 1/2/13 | QC di-prepare ulang; provenance ditangkap sebelum output; hash kode/config; source tag dan release tag terpisah | `benchmark.json`, sumber clean saat run; PDF/deck membaca key QC yang benar |
| A1b | Prediksi held-out dan ringkasan hewan atipikal menjadi keluaran pipeline | `*_heldout_predictions.csv`, `*_atypical_samples.csv`; skor kemiripan didefinisikan eksplisit, bukan ancestry |
| B6 | S1 donor ONG/MAD terpisah, keturunan F1/BC1/BC2 dari induk uji, frekuensi/ranking training | `*_ancestry*`; titik ROC oracle dijelaskan, bukan ambang lapangan |
| B7 | PCA Figshare dan subset Dryad, flag hewan untuk konfirmasi | `*_pca.csv`, figur dan dashboard; deskriptif |
| Bug 3/4/5/6/7/8/9/10/11/12 | Label/statistik sumber, path relatif, random spacing setara, model robustness dipakai ulang, batas imputasi, dokumen scope/URL, dependensi dan tes, pembersihan output basi | Kode, protokol, runbook dan tes regresi |
| A2/A4 | Struktur pitch 11 slide mencakup seluruh bagian; tim dari daftar yang tersedia; peran/kualifikasi tidak direkayasa | PDF/PPTX, skrip; konfirmasi peran individual tetap tindakan tim |
| A3/W5 | Pemisahan sumber/ide pra-kickoff dan hasil selama hackathon | README, deck, `CONTRIBUTIONS.md`; waktu menulis perlu konfirmasi |
| B2/B3 | TAM bottom-up dan unit economics interaktif berlabel asumsi; peta alternatif 2×2 dan sumber primer | `BUSINESS_MODEL.md`, `business_scenario.json`; pasar/harga/ROI belum tervalidasi |
| B4/W2 | Demo publik, paket offline, video cadangan dua menit, link README | Status deployment dan verifikasi berkas; video merupakan walkthrough ber-caption dari tampilan aktual |
| B5/§4.3 | README produk; materi panitia dikeluarkan dari snapshot dengan backup privat terverifikasi | `PRIVACY_AND_RIGHTS.md`; riwayat lama dan kebutuhan rotasi belum hilang |
| C2 | Tes encoding, traversal ZIP, held-out leakage, jarak acak, estimator q, Mendelian dan provenance; pemeriksaan ulang metrik CSV | `tests/`, `scripts/verify_release.py`; pipeline juga dijalankan penuh |
| A5/B1 | Draf outreach, panduan, log validasi dan calon institusi bersumber disiapkan | Belum ada pengiriman pesan/wawancara nyata; jumlah tetap nol |
| A6/D/E | Checklist, skrip dan timer tersedia | Latihan manusia dan unggah submission belum dibuktikan |

## Cara menilai selesai

Pemeriksaan akhir rilis: source `fb784d54af1646058a083dfee05bd0a40879444d` di `mvp-v1.0-source`, `gitDirty: false`; dua run menghasilkan seluruh hasil kohort yang identik dan 18 CSV identik byte demi byte. Delapan tes regresi lulus, termasuk CI Linux di GitHub. Deck 11 slide lolos pemeriksaan struktur/font/chart/table dan ditinjau visual; PDF, video 120 detik, unduhan CSV dan bundle offline diperiksa. Bukti rinci berada di `release_verification.json`.

Rilis komputasional boleh disebut selesai setelah pemeriksaan kode/artefak, deck, demo dan cadangan lulus. **Definition of Done kompetisi secara keseluruhan belum otomatis terpenuhi**: konfirmasi tim, wawancara jika dilaporkan, latihan nyata dan bukti submission tetap memerlukan manusia. Tidak ada klaim wawancara, kemitraan, persetujuan tim, latihan atau pengiriman yang dibuat-buat untuk mencentang audit.

## Perbedaan terhadap angka audit historis

**Temuan tambahan yang mengubah kesimpulan 8 SNP:** ada 20 marker Dryad yang lolos call-rate/MAF gabungan tetapi tidak memiliki satu pun observasi genotipe Bali. Kode lama memakai denominator minimal satu, sehingga p_Bali yang tidak diketahui menjadi nol dan menghasilkan kontras palsu. Protokol 2.0 mengecualikan frekuensi kelas yang tidak terdefinisi. BA 8 SNP hasil terkoreksi adalah 0,945 vs Global-MAF 0,944, bukan 0,962 vs 0,940. Karena itu, pesan “keunggulan regime 8 SNP” dalam audit historis tidak dipertahankan sebagai kesimpulan rilis.

Baseline random sekarang memakai jarak yang sama dan RNG terpisah; nilainya juga berubah dari protokol lama. Skor kemiripan rilis memakai kandidat 200 marker berjarak dan mean dosis, mengecualikan missing; jangan memaksa angka 0,37/0,44 pada audit lama. Frekuensi salah klasifikasi dan indikator tinjauan dibaca dari CSV hasil ulang. Perubahan panel akibat frekuensi tak terdefinisi juga mengubah skor full-cohort. Dua hewan yang paling sering salah dikenali tetap sama, tanpa klaim status introgresi.
