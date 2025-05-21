# rendering/buffers.py

import numpy as np

def prepare_buffers(contexto):
    vertices = []
    colors = []
    polygon_types = []

    for key in contexto.planeta.geografia.nodes:
        try:
            verts = contexto.planeta.poligonos[key]
        except KeyError:
            continue

        node_data = contexto.planeta.geografia.nodes[key]
        color = node_data.get('cor_bioma', (255, 255, 255))
        r, g, b = [c / 255.0 for c in color]

        polygon_types.append(len(verts))  # salva quantos vértices esse poligono tem

        for v in verts:
            vertices.extend(v)
            colors.extend([r, g, b])

    return (
        np.array(vertices, dtype=np.float32),
        np.array(colors, dtype=np.float32),
        polygon_types
    )