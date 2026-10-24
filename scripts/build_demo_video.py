"""Two-minute captioned walkthrough using genuine, unmodified dashboard views."""
import json
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
facts = json.loads((ROOT / "artifacts/public/pitch_facts.json").read_text())
frames = ROOT / "artifacts/demo/frames"
work = ROOT / "artifacts/qa/video"
work.mkdir(parents=True, exist_ok=True)
steps = [
    ("00-intro.png", 15, "BantengPanel: prototipe riset panel SNP minimal. Dua kohort publik dianalisis terpisah; bukan uji kemurnian ternak."),
    ("01-s1-ong.png", 20, "S1 memakai induk fold uji dan frekuensi training. Pilih ONG: MAE lebih rendah berarti estimasi campuran simulasi lebih dekat ke target pedigree."),
    ("02-s1-mad.png", 15, "Ganti donor ke MAD. Referensi memengaruhi hasil; q bersifat relatif, bukan proporsi banteng absolut. Semua metode memakai keturunan yang sama."),
    ("03-pca.png", 20, "PCA mendeskripsikan struktur populasi. Dua hewan Bali sering salah dikenali; perlu konfirmasi label/sampel. Posisi PCA tidak membuktikan introgresi."),
    ("04-classification.png", 15, "Benchmark biner tetap terlihat, termasuk hasil yang tidak unggul. Marker dengan frekuensi kelas tak terdefinisi sudah dikeluarkan; angka versi lama diganti."),
    ("05-markers.png", 15, "Pilih panel 8 SNP dan unduh CSV kandidat. Daftar full-cohort bukan panel yang sudah divalidasi eksternal. QC, baseline dan batas klaim dapat diperiksa."),
    ("06-figshare.png", 10, "Pilih Figshare: 107 hewan, 16 Bali. Jangan menggabungkan dosis alel kedua kohort tanpa harmonisasi. Grafik membaca artefak analisis."),
    ("07-business.png", 10, "Kalkulator bisnis adalah skenario asumsi, bukan TAM terukur atau traksi. Harga, kebutuhan pembeli dan biaya assay memerlukan validasi nyata.")]
font_path = Path("C:/Windows/Fonts/arial.ttf")
font = ImageFont.truetype(str(font_path), 26)
small = ImageFont.truetype(str(font_path), 20)
manifest = []
concat = []
for i, (name, duration, caption) in enumerate(steps):
    screenshot = Image.open(frames / name).convert("RGB")
    # Preserve the entire screenshot, with a separate caption band underneath.
    canvas = Image.new("RGB", (1280, 940), "#F4F7F3")
    screenshot.thumbnail((1280, 800))
    canvas.paste(screenshot, ((1280-screenshot.width)//2, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0,800,1280,940), fill="#16333A")
    draw.text((26,810), f"{i+1:02d}/08   BANTENGPANEL · WALKTHROUGH DEMO · TANPA AUDIO", font=small, fill="#A8D8C7")
    draw.multiline_text((26,844), "\n".join(textwrap.wrap(caption, 94)), font=font, fill="white", spacing=6)
    target = work / f"frame-{i:02d}.png"
    canvas.save(target)
    concat += [f"file '{target.as_posix()}'", f"duration {duration}"]
    manifest.append({"frame": name, "seconds": duration, "caption": caption})
concat.append(f"file '{target.as_posix()}'")
playlist = work / "frames.txt"
playlist.write_text("\n".join(concat), encoding="utf-8")
output = ROOT / "artifacts/demo/BantengPanel_demo_2min.mp4"
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(playlist), "-t", "120", "-r", "24", "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)], check=True)
(ROOT / "artifacts/public/demo_video.json").write_text(json.dumps({"durationSeconds": sum(s[1] for s in steps), "format": "Captioned slideshow walkthrough of actual dashboard views; no audio", "frames": manifest}, indent=2), encoding="utf-8")
print(output)
