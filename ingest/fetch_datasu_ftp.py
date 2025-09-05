from ftplib import FTP
from pathlib import Path
from datetime import datetime

# Configurações
FTP_HOST = "ftp.datasus.gov.br"
FTP_DIR = "/dissemin/publicos/IBGE/POPSVS/"
LOCAL_DIR = Path("dados_brutos/POPSVS")
LOCAL_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp para versionamento
timestamp = datetime.now().strftime("%Y-%m-%d")

# Conectar ao FTP
ftp = FTP(FTP_HOST)
ftp.login()  # login anônimo
ftp.cwd(FTP_DIR)

arquivos = ftp.nlst()
print(f"{len(arquivos)} arquivos encontrados no FTP.")

# Baixar apenas arquivos CSV ou CSV.zip
for arquivo in arquivos:
    if arquivo.lower().endswith(".csv") or arquivo.lower().endswith(".csv.zip"):
        local_path = LOCAL_DIR / f"{arquivo.replace('.csv','')}_{timestamp}.csv"
        if local_path.exists():
            print(f"✅ Já existe: {local_path.name}")
            continue
        print(f"Baixando {arquivo} → {local_path.name} ...")
        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {arquivo}", f.write)

ftp.quit()
print("✅ Todos os arquivos CSV/CSV.zip foram baixados em dados_brutos/POPSVS com timestamp.")
