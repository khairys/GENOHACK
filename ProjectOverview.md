# BantengPanel — Project Overview

**Exastra · GENOHACK 2026 Track 2 · prototipe riset komputasional**

BantengPanel merancang dan menguji panel SNP minimal untuk studi ancestry sapi Bali. Alurnya: sumber publik → verifikasi dan QC → struktur populasi → seleksi panel di training → benchmark label sumber dan simulasi Mendelian → laporan serta dashboard.

## Kondisi implementasi

- Dryad: 1.542 hewan setelah QC, termasuk 20 Bali, 43.042 SNP autosomal.
- Figshare: 107 hewan, termasuk 16 Bali, 52.886 SNP.
- Keduanya dianalisis terpisah karena encoding alel berbeda.
- Panel 8/16/24/48/72/96/128/156/200 SNP. Baseline Global-MAF dan random memakai aturan jarak yang sama.
- Klasifikasi label sumber merupakan sanity check yang dapat jenuh. Analisis hewan atipikal tetap mempertahankan semua hewan.
- S1 menguji MAE q relatif pada F1/BC1/BC2 dari induk fold uji, dengan frekuensi dan panel dipilih dari training. PCA adalah deskripsi struktur, bukan bukti introgresi.

Nilai dan status final dibaca dari [laporan bukti](artifacts/public/evidence_report.md), bukan angka yang disalin ke deskripsi ini. Demo: https://bantengpanel-genohack.toastygecko1026.chatgpt.site .

## Pengguna dan nilai yang akan diuji

Calon pengguna: analis genetika ternak/peneliti. Calon pembeli: kepala lab/program pembibitan. Produk awal yang diuji adalah jasa desain dan audit panel per proyek. Kemampuan menghemat biaya assay, kemurnian bibit, manfaat keputusan breeding, dan willingness-to-pay belum dibuktikan. Model bisnis dan angka skenario diberi label asumsi.

## Arsitektur dan deliverable

Python/NumPy/Pandas/scikit-learn menjalankan analisis secara lokal, menulis JSON/CSV/figur dan manifest. Dashboard HTML/CSS/JS membaca artefak statis. Data mentah tetap lokal. Paket mencakup kode dan tes, laporan, kandidat marker, dashboard publik, deck PDF/PPTX, video cadangan dan demo offline.

Rincian: [MVP_SPEC](docs/MVP_SPEC.md), [SCIENTIFIC_PROTOCOL](docs/SCIENTIFIC_PROTOCOL.md), [ARCHITECTURE](docs/ARCHITECTURE.md), [RUNBOOK](docs/RUNBOOK.md), [status audit](docs/AUDIT_IMPLEMENTATION_STATUS.md).

## Batas klaim

MVP tidak menghasilkan assay siap pakai, sertifikasi kemurnian, parentage, nilai pemuliaan, atau rekomendasi breeding. q simulasi relatif terhadap referensi; label BALI sumber bukan jaminan kemurnian. Hewan atipikal perlu konfirmasi. Sampel Bali kecil, pedigree tidak diketahui, dan fold berulang saling tumpang tindih.

## Sebelum / selama hackathon

Sumber publik, ide/proposal awal, dan referensi bootcamp sudah tersedia sebelumnya. Pipeline/artefak/dashboard/deck tercatat dalam commit selama hackathon. Waktu penulisan dan kontribusi individu harus dikonfirmasi tim; [CONTRIBUTIONS](docs/CONTRIBUTIONS.md) memisahkan bukti dan asumsi.
