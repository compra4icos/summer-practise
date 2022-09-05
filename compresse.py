import zipfile

archive = "arhive.zip"
file = "saved files/7m:30d_26490.333730759.wav"

try:
    mode= zipfile.ZIP_DEFLATED
except:
    mode= zipfile.ZIP_STORED

def compressed(*, file_for_compresse: str = file, archive_file: str = archive):
    with zipfile.ZipFile(archive_file, "w", mode) as zf:
        zf.write(file_for_compresse)

def decompressed(*, archive_file: str = archive):
    with zipfile.ZipFile(archive_file, "r", mode) as zf:
        zf.extractall()
