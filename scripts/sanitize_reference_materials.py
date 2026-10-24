"""Preserve organizer material privately; remove copies from the public working tree.

Does not rewrite Git history, change permissions, or contact anyone.
"""
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "DriveKit").resolve()
backup = (ROOT / "artifacts/private/references/DriveKit").resolve()
assert source == ROOT.resolve() / "DriveKit" and backup.is_relative_to(ROOT / "artifacts/private")
files = [p for p in source.rglob("*") if p.is_file()]
if len(files) > 1:
    shutil.copytree(source, backup, dirs_exist_ok=True)
    for p in files:
        assert hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256((backup / p.relative_to(source)).read_bytes()).digest()
    shutil.rmtree(source)  # Exact verified workspace target, after byte-for-byte backup.
    source.mkdir()
source.mkdir(exist_ok=True)
(source / "README.md").write_text("# Materi panitia GENOHACK\n\nTranskripsi materi bootcamp, daftar peserta, dan detail operasional panitia tidak didistribusikan dalam snapshot produk publik. Hak cipta tetap pada penyelenggara. Tim memiliki salinan referensi lokal yang diabaikan Git. Gunakan kanal resmi panitia untuk memperoleh dokumen aslinya.\n\nRingkasan persyaratan yang ditulis tim: [Competition requirements](../docs/COMPETITION_REQUIREMENTS.md). Penghapusan dari snapshot ini tidak menghapus salinan pada riwayat Git lama.\n", encoding="utf-8")
print(f"Public reference material removed; verified local backup for {len(files)} files. History unchanged.")
