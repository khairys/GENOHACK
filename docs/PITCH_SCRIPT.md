# Skrip pitch BantengPanel audited

Target slot 340 detik + buffer 20 detik = 6 menit. Ini alokasi rancangan, **bukan bukti latihan**. Versi final 7 menit: tambah 30 detik demo dan 30 detik bukti.

## 1. Intro — 0:00 sampai 0:15

Kami tim Exastra, membangun BantengPanel: prototipe desain panel SNP minimal untuk riset ancestry sapi Bali. Hari ini kami menunjukkan pipeline, data, dan batas buktinya.

## 2. Story — 0:15 sampai 0:45

Ternak Indonesia mempunyai sejarah campuran zebu dan banteng yang kompleks. Literatur memberi alasan untuk menilai referensi populasi dengan hati-hati. Sebagian studi tidak menemukan introgresi zebu pada Bali yang diteliti, sedangkan studi genom terbaru menemukan beberapa individu hibrida. Kita tidak boleh menggeneralisasi bahwa semua Bali tidak murni.

## 3. Pelanggan dan pain — 0:45 sampai 1:20

Calon pengguna kami adalah analis genetika dan peneliti ternak, dengan kepala lab atau program sebagai calon pembeli. BPTU-HPT Denpasar adalah contoh institusi pembibitan Bali yang relevan menurut situs resminya, belum pelanggan kami. Saat ini ada nol wawancara, nol LOI dan nol pilot berbayar. Validasi kebutuhan serta anggaran tetap perlu dilakukan.

## 4. Solusi — 1:20 sampai 1:45

Dua kohort publik diverifikasi dan dianalisis terpisah karena kode alelnya berbeda. Setiap fold memilih marker hanya di training. BantengPanel dibandingkan dengan Global-MAF dan tiga puluh panel acak pada ukuran dan aturan jarak yang sama. Kami menambahkan simulasi Mendelian dan PCA deskriptif.

## 5. Demo live — 1:45 sampai 3:00

Buka demo. Tunjukkan sumber commit dan jumlah hewan. Pilih referensi ONG, baca kurva MAE simulasi: lebih rendah lebih baik. Ganti donor MAD untuk menunjukkan pengaruh referensi. Buka PCA dan hewan yang perlu konfirmasi. Tunjukkan benchmark 8 SNP, ubah ukuran marker, unduh CSV. Ganti kohort ke Figshare. Bila jaringan gagal, gunakan video dua menit atau bundle offline.

## 6. Bukti — 3:00 sampai 3:45

Di Dryad, panel delapan SNP menang atas Global-MAF pada 14 dari 20 fold, seri 0 dan kalah 6. Pada empat puluh delapan SNP, balanced accuracy BantengPanel 0.960, dibanding 0.969 untuk Global-MAF. S1 Dryad versus ONG pada ukuran sama memberi MAE 0.068 dan 0.092. Hasil lengkap tetap ditampilkan untuk semua donor dan metode. Hewan atipikal bukan bukti introgresi. Simulasi bukan validasi lapangan.

## 7. TAM, ROI dan finansial — 3:45 sampai 4:10

Jumlah pasar dan willingness-to-pay belum tervalidasi. Skenario asumsi sepuluh institusi, dua proyek per tahun, harga lima belas juta menghasilkan potensi 300 juta per tahun. Margin skenario 40 persen dan LTV terhadap CAC 1.39 kali. Angka ini memperlihatkan hipotesis yang perlu diperbaiki, bukan bisnis yang sudah terbukti. ROI assay memerlukan penawaran lab.

## 8. Kompetisi — 4:10 sampai 4:30

Alternatifnya chip genome-wide, panel parentage untuk tugas berbeda, analisis khusus, serta seleksi fenotipik atau status quo. Kami menawarkan desain riset yang dapat diaudit. Kami belum mengklaim assay lebih murah atau lebih baik dari produk komersial.

## 9. GTM — 4:30 sampai 4:55

Mulai dari wawancara dan akses kohort, lanjut ke proyek desain dengan kriteria penerimaan, baru pilot bersama laboratorium. Penjualan mengikuti peneliti sebagai champion, kepala program sebagai pembeli, serta izin data dan pengadaan. Langganan hanya dipertimbangkan setelah penggunaan berulang terbukti.

## 10. Tim dan kontribusi — 4:55 sampai 5:15

Exastra terdiri dari Bramantyo, Agathan, Bowo dan Bagus. Pembagian peran dan kualifikasi individual perlu dikonfirmasi tim. Ide dan referensi sudah ada sebelum kickoff; pipeline, eksperimen, dashboard dan deck tercatat selama hackathon. Timestamp Git menunjukkan pencatatan, bukan waktu setiap bagian ditulis.

## 11. Roadmap dan ask — 5:15 sampai 5:40

Langkah berikutnya adalah kalibrasi serta validasi independen, review probe dan uji assay, lalu pilot prospektif. Kami meminta akses satu kohort Bali dengan metadata, satu mitra lab untuk menilai kelayakan panel kecil, dan introduksi kepada calon pembeli program pembibitan. Bukti dapat diaudit, hasil negatif tetap terlihat, dan batas simulasi dinyatakan jelas.

## Q&A

- Apakah hewan atipikal terbukti introgresi? Belum; label, sampel dan variasi biologis masih kemungkinan lain.
- Apakah q adalah kemurnian? S1 memakai q relatif dan target ekspektasi pedigree, bukan ancestry banteng absolut.
- Apakah sensitivitas bisa dipakai langsung? Tidak; itu titik ROC oracle pada kontrol uji yang kecil. Ambang perlu kalibrasi independen.
- Mengapa ada hasil negatif? Endpoint klasifikasi jenuh; semua baseline dan donor dilaporkan. Tidak ada pembuangan hewan agar hasil naik.
- Berapa penghematan assay? Belum diketahui; belum ada quote laboratorium atau uji assay.
- Berapa wawancara/LOI? Nol pada paket ini; hanya catatan percakapan nyata berizin boleh mengubahnya.

Catat latihan nyata di REHEARSAL_LOG.md dan cek SUBMISSION_CHECKLIST.md sebelum mengunggah.