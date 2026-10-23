# BantengPanel — Project Overview

**Population-Aware Genomic Marker Optimization for Bali Cattle Breeding**

**Competition:** GENOHACK 2026 — Track 2: Food Security & Biodiversity Genomics  
**Team:** Exastra  
**Project Type:** Bioinformatics, Computational Genomics, Decision Support Platform  
**Development Stage:** Hackathon Minimum Viable Product (MVP)

---

## 1. Project Description

**BantengPanel** adalah platform bioinformatika yang dirancang untuk mengoptimalkan pemilihan *Single Nucleotide Polymorphism* (SNP), yaitu variasi pada posisi tertentu dalam DNA yang dapat digunakan sebagai penanda informasi genetik.

Proyek ini berfokus pada **sapi Bali (Bos javanicus domesticus)**, salah satu sumber daya genetik ternak lokal Indonesia yang penting bagi ketahanan pangan dan program pemuliaan nasional.

BantengPanel bertujuan mengidentifikasi kombinasi marker SNP yang paling informatif bagi populasi sapi Bali, kemudian mengevaluasi apakah kombinasi tersebut dapat memberikan performa analisis genetik yang lebih efisien dibandingkan marker pembanding dengan jumlah yang sama.

Sistem dikembangkan sebagai **platform analisis genomik berbasis data dan pembuktian komputasional**, bukan sebagai alat sequencing DNA atau produk uji laboratorium.

## 2. Problem Statement

Pengembangan program pemuliaan ternak membutuhkan informasi genetik yang akurat dan efisien untuk memahami karakteristik populasi serta mendukung keputusan breeding.

Namun, marker genetik yang dikembangkan menggunakan populasi sapi secara umum belum tentu menjadi kombinasi paling efisien untuk setiap populasi lokal.

Sapi Bali memiliki karakteristik genetik yang berbeda dari berbagai ras sapi lainnya. Karena itu, terdapat peluang untuk mengembangkan metode pemilihan SNP yang mempertimbangkan karakteristik populasi tersebut.

**Pertanyaan utama yang ingin dijawab:**

> Apakah kombinasi marker SNP yang dioptimalkan khusus untuk populasi sapi Bali mampu menghasilkan informasi genetik yang setara atau lebih baik dengan jumlah marker lebih sedikit dibandingkan kombinasi marker pembanding?

Keunggulan tersebut merupakan hipotesis penelitian yang harus diuji, bukan sesuatu yang diasumsikan sejak awal.

## 3. Proposed Solution

BantengPanel menyediakan sistem terintegrasi untuk:

1. **Genomic Data Processing:** Mengolah dataset genotipe sapi Bali dan populasi pembanding.
2. **Genomic Quality Control:** Memeriksa kualitas sampel dan SNP sebelum analisis.
3. **Population Analysis:** Menganalisis karakteristik serta perbedaan genetik antarpopulasi.
4. **SNP Marker Optimization:** Memilih kombinasi marker paling informatif berdasarkan karakteristik populasi.
5. **Comparative Benchmarking:** Membandingkan panel hasil optimasi terhadap baseline dengan jumlah SNP yang sama.
6. **Performance Evaluation:** Mengukur performa panel dan ketahanannya terhadap data genotipe yang tidak lengkap.
7. **Evidence-Based Reporting:** Menyajikan rekomendasi panel, hasil eksperimen, grafik, dan laporan bukti ilmiah.

Fokus inovasi bukan sekadar membuat dashboard genomik, melainkan **membangun metode pemilihan marker yang dapat diuji secara objektif dan transparan**.

## 4. How BantengPanel Works

Alur kerja utama sistem:

