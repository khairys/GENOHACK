# Runbook BantengPanel

## Demo tanpa data mentah

Publik: https://bantengpanel-genohack.toastygecko1026.chatgpt.site . Cadangan: ekstrak `artifacts/demo/BantengPanel_offline.zip`, jalankan `python -m http.server 8000` dari folder hasil ekstraksi, buka http://localhost:8000/apps/dashboard/ . Di Windows, `launch_offline.cmd` melakukan hal yang sama. Buka melalui HTTP, bukan klik file HTML, agar fetch JSON bekerja.

## Reproduksi ilmiah

Python 3.11+ dan akses internet untuk instalasi serta unduhan pertama. Untuk angka rilis, gunakan source tag `mvp-v1.0-source` pada clone/worktree bersih; simpan data di folder yang diabaikan Git. Jangan menyalin berkas hasil baru ke checkout sebelum run, karena identitas `gitDirty` direkam saat awal.

```powershell
git clone https://github.com/khairys/GENOHACK.git
cd GENOHACK
git checkout mvp-v1.0-source
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

### Dryad

Unduh dari [DOI Dryad](https://doi.org/10.5061/dryad.th092) / [halaman dataset](https://datadryad.org/dataset/doi:10.5061/dryad.th092). Pilih `WorldWideCattleDryad.zip` (24,19 MB) atau arsip dataset lengkap. Keduanya diterima. Paket individual diharapkan memiliki MD5 `0377a330590e4e8af07c1ebe416c975a`. Berkas ZIP tidak disimpan di Git.

```powershell
python -m bantengpanel.cli fetch --dryad "D:\lokasi\WorldWideCattleDryad.zip"
python -m bantengpanel.cli prepare
python -m bantengpanel.cli run
python -m bantengpanel.cli figures
```

Figshare diunduh otomatis dari https://ndownloader.figshare.com/files/25037732 dan dicek MD5 `13f07b9bf8a0cb1e61d689cce08b30ec`. Jika akses Dryad memerlukan klik manual, unduh ZIP di browser lalu berikan path di atas; jangan mengubah checksum atau membuat data pengganti. Setelah unduhan, seluruh analisis bekerja lokal.

`prepare` harus diulang jika aturan QC/versi parser berubah. Ringkasan saat ini memakai key `excludedSamplesAboveMissingThreshold`; tidak membaca salinan cache versi lama untuk deck. `run` menghitung klasifikasi, prediksi per hewan, S1 dan PCA. `figures` memerlukan matplotlib dari extras `dev`. Durasi bergantung perangkat; progres tiap fold tercetak. Manifest mencatat versi lingkungan aktual, parameter dan hash source. Untuk environment rilis gunakan `requirements-science-lock.txt` bila tersedia di tag rilis.

## Verifikasi dan bundle

```powershell
python -m pytest -q
python scripts/build_release_metadata.py
python scripts/verify_release.py
python apps/dashboard/package_static.py
python -m http.server 8000 --directory out
```

Dashboard build: http://localhost:8000/apps/dashboard/ . Root redirect dan seluruh link internal memakai path relatif sehingga dapat dilayani di subdirektori seperti GitHub Pages. `out/` dibangun ulang dari artefak terbaru. Builder membersihkan `out/` dan salinan basi `apps/dashboard/out/` hanya setelah memverifikasi keduanya berada di lokasi workspace yang diharapkan.

Verifikasi rilis penuh memerlukan deck/video/offline yang sudah dibuat; gunakan `--science-only` untuk memeriksa hasil analisis tanpa artefak presentasi. Source tag menandai kode clean saat analisis; release tag `mvp-v1.0` memuat keluaran dan paket submission. Jangan menuntut manifest menunjuk commit yang memuat dirinya sendiri.

## Deployment

Site ID tersimpan di `.openai/hosting.json`; gunakan project yang sama, pertahankan audience public. Paket static.directory = `out`. Source dipush ke repository Sites, lalu versi dengan SHA yang sama disimpan dan dideploy. Kredensial sementara hanya lewat stdin helper; jangan menyimpannya di repo. Proses ini memerlukan akses pemilik Sites, terpisah dari reproduksi ilmiah.

## Hal yang harus dilakukan manusia

Lakukan wawancara nyata dan perbarui log, konfirmasi nama/peran serta kontribusi tim, latihan pitch dengan timer, lalu unggah submission pada kanal resmi. Artefak yang tersedia tidak berarti wawancara, latihan, atau pengiriman sudah dilakukan.
