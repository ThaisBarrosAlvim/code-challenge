import os
import shutil
import datetime
import re
import argparse


def process(source_name):
    # Diretório base onde os arquivos JSONL estão salvos
    base_path = "../data/target-singer-jsonl/"
    # Diretório de destino organizado
    output_base_path = f"../data/{source_name}/"
    # Data atual no formato AAAA-MM-DD
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Verificar se o diretório base existe
    if not os.path.exists(base_path):
        print(f"Base path '{base_path}' does not exist. Exiting.")
        return

    # Expressão regular para remover "public-", timestamps e extensões extras
    table_name_pattern = re.compile(r"^(public-)?(.*?)-\d{8}T\d{6}\.singer(?:\.gz)?$")

    # Percorrer os arquivos no diretório base
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".singer.gz"):
                # Derivar o nome da tabela pelo nome do arquivo
                match = table_name_pattern.match(file)
                if match:
                    table_name = match.group(2)  # Pegar o nome base da tabela sem 'public-' e sem timestamp
                else:
                    print(f"Could not parse table name from file: {file}. Skipping.")
                    continue

                # Construir o caminho de destino
                destination_dir = os.path.join(output_base_path, table_name, today)
                os.makedirs(destination_dir, exist_ok=True)

                # Criar o nome do arquivo normalizado
                normalized_filename = f"{table_name}.singer.gz"

                # Mover o arquivo para o caminho de destino
                src = os.path.join(root, file)
                dest = os.path.join(destination_dir, normalized_filename)
                shutil.move(src, dest)
                print(f"Moved: {src} -> {dest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and organize .singer.gz files.")
    parser.add_argument("source_name", type=str, help="The source name to be used for organizing files.")
    args = parser.parse_args()

    process(args.source_name)
