# Protokol ilmiah BantengPanel 2.0

## Sumber dan QC

Dryad Decker PED/MAP/PEDIND dan Figshare Sudrajad dianalisis terpisah. Dryad memakai Illumina A/B, Figshare memakai kode minor/major sumber; dosis antar-kohort tidak disetarakan. Koordinat UMD3.1. Raw archive diverifikasi checksum, autosom 1–29 dipertahankan, sampel dengan missing >10% dikeluarkan. Dryad: 1.543 → 1.542 hewan, 43.043 → 43.042 SNP; Figshare: 107 dan 52.886. Duplikat ID Dryad dipertahankan sebagai kolom sumber dengan ID internal unik; jarak posisi mencegah dua salinan dipilih bersamaan.

## Klasifikasi label sumber (sanity check)

Target BALI versus semua ras pembanding. RepeatedStratifiedKFold 4 × 5, seed 20261024. Hanya training fold menentukan call rate ≥90%, pooled MAF ≥1%, kontras |p_Bali−p_other| dan ranking. Marker tanpa observasi alel di salah satu kelas tidak eligible. Logistic regression ber-class-weight, C=0.1, liblinear; imputasi modus hanya di-fit di training. Imputasi gabungan dapat memihak kelas pembanding yang besar; belum ada klaim robustness optimal.

Panel BantengPanel diranking kontras, Global-MAF diranking MAF, dan 30 panel acak memakai prioritas acak. **Ketiganya memakai aturan greedy jarak minimum 250 kb dalam kromosom.** Prefix panel yang sama dipakai untuk ukuran 8,16,24,48,72,96,128,156,200. Aturan jarak bukan LD pruning dan tidak menjamin independensi marker. RNG pemilihan panel, noise, serta simulasi dipisahkan agar penambahan satu eksperimen tidak mengubah yang lain.

Balanced accuracy dan recall Bali diukur pada fold uji. Model dan imputer yang sama dipakai untuk perturbasi 48 SNP: tambahan missing 5/10/20% serta penggantian dosis salah 1%. Prediksi per hewan disimpan. Daftar kandidat seluruh kohort diekspor terpisah dan tidak memperoleh klaim performa eksternal.

## Hewan atipikal dan PCA

CSV `*_atypical_samples.csv` menyimpan kesalahan held-out per repeat pada 48 SNP, skor kedekatan dosis ke rerata Bali vs pembanding pada kandidat 200 marker seluruh kohort, dan flag tinjauan. Flag: hewan BALI salah dikenali pada setidaknya separuh repeat. Skor kedekatan adalah post-hoc dan bukan ancestry. Hewan yang sama tidak dikeluarkan agar performa naik. Kemungkinan penyebabnya termasuk label, sampel, variasi biologis atau introgresi; belum dapat dibedakan.

PCA: Figshare seluruh 107 hewan; Dryad subset kode BALI,MAD,ONG,ACE,PES,BRE,THA,SAHW,GIR,RSIN. QC/MAF di subset penuh, hingga 3.000 SNP berjarak 250 kb, imputasi rerata dosis, skala sqrt(2p(1−p)), randomized PCA dua komponen ber-seed. PCA bersifat deskriptif; tidak dipakai untuk memilih panel atau mengukur performa. Persentase varians dan seluruh koordinat diekspor.

## S1 — simulasi Mendelian tanpa linkage

Fold sama dengan klasifikasi. Per donor ONG dan MAD secara **terpisah**, frekuensi alel Jeffreys-smoothed, QC dan ranking dihitung dari hewan BALI+donor di training fold. Ini menjawab desain referensi spesifik donor, bukan ranking klasifikasi seluruh pembanding.

BALI dan donor dari fold uji menjadi induk. Per donor/fold, 64 F1 dibuat dengan satu gamet tiap induk, lalu 64 BC1 dan BC2 melalui backcross ke induk BALI fold uji. Gamet SNP disampel independen berdasarkan dosis induk; missing parental diisi dengan draw dari frekuensi training kelompok terkait. Semua metode memakai keturunan simulasi yang sama pada union marker. Induk dipilih dengan pengembalian, sehingga keturunan saling berkaitan.

Target q adalah **ekspektasi kontribusi pedigree Bali**: F1 0,50; BC1 0,75; BC2 0,875. Realisasi ancestry per genom berbeda dari ekspektasi, terutama pada panel kecil. q diestimasi pada grid 0..1 langkah 0,01 melalui composite likelihood binomial dua referensi. Model mengasumsikan HWE dan SNP independen. q bersifat relatif terhadap pasangan frekuensi referensi; donor MAD/ONG dapat sudah admixed, dan label BALI sumber bukan jaminan kemurnian. q tidak boleh disebut proporsi banteng absolut pada ternak nyata.

MAE dilaporkan per generasi serta rerata F1/BC1/BC2. Kontrol murni diambil dari BALI fold uji (asumsi label sumber). Sensitivitas BC2 pada spesifisitas empiris ≥95% berasal dari **titik ROC oracle pada kontrol uji**, bersifat deskriptif: ambang dipilih menggunakan kontrol uji, sehingga bukan ambang kalibrasi yang boleh diterapkan. Dengan 4–5 kontrol/fold, target ≥95% praktis memerlukan nol false-positive. Ambang lapangan harus dipilih di cohort kalibrasi independen, kemudian diuji lagi. Fold donor dengan <3 hewan training atau tanpa donor uji dilewati dan dicatat.

## Ketidakpastian dan batas klaim

Hanya 20 dan 16 Bali; hubungan pedigree tidak diketahui. Fold berulang tumpang tindih, keturunan berbagi induk, sehingga rerata/SD dan jumlah menang/seri/kalah bersifat deskriptif, bukan confidence interval atau uji signifikansi. Kedua cohort bukan validasi silang terharmonisasi. Hasil simulasi tidak sama dengan validasi lapangan, uji assay, breeding value, parentage atau sertifikasi kemurnian.

## Ketertelusuran

`gitCommit` dan `gitDirty` ditangkap sebelum menulis output. SHA-256 kode ilmiah dinormalisasi UTF-8/LF agar lintas-OS; konfigurasi, versi Python/scikit-learn, checksum raw, dan QC disimpan pada manifest. Tag sumber mengidentifikasi kode bersih; tag rilis memuat artefak hasil. Rerun penuh harus memakai kode/config/environment yang tercatat, bukan mengedit angka secara manual.

## Literatur primer

[Decker 2014](https://doi.org/10.1371/journal.pgen.1004254) dan [Sudrajad 2020](https://doi.org/10.1371/journal.pone.0241038) mendasari sumber data. [Mohamad 2009](https://doi.org/10.1371/journal.pone.0005490) tidak menemukan bukti introgresi zebu di lima populasi Bali yang ditelitinya; [Wang 2025](https://doi.org/10.1038/s41467-025-62692-z) menunjukkan sejarah admixture yang kompleks dan beberapa hybrid dalam sampelnya. Temuan tersebut tidak membuktikan status hewan atipikal di MVP ini.