```text
PUBLIC GENOMIC DATASETS
          |
          v
GENOTYPE DATA PREPROCESSING
          |
          v
GENOMIC QUALITY CONTROL
          |
          v
POPULATION GENETIC ANALYSIS
          |
          v
POPULATION-AWARE SNP SELECTION
          |
          v
PANEL GENERATION
(48 / 72 / 96 / 128 / 156 / 200 SNP)
          |
          v
EQUAL-BUDGET BENCHMARKING
(Optimized vs Baseline)
          |
          v
PERFORMANCE & ROBUSTNESS EVALUATION
          |
          v
BANTENGPANEL WEB DASHBOARD
          |
          v
SNP PANEL RECOMMENDATION
+ SCIENTIFIC EVIDENCE REPORT
```

### Penjelasan Alur

**Input:** Dataset genotipe publik yang berisi ribuan hingga puluhan ribu marker SNP dari sapi Bali dan populasi pembanding.

**Processing:** Sistem membersihkan data, menganalisis informasi genetik, dan menyeleksi SNP menggunakan pendekatan berbasis genetika populasi.

**Optimization:** Sistem menghasilkan beberapa kandidat panel dengan jumlah SNP berbeda.

**Benchmarking:** Setiap kandidat dibandingkan dengan panel baseline berukuran sama menggunakan data pengujian yang tidak digunakan saat seleksi marker.

**Output:** Sistem menghasilkan daftar SNP terpilih, hasil evaluasi, visualisasi perbandingan, serta rekomendasi yang didukung data eksperimen.

## 5. MVP Scope

MVP BantengPanel difokuskan pada pembuktian kemampuan sistem dalam mengoptimalkan dan mengevaluasi kombinasi SNP melalui pendekatan *in-silico*.

### Core Features

| Fitur | Deskripsi |
|---|---|
| Genomic Dataset Processing | Membaca dan memproses dataset genotipe sapi |
| SNP Quality Control | Memfilter marker dan sampel berdasarkan kualitas data |
| SNP Optimization Engine | Menghasilkan kandidat panel berdasarkan informasi populasi |
| Multi-Size Panel Evaluation | Membandingkan beberapa ukuran panel SNP |
| Baseline Benchmarking | Menguji optimized panel terhadap random/global baseline yang valid |
| Performance Visualization | Menampilkan grafik performa dan perbandingan panel |
| SNP Panel Explorer | Menampilkan marker yang terpilih untuk setiap konfigurasi |
| Evidence Report | Menyajikan hasil evaluasi, keterbatasan, dan ekspor daftar SNP |

### MVP Limitations

Pada tahap hackathon, BantengPanel **tidak mencakup**:

- Pengambilan atau sequencing sampel DNA secara langsung.
- Pengujian laboratorium terhadap marker terpilih.
- Sertifikasi parentage atau pengganti pengujian ICAR/ISAG.
- Pembuktian hubungan induk–anak menggunakan pedigree lapangan yang tervalidasi.
- Integrasi langsung dengan sistem peternakan atau laboratorium komersial.
- Infrastruktur SaaS skala produksi.

Jika dilakukan simulasi hubungan kekerabatan, hasilnya harus diberi label sebagai validasi komputasional berbasis simulasi, bukan bukti keberhasilan pada populasi ternak nyata.

## 6. System Architecture Overview

BantengPanel dibangun menggunakan tiga komponen utama.

### A. Scientific Engine

**Technology:** Python, NumPy, Pandas, Scikit-learn, PLINK 2.

Bertanggung jawab untuk memproses data genomik, melakukan quality control, memilih marker SNP, menjalankan eksperimen benchmarking, dan menghasilkan keluaran CSV/JSON.

### B. Backend API

**Technology:** Python FastAPI.

Bertanggung jawab menyediakan hasil eksperimen, konfigurasi panel, metrik evaluasi, dan laporan untuk diakses aplikasi frontend.

Komputasi genomik utama dapat dijalankan secara offline dan hasilnya disimpan sebagai artefak yang dapat direproduksi.

### C. Web Dashboard

**Technology:** Next.js, React, Tailwind CSS, Recharts.

Bertanggung jawab menampilkan hasil analisis dalam antarmuka interaktif yang mudah dipahami pengguna dan juri hackathon.

