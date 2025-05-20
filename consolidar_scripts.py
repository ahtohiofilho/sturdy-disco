# Lista de caminhos completos dos arquivos específicos

import os

arquivos_especificos = [
    "README.md",
    "main.py",
    "window.py",
    "contexto.py",
    "camera.py",
    "rendering/buffers.py",
    "rendering/renderer.py",
    "rendering/sahder.py",
    "shaders/picking_fs.glsl",
    "shaders/picking_vs.glsl",
    "shaders/render_fs.glsl",
    "shaders/render_vs.glsl",
    "utils/font_renderer.py",
    "utils/geografia.py",
    "utils/poligonos.py",
    "requirements.txt"
]

# Nome do arquivo consolidado
arquivo_saida = "consolidado.txt"

# Abre o arquivo de saída em modo de escrita
with open(arquivo_saida, "w", encoding="utf-8") as f_out:
    for caminho_arquivo in arquivos_especificos:
        # Verifica se o arquivo existe antes de tentar abrir
        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f_in:
                texto = f_in.read()
                f_out.write(f"Conteúdo do arquivo {os.path.basename(caminho_arquivo)}:\n")
                f_out.write(texto + "\n\n")
        else:
            print(f"⚠️ Arquivo '{caminho_arquivo}' não encontrado.")

print(f"✅ Consolidação concluída! Arquivo '{arquivo_saida}' criado com sucesso.")
