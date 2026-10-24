# Model bisnis dan asumsi ekonomi

## Pelanggan dan proses pembelian yang diuji

Pengguna: analis/peneliti genetika ternak. Champion: peneliti pemuliaan. Pembeli ekonomi: kepala lab/program. Veto: pemilik data, standar mutu, dan pihak pengadaan. Semua peran ini **hipotesis**, belum divalidasi dalam wawancara.

Ada institusi yang relevan: [BPTU-HPT Denpasar](https://bptuhptdenpasar.ditjenpkh.pertanian.go.id/faq) menyatakan menyediakan bibit sapi Bali. Ini bukti relevansi satu institusi, bukan minat membeli, jumlah pasar nasional, atau kemitraan. Tidak ada outreach yang dinyatakan telah dilakukan.

## TAM, SAM, SOM

Rumus bottom-up: institusi yang memenuhi kriteria × proyek per institusi per tahun × nilai jasa per proyek. Jumlah institusi nasional, frekuensi proyek dan willingness-to-pay belum diketahui, sehingga **TAM/SAM/SOM terukur belum tersedia**.

Kalkulator dan deck memakai skenario ilustratif dari `configs/business.json`: 10 institusi × 2 proyek × Rp15 juta = Rp300 juta/tahun. Ketiga input adalah **asumsi tim**, bukan statistik resmi, harga laboratorium, atau TAM yang telah dibuktikan. Skenario tidak memakai jumlah seluruh ternak sebagai calon pembeli software.

## Unit economics skenario (semuanya asumsi)

| Input | Nilai | Status / dasar |
|---|---:|---|
| Harga jasa desain/proyek | Rp15 juta | Asumsi; perlu willingness-to-pay |
| Tenaga analis | 80 jam × Rp100 ribu | Asumsi = Rp8 juta |
| Komputasi langsung | Rp1 juta/proyek | Asumsi |
| Total biaya langsung | Rp9 juta/proyek | Turunan asumsi; assay tidak termasuk |
| Margin kotor | 40% | (15−9)/15; belum tervalidasi |
| Sales & marketing/periode | Rp30 juta | Asumsi |
| Pelanggan baru/periode | 2 | Asumsi |
| CAC | Rp15 juta | 30/2, turunan asumsi |
| Retensi | 2 tahun | Asumsi |
| Diskonto | 10%/tahun | Asumsi |
| Proyek/pelanggan/tahun | 2 | Asumsi |
| LTV | Jumlah gross profit tahunan terdiskonto | `(15−9)×2×(1/1.1+1/1.1²)` juta |

Rasio LTV/CAC skenario ini belum mencapai sasaran internal 3×. Itu menunjukkan kebutuhan menguji harga, produktivitas analisis, biaya penjualan, dan repeat purchase; jangan menyajikannya sebagai bisnis yang sudah layak. ROI assay dan penghematan genotyping **belum dihitung** karena harga, call rate, dan biaya platform belum tersedia.

## Alternatif dan diferensiasi

Peta 2×2 di deck/dashboard memakai sumbu cakupan populasi dan banyak/sedikit marker. [BovineSNP50 dari Illumina](https://www.illumina.com/products/by-type/microarray-kits/bovine-snp50.html) adalah contoh array genome-wide; tidak ada klaim harga pesaing. Panel parentage menjawab pedigree, sedangkan BantengPanel menguji desain ancestry: tugas dan validasi berbeda. Seleksi fenotipik/status quo juga alternatif, tetapi tidak menghasilkan ancestry DNA. Posisi BantengPanel adalah desain riset yang dapat diaudit, bukan klaim assay lebih murah.

## GTM dan finansial bertahap

1. Riset kebutuhan, review pakar dan akses kohort independen.
2. Proyek kolaboratif desain panel dengan ruang lingkup, acceptance criteria, dan biaya yang disepakati setelah penawaran nyata.
3. Review probe/strand dan feasibility laboratorium; baru setelah itu pilot prospektif.
4. Jasa per proyek lebih dahulu. Langganan hanya bila pola penggunaan berulang terbukti.

Sumber dana yang akan dicari: kolaborasi riset/pilot dan akses fasilitas; tidak ada pendanaan yang diklaim sudah diterima. Ask saat ini: satu kohort Bali independen dengan metadata, satu mitra lab untuk menilai panel kecil, dan introduksi kepada satu calon pembeli program pembibitan.
