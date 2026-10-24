# Arsitektur dan kontrak artefak 2.0

`data.py` memverifikasi dan membaca sumber → `analysis.py` mengelola fold, ranking, klasifikasi, prediksi dan manifest → `ancestry.py` menjalankan S1 donor-terpisah → `population.py` membuat PCA deskriptif → `report.py` menyusun narasi → `figures.py` merender figur mandiri.

CLI: `fetch`, `prepare`, `run`, `report`, `figures`. Cache/ZIP tidak dilacak Git. Implementasi protokol 1.0 tetap dikenali secara historis dalam audit, tetapi dashboard rilis meminta bundle 2.0 lengkap.

## Kontrak JSON yang dipakai dashboard

- `benchmark.json`: `protocolVersion`, `gitCommit`, `gitDirty`, `sourceFilesSha256`, `identityCapturedBeforeWrites`, `generatedAt`, `processingQC`, `parameters`, `datasets`.
- Setiap dataset mempertahankan nama/tipe field benchmark lama (`results`, `folds`, `selectedMarkers`, `robustness`) dan menambahkan `pairedComparisons`, `atypicalSamples`, `ancestry`, `population`.
- `ancestry.results`: per `donorBreed`, `size`, `method`, jumlah fold, `maeMean/SD`, MAE per generasi, sensitivitas BC2 dan spesifisitas deskriptif.
- `population`: daftar ras, jumlah hewan/SNP, explained variance, dan titik `{sampleId, breed, pc1, pc2, atypicalReview}`.
- Angka harus finite atau null bila metrik tidak terdefinisi; JSON tidak memuat NaN/Infinity. Unit q dan BA adalah 0–1, posisi SNP dalam base pair UMD3.1.

`benchmark.json` adalah satu sumber tampilan. Dashboard memvalidasi versi/bagian wajib dan menampilkan pesan error eksplisit bila bundle tidak lengkap; perpindahan kohort membaca dataset dari manifest yang sama sehingga tidak bisa tertukar oleh fetch yang terlambat. Teks sumber di-escape sebelum dimasukkan ke HTML/SVG. Kalkulator bisnis berasal dari skenario yang dilabeli asumsi; hasil hitung tidak disimpan sebagai bukti penjualan.

## Presentasi dan distribusi

Builder membaca metrik/manifest/konfigurasi, bukan menulis angka ilmiah secara manual. PDF menggunakan render slide yang sama dengan PPTX. Builder statis membersihkan target output yang diverifikasi, menyalin dashboard, hasil, dokumen dan paket pitch, lalu menghasilkan ZIP offline. Root redirect dan link data relatif mendukung subpath hosting.

Verifier memeriksa sumber ilmiah terhadap hash manifest, angka antar artefak, jumlah panel, berkas sumber/deck/video/offline dan batas privasi snapshot. Tag sumber dan tag rilis terpisah untuk menghindari referensi commit ke dirinya sendiri.
