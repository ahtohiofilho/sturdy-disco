# utils/geography.py

import json
import networkx
import random
import math
from statistics import mean

def letra_grega(placa):
    letras_gregas_dict = {
        "Alpha": "Α", "Beta": "Β", "Gamma": "Γ", "Delta": "Δ",
        "Epsilon": "Ε", "Zeta": "Ζ", "Eta": "Η", "Theta": "Θ",
        "Iota": "Ι", "Kappa": "Κ", "Lambda": "Λ", "Mu": "Μ",
        "Nu": "Ν", "Xi": "Ξ", "Omicron": "Ο", "Pi": "Π",
        "Rho": "Ρ", "Sigma": "Σ", "Tau": "Τ", "Upsilon": "Υ",
        "Phi": "Φ", "Chi": "Χ", "Psi": "Ψ", "Omega": "Ω"
    }
    return letras_gregas_dict.get(placa)

def definir_geografia(poligonos, fator):

    geografia = networkx.DiGraph()

    for coordenadas in poligonos:
        geografia.add_node(coordenadas)

    def tipo_de_poligono(c):
        if c == (0, 0):
            geografia.nodes[c]['tipo'] = 'pn'
            return "pn"
        elif 0 < c[0] < fator and c[1] % c[0] == 0:
            geografia.nodes[c]['tipo'] = 'ipn'
            return "ipn"
        elif 0 < c[0] < fator and c[1] % c[0] != 0:
            geografia.nodes[c]['tipo'] = 'cpn'
            return "cpn"
        elif c[0] == fator and c[1] % c[0] == 0:
            geografia.nodes[c]['tipo'] = 'ntn'
            return "ntn"
        elif c[0] == fator and c[1] % c[0] != 0:
            geografia.nodes[c]['tipo'] = 'itn'
            return "itn"
        elif fator < c[0] < fator * 2:
            geografia.nodes[c]['tipo'] = 'e'
            return "e"
        elif c[0] == fator * 2 and c[1] % fator != 0:
            geografia.nodes[c]['tipo'] = 'its'
            return "its"
        elif c[0] == fator * 2 and c[1] % fator == 0:
            geografia.nodes[c]['tipo'] = 'nts'
            return "nts"
        elif fator * 2 < c[0] < fator * 3 and c[1] % (fator * 3 - c[0]) != 0:
            geografia.nodes[c]['tipo'] = 'cps'
            return "cps"
        elif fator * 2 < c[0] < fator * 3 and c[1] % (fator * 3 - c[0]) == 0:
            geografia.nodes[c]['tipo'] = 'ips'
            return "ips"
        elif c[0] == fator * 3:
            geografia.nodes[c]['tipo'] = 'ps'
            return "ps"

    for n in list(geografia.nodes):
        no = tipo_de_poligono(n)
        if no == "pn":
            for y in range(5):
                geografia.add_edge(n, (1, y), direcao=f'S{y+1}')
            continue
        if no == "ps":
            for y in range(5):
                geografia.add_edge(n, (fator * 3 - 1, y), direcao=f'N{y+1}')
            continue
        x = n[1] // n[0]
        y = n[1] // (fator * 3 - n[0])
        if no == "ipn":
            if n[1] != n[0] * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1] + x), direcao='S')
                geografia.add_edge(n, (n[0] + 1, n[1] + x + 1), direcao='SE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] - x), direcao='N')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W') if n[1] != 0 else geografia.add_edge(n, (n[0], n[0] * 5 - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] + x - 1), direcao='SW') if n[1] != 0 else \
                                        geografia.add_edge(n, (n[0] + 1, (n[0] + 1) * 5 - 1), direcao='SW')
            else:
                geografia.add_edge(n, (n[0] + 1, n[1] + x), direcao='S')
                geografia.add_edge(n, (n[0] + 1, n[1] + x + 1), direcao='SE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] - x), direcao='N')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] + x - 1), direcao='SW')
        elif no == "cpn":
            if n[1] != n[0] * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1] + x + 1), direcao='SE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] - x), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - x - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] + x), direcao='SW')
            else:
                geografia.add_edge(n, (n[0] + 1, n[1] + x + 1), direcao='SE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, 0), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - x - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] + x), direcao='SW')
        elif no == "ntn":
            geografia.add_edge(n, (n[0] + 1, n[1]), direcao='SW')
            geografia.add_edge(n, (n[0] + 1, n[1] + 1), direcao='SE')
            geografia.add_edge(n, (n[0], n[1] + 1), direcao='NE')
            geografia.add_edge(n, (n[0] - 1, n[1] - x), direcao='N')
            geografia.add_edge(n, (n[0], n[1] - 1), direcao='NW') if n[1] != 0 else geografia.add_edge(n, (n[0], n[0] * 5 - 1), direcao='NW')
        elif no == "itn":
            if n[1] != fator * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1]), direcao='SW')
                geografia.add_edge(n, (n[0] + 1, n[1] + 1), direcao='NE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] - x), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - x - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
            else:
                geografia.add_edge(n, (n[0] + 1, n[1]), direcao='SW')
                geografia.add_edge(n, (n[0] + 1, 0), direcao='NE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, 0), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - x - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
        elif no == "e":
            if n[1] != fator * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1]), direcao='SW')
                geografia.add_edge(n, (n[0] + 1, n[1] + 1), direcao='SE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1]), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - 1), direcao='NW') if n[1] != 0 else geografia.add_edge(n, (n[0] - 1, fator * 5 - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W') if n[1] != 0 else geografia.add_edge(n, (n[0], fator * 5 - 1), direcao='W')
            else:
                geografia.add_edge(n, (n[0] + 1, n[1]), direcao='SW')
                geografia.add_edge(n, (n[0] + 1, 0), direcao='SE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1]), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
        elif no == "its":
            if n[1] != fator * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1] - y), direcao='SE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1]), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] - y - 1), direcao='SW')
            else:
                geografia.add_edge(n, (n[0] + 1, 0), direcao='SE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1]), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] - y - 1), direcao='SW')
        elif no == "nts":
            geografia.add_edge(n, (n[0] + 1, n[1] - y), direcao='S')
            geografia.add_edge(n, (n[0], n[1] + 1), direcao='SE')
            geografia.add_edge(n, (n[0] - 1, n[1]), direcao='NE')
            geografia.add_edge(n, (n[0] - 1, n[1] - 1), direcao='NW') if n[1] != 0 else geografia.add_edge(n, (n[0] - 1, fator * 5 - 1), direcao='NW')
            geografia.add_edge(n, (n[0], n[1] - 1), direcao='SW') if n[1] != 0 else geografia.add_edge(n, (n[0], fator * 5 - 1), direcao='SW')
        elif no == "cps":
            if n[1] != (fator * 3 - n[0]) * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1] - y), direcao='SE')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] + y + 1), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] - y - 1), direcao='SW')
            else:
                geografia.add_edge(n, (n[0] + 1, 0), direcao='SE')
                geografia.add_edge(n, (n[0], 0), direcao='E')
                geografia.add_edge(n, (n[0] - 1, n[1] + y + 1), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='W')
                geografia.add_edge(n, (n[0] + 1, n[1] - y - 1), direcao='SW')
        elif no == "ips":
            if n[1] != (fator * 3 - n[0]) * 5 - 1:
                geografia.add_edge(n, (n[0] + 1, n[1] - y), direcao='S')
                geografia.add_edge(n, (n[0], n[1] + 1), direcao='SE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y + 1), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y), direcao='N')
                geografia.add_edge(n, (n[0] - 1, n[1] + y - 1), direcao='NW') if n[1] != 0 else \
                                        geografia.add_edge(n, (n[0] - 1, (fator * 3 - n[0] + 1) * 5 - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='SW') if n[1] != 0 else \
                                        geografia.add_edge(n, (n[0], (fator * 3 - n[0]) * 5 - 1), direcao='SW')
            else:
                geografia.add_edge(n, (n[0] + 1, n[1] - y), direcao='S')
                geografia.add_edge(n, (n[0], 0), direcao='SE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y + 1), direcao='NE')
                geografia.add_edge(n, (n[0] - 1, n[1] + y), direcao='N')
                geografia.add_edge(n, (n[0] - 1, n[1] + y - 1), direcao='NW')
                geografia.add_edge(n, (n[0], n[1] - 1), direcao='SW')

    areas = list(poligonos.keys())
    areas_sem_definicao = {}
    areas_definidas = {}
    referencias_relevo = random.sample(areas, fator * 20)

    for area in areas:
        areas_sem_definicao[area] = []
        areas_definidas[area] = []

    for n in range(fator * 3 // 2):
        if not areas_sem_definicao:
            break
        for node in referencias_relevo:
            altitude = random.randint(0, 12)
            areas_definidas[node].append(altitude)
            if node in areas_sem_definicao:
                del areas_sem_definicao[node]
            distancias = networkx.single_source_shortest_path_length(geografia, node)
            nos_a_n_arestas = [node for node, distance in distancias.items() if distance == n + 1]
            for neighbor in nos_a_n_arestas:
                if neighbor in areas_sem_definicao and neighbor not in referencias_relevo:
                    areas_sem_definicao[neighbor].append(altitude)
        for chave in list(areas_sem_definicao.keys()):
            if areas_sem_definicao[chave]:
                areas_definidas[chave].append(round(mean(areas_sem_definicao[chave]), 3))
                del areas_sem_definicao[chave]

    chaves = list(areas_definidas.keys())
    random.shuffle(chaves)
    chaves_ordenadas = sorted(chaves, key=lambda chave: areas_definidas[chave])
    percentual_terra = random.randint(35, 45)
    limite_abissal = (100 - percentual_terra) // 2
    limite_barreira = limite_abissal + (100 - percentual_terra) // 3
    nivel_do_mar = 100 - percentual_terra
    limite_planicie = nivel_do_mar + (100 - nivel_do_mar) * 4 // 6
    limite_planalto = limite_planicie + (100 - limite_planicie) // 2

    for i, chave in enumerate(chaves_ordenadas):
        if i <= len(chaves_ordenadas) * limite_abissal // 100:
            geografia.nodes[chave]['altitude'] = 'abissal'
        elif i <= len(chaves_ordenadas) * limite_barreira // 100:
            geografia.nodes[chave]['altitude'] = 'barreira'
        elif i <= len(chaves_ordenadas) * nivel_do_mar // 100:
            geografia.nodes[chave]['altitude'] = 'plataforma'
        elif i <= len(chaves_ordenadas) * limite_planicie // 100:
            geografia.nodes[chave]['altitude'] = 'planicie'
        elif i <= len(chaves_ordenadas) * limite_planalto // 100:
            geografia.nodes[chave]['altitude'] = 'planalto'
        else:
            geografia.nodes[chave]['altitude'] = 'cordilheira'

    areas_sem_definicao = {}
    areas_definidas = {}
    referencias_umidade = random.sample(areas, 60)

    for area in areas:
        areas_sem_definicao[area] = []
        areas_definidas[area] = []

    for n in range(fator * 3 // 2):
        if not areas_sem_definicao:
            break
        for node in referencias_umidade:
            altitude = random.randint(0, 12)
            areas_definidas[node].append(altitude)
            if node in areas_sem_definicao:
                del areas_sem_definicao[node]
            distancias = networkx.single_source_shortest_path_length(geografia, node)
            nos_a_n_arestas = [node for node, distance in distancias.items() if distance == n + 1]
            for neighbor in nos_a_n_arestas:
                if neighbor in areas_sem_definicao and neighbor not in referencias_umidade:
                    areas_sem_definicao[neighbor].append(altitude)
        for chave in list(areas_sem_definicao.keys()):
            if areas_sem_definicao[chave]:
                areas_definidas[chave].append(round(mean(areas_sem_definicao[chave]), 3))
                del areas_sem_definicao[chave]

    chaves = list(areas_definidas.keys())
    random.shuffle(chaves)
    chaves_ordenadas = sorted(chaves, key=lambda chave: areas_definidas[chave])

    for i, chave in enumerate(chaves_ordenadas):
        if i <= len(chaves_ordenadas) * 25 // 100:
            geografia.nodes[chave]['umidade'] = 'arido'
        elif i <= len(chaves_ordenadas) * 50 // 100:
            geografia.nodes[chave]['umidade'] = 'semi-arido'
        elif i <= len(chaves_ordenadas) * 75 // 100:
            geografia.nodes[chave]['umidade'] = 'fertil'
        else:
            geografia.nodes[chave]['umidade'] = 'umido'

    # Definição das placas com dois pontos de referência cada
    placas = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta',
            'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu',
            'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma',
            'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
    
    # Gerar duas referências para cada placa (total 48)
    placas_duplicadas = placas * 2
    random.shuffle(placas_duplicadas)
    referencias_geologia = random.sample(areas, 48)

    # Atribuir cada referência a uma placa
    areas_definidas = {area: None for area in areas}
    for i, node in enumerate(referencias_geologia):
        areas_definidas[node] = placas_duplicadas[i]

    # Calcular a placa para cada nó baseado na proximidade
    for node in areas_definidas:
        if areas_definidas[node] is not None:
            continue  # Pula pontos de referência já definidos
        
        # Encontrar todas as distâncias para pontos de referência
        distancias = []
        for ref in referencias_geologia:
            try:
                dist = networkx.shortest_path_length(geografia, ref, node)
                distancias.append( (ref, dist) )
            except networkx.exception.NetworkXNoPath:
                continue
        
        if not distancias:
            areas_definidas[node] = random.choice(placas)
            continue
        
        # Encontrar a distância mínima
        min_dist = min(d[1] for d in distancias)
        candidatos = [d[0] for d in distancias if d[1] == min_dist]
        
        # Escolher aleatoriamente entre candidatos equidistantes
        ref_escolhida = random.choice(candidatos)
        areas_definidas[node] = areas_definidas[ref_escolhida]
    
    coeficiente_movimento = 300

    # Gerar cores para as placas
    cores_placas = []
    for _ in range(24):
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            if (r + g + b) > 127.5:
                cores_placas.append((r, g, b))
                break

    latitude_equador = fator * 3 / 2

    for chave, valor in areas_definidas.items():
        geografia.nodes[chave]['placa'] = valor
        geografia.nodes[chave]['cor_placa'] = cores_placas[placas.index(valor)]
        geografia.nodes[chave]['letra_grega'] = letra_grega(geografia.nodes[chave]['placa'])
        if chave[0] < latitude_equador:
            distancia_para_equador = latitude_equador - chave[0]
            angulo = distancia_para_equador * 90 / latitude_equador
            incidencia_solar = math.cos(math.radians(angulo))
        elif chave[0] == latitude_equador:
            distancia_para_equador = 0
            angulo = distancia_para_equador * 90 / latitude_equador
            incidencia_solar = math.cos(math.radians(angulo))
        else:
            distancia_para_equador = chave[0] - latitude_equador
            angulo = distancia_para_equador * 90 / latitude_equador
            incidencia_solar = math.cos(math.radians(angulo))
        if geografia.nodes[chave]['altitude'] == 'abissal' \
        or geografia.nodes[chave]['altitude'] == 'barreira' \
        or geografia.nodes[chave]['altitude'] == 'plataforma':
            fator_altitude = 3
        elif geografia.nodes[chave]['altitude'] == 'planicie':
            fator_altitude = 1
        elif geografia.nodes[chave]['altitude'] == 'planalto':
            fator_altitude = -1
        elif geografia.nodes[chave]['altitude'] == 'cordilheira':
            fator_altitude = -3
        if geografia.nodes[chave]['umidade'] == 'umido':
            fator_umidade = 1.5
        elif geografia.nodes[chave]['umidade'] == 'fertil':
            fator_umidade = 0.5
        elif geografia.nodes[chave]['umidade'] == 'semi-arido':
            fator_umidade = -0.5
        elif geografia.nodes[chave]['umidade'] == 'arido':
            fator_umidade = -1.5
        geografia.nodes[chave]['temperatura'] = round(40 * incidencia_solar - 8 + fator_altitude + fator_umidade, 1) - 4

    for node, atributos in geografia.nodes(data = True):
        temperatura = atributos.get('temperatura')
        altitude = atributos.get('altitude')
        umidade = atributos.get('umidade')
        if temperatura < 0:
            geografia.nodes[node]['bioma'] = 'polo'
            geografia.nodes[node]['cust_mob'] = 8 * coeficiente_movimento
            geografia.nodes[node]['prod_agric'] = 0
        else:
            if altitude == 'cordilheira':
                geografia.nodes[node]['bioma'] = 'montanha'
                geografia.nodes[node]['cust_mob'] = 4 * coeficiente_movimento
                geografia.nodes[node]['prod_agric'] = 1 / 2
            elif altitude == 'planalto':
                    geografia.nodes[node]['bioma'] = 'estepe'
                    geografia.nodes[node]['cust_mob'] = 2 * coeficiente_movimento
                    geografia.nodes[node]['prod_agric'] = 2
            elif altitude == 'planicie':
                if umidade == 'umido':
                    geografia.nodes[node]['bioma'] = 'floresta'
                    geografia.nodes[node]['cust_mob'] = 1.5 * coeficiente_movimento
                    geografia.nodes[node]['prod_agric'] = 3
                elif umidade == 'fertil':
                    geografia.nodes[node]['bioma'] = 'prado'
                    geografia.nodes[node]['cust_mob'] = 1 * coeficiente_movimento
                    geografia.nodes[node]['prod_agric'] = 4
                elif umidade == 'semi-arido':
                    geografia.nodes[node]['bioma'] = 'savana'
                    geografia.nodes[node]['cust_mob'] = 1 * coeficiente_movimento
                    geografia.nodes[node]['prod_agric'] = 1
                else:
                    geografia.nodes[node]['bioma'] = 'deserto'
                    geografia.nodes[node]['cust_mob'] = 1.5 * coeficiente_movimento
                    geografia.nodes[node]['prod_agric'] = 1 / 3
            elif altitude == 'plataforma':
                geografia.nodes[node]['bioma'] = 'costa'
                geografia.nodes[node]['cust_mob'] = 0.3 * coeficiente_movimento
                geografia.nodes[node]['prod_agric'] = 0
            elif altitude == 'barreira':
                geografia.nodes[node]['bioma'] = 'mar'
                geografia.nodes[node]['cust_mob'] = 0.25 * coeficiente_movimento
                geografia.nodes[node]['prod_agric'] = 0
            else:
                geografia.nodes[node]['bioma'] = 'oceano'
                geografia.nodes[node]['cust_mob'] = 0.2 * coeficiente_movimento
                geografia.nodes[node]['prod_agric'] = 0

    for u, v, data in geografia.edges(data = True):
        mob_u = geografia.nodes[u]['cust_mob']
        mob_v = geografia.nodes[v]['cust_mob']
        if geografia.nodes[u]['bioma'] in ['costa', 'mar', 'oceano'] != (geografia.nodes[v]['bioma'] in ['costa', 'mar', 'oceano']):
            geografia[u][v]['cust_mob'] = (mob_u + mob_v) / 2 + coeficiente_movimento / 2
        else:
            geografia[u][v]['cust_mob'] = (mob_u + mob_v) / 2

    cores_biomas = {
        'oceano': (0, 23, 98), 'mar': (8, 33, 113), 'costa': (12, 71, 108), 'prado': (91, 174, 70), 'savana': (231, 190, 141),
        'floresta': (75, 129, 66), 'deserto': (242, 242, 166), 'estepe': (201, 147, 121), 'montanha': (158, 86, 86), 'polo': (245, 255, 245)
    }

    prados = []

    for node in geografia.nodes:
        geografia.nodes[node]['cor_bioma'] = cores_biomas[geografia.nodes[node]['bioma']]
        if geografia.nodes[node]['bioma'] == 'prado':
            prados.append(node)

    # Grava o grafo em um arquivo JSON
    with open("geografia.json", "w") as arquivo:
        json.dump(networkx.node_link_data(geografia), arquivo)
    
    return geografia, len(prados) // 2