Dashboard memungkinkan pengguna membandingkan ukuran panel, melihat grafik performa, mengeksplorasi SNP terpilih, dan mengunduh hasil analisis.

## 7. Scientific Validation

Keberhasilan BantengPanel tidak ditentukan oleh tampilan dashboard, melainkan oleh hasil pengujian terhadap baseline yang adil.

Eksperimen utama adalah **Equal-Budget SNP Benchmark**:

- Membandingkan panel hasil optimasi dan baseline dengan jumlah SNP identik.
- Menggunakan data pengujian terpisah dari data pemilihan marker.
- Mengukur kemampuan panel membedakan sapi Bali dari populasi pembanding.
- Menguji beberapa ukuran panel dan variasi eksperimen.
- Mengevaluasi performa ketika sebagian genotipe hilang atau mengandung kesalahan simulasi.
- Mendokumentasikan parameter, sumber dataset, keterbatasan, dan hasil pengujian.

**Kriteria keberhasilan:** Terdapat bukti empiris bahwa pendekatan optimasi menghasilkan peningkatan performa, efisiensi jumlah marker, atau ketahanan terhadap gangguan data dibandingkan baseline yang relevan.

Jika peningkatan tidak ditemukan, sistem harus melaporkan hasil tersebut secara transparan tanpa mengklaim keunggulan yang tidak terbukti.

## 8. Target Users & Potential Impact

Calon pengguna BantengPanel meliputi:

- Peneliti bioinformatika dan genetika ternak.
- Laboratorium analisis genetik.
- Institusi pembibitan dan pemuliaan sapi Bali.
- Lembaga penelitian serta program pelestarian sumber daya genetik ternak.

Dalam jangka panjang, BantengPanel diharapkan dapat membantu institusi terkait merancang dan mengevaluasi panel marker yang sesuai dengan karakteristik populasi ternak lokal.

Adopsi komersial, penghematan biaya, dan dampak terhadap hasil pemuliaan masih membutuhkan validasi lanjutan.

## 9. Expected MVP Deliverables

Hasil akhir pengembangan MVP meliputi:

1. **Reproducible Scientific Pipeline** — Program komputasional untuk memproses data dan menyeleksi SNP.
2. **Optimized SNP Panel Candidates** — Daftar kandidat marker untuk beberapa ukuran panel.
3. **Benchmark Results** — Perbandingan performa antara optimized panel dan baseline.
4. **Interactive Web Dashboard** — Aplikasi untuk mengeksplorasi dan memvisualisasikan hasil.
5. **Scientific Evidence Report** — Dokumentasi dataset, metode, eksperimen, hasil, dan keterbatasan.
6. **Working Demonstration** — Demonstrasi end-to-end menggunakan dataset genomik nyata yang dapat diverifikasi.

## 10. Long-Term Vision

BantengPanel dikembangkan dengan visi menjadi **platform optimasi panel marker genomik untuk populasi ternak lokal Indonesia**.

Pengembangan setelah MVP dapat mencakup validasi menggunakan dataset lebih besar, pengujian hubungan kekerabatan dengan pedigree nyata, integrasi laboratorium, evaluasi biaya assay, dan kolaborasi dengan institusi pemuliaan.

Namun, prioritas pertama adalah membuktikan bahwa pendekatan population-aware SNP selection benar-benar memberikan manfaat yang terukur.

---

## Project Summary

**BantengPanel adalah platform bioinformatika yang memproses data genomik sapi Bali, mengoptimalkan kombinasi marker SNP, membandingkan performanya dengan metode pembanding, dan menyajikan rekomendasi panel berbasis bukti ilmiah melalui dashboard interaktif.**

**Core Value:** Population-specific marker optimization supported by reproducible scientific benchmarking.

**MVP Goal:** Demonstrate whether Bali cattle–optimized SNP panels provide measurable advantages over valid equal-budget baselines.

**Development Principle:** Scientific validity first, implementation simplicity second, visualization third.