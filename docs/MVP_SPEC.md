# BantengPanel — Spesifikasi MVP audited

## Produk dan tujuan

Prototipe riset desain panel SNP minimal bagi studi ancestry sapi Bali. Endpoint utama tambahan adalah MAE estimasi q relatif pada simulasi S1; klasifikasi label sumber tetap sebagai sanity check. Panel belum memverifikasi kemurnian, parentage, atau performa ternak nyata.

## Fitur

| Fitur | Implementasi |
|---|---|
| Akuisisi/QC | Dua kohort, checksum, ZIP aman, parser sumber, autosom, missing sampel |
| Seleksi panel | Kontras frekuensi alel training; Global-MAF dan random dengan jarak sama |
| Benchmark | 8–200 SNP, 20 fold, 30 panel acak, BA/recall, robustness 48 SNP |
| Ancestry S1 | F1/BC1/BC2 dari induk uji, referensi training per ONG/MAD, MAE dan ROC deskriptif |
| Populasi | PCA subset eksplisit, hewan atipikal dan prediksi held-out |
| Dashboard | Pilihan kohort/donor/panel, kurva, PCA, tabel, CSV, kalkulator asumsi |
| Ketertelusuran | Snapshot commit sebelum penulisan, hash sumber/config, checksum raw |
| Submission | Deck PDF/PPTX, skrip pitch, video 2 menit, bundle offline, model bisnis berlabel |

## Batas selesai

Rilis teknis selesai saat pipeline/config/source hash cocok, tes bermakna lulus, dashboard/CSV/deck memakai hasil yang sama, paket lokal dan publik berfungsi, dan tidak ada placeholder di deliverable. Ketidakunggulan suatu metode tetap hasil sah.

Kesiapan kompetisi lengkap juga memerlukan pekerjaan manusia: wawancara jika dilaporkan, persetujuan kontribusi/peran tim, latihan 6 menit, dan unggah sesuai tenggat. Status keduanya dipisahkan pada `AUDIT_IMPLEMENTATION_STATUS.md`.

## Kriteria penelitian

Laporkan apakah panel memberikan MAE/sensitivitas/efisiensi yang lebih baik dari baseline setara. Jangan mencari atau membuang hewan agar metode terlihat unggul. S1 bersifat eksploratif dan mengasumsikan linkage/HWE sederhana; kemenangan simulasi bukan bukti lapangan.
