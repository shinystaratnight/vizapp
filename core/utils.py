import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from django.conf import settings


def get_nombres_series():
    nombres_series = pd.read_excel(os.path.join(settings.STATIC_ROOT, 'Nombres Series Easyviz.xlsx'))
    nombres_series.set_index('Código de serie', inplace=True)
    nombres_series['Unidades'].replace(np.nan, ' ', regex=True, inplace=True)
    return nombres_series


def consulta_bcr3(Serie1, Serie2, Serie3, Serie4, periodo, tipo1, tipo2, tipo3, tipo4, color_fondo, color_area,
                  color_linea1, color_linea2, color_linea3, color_linea4, Modificar_Serie1, Operacion1, Valor1,
                  Modificar_Serie2, Operacion2, Valor2, Modificar_Serie3, Operacion3, Valor3, Modificar_Serie4,
                  Operacion4, Valor4, Marcar_recesiones, Linea_cero, Eje_secundario2, Eje_secundario3, Eje_secundario4,
                  Cambiar_eje1, Mostrar_titulo, Cambiar_Nombre1, Cambiar_Nombre2, Cambiar_Nombre3, Cambiar_Nombre4):

    nombres_series = get_nombres_series()
    if Serie1 == '':
        print("\033[1;31m" + 'Introduzca Serie1')
    else:
        ''
        # Revisando si series son correctas / CHECKING IF CODES ARE CORRECT
    if len(nombres_series[nombres_series.index == Serie1]) == 0:
        print("\033[1;31m" + 'Introduzca una Serie1 válida')
    else:
        ''
    if (Serie2 != '') & (len(nombres_series[nombres_series.index == Serie2]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie2 válida')
    else:
        ''
    if (Serie3 != '') & (len(nombres_series[nombres_series.index == Serie3]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie3 válida')
    else:
        ''
    if (Serie4 != '') & (len(nombres_series[nombres_series.index == Serie4]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie4 válida')
    else:
        ''
        # Comparando si series son iguales / CHECKING IF CODES ARE THE SAME

    if Serie1 == Serie2 != '':
        print("\033[1;31m" + 'Series iguales detectadas, por favor introduzca series diferentes')
    elif Serie1 == Serie3:
        print("\033[1;31m" + 'Series iguales detectadas, por favor introduzca series diferentes')
    elif Serie1 == Serie4 != '':
        print("\033[1;31m" + 'Series iguales detectadas, por favor introduzca series diferentes')
    elif Serie2 == Serie3 != '':
        print("\033[1;31m" + 'Series iguales detectadas, por favor introduzca series diferentes')
    elif Serie3 == Serie4 != '':
        print("\033[1;31m" + 'Series iguales detectadas, por favor introduzca series diferentes')
    else:
        ''
        # Generando codigo final para busqueda  / SUM UP CODES
    if Serie2 == '':
        final = Serie1
        final_lista = pd.Series([Serie1]).sort_values()
    elif Serie3 == '':
        final = Serie1 + '-' + Serie2
        final_lista = pd.Series([Serie1, Serie2]).sort_values()
    elif Serie4 == '':
        final = Serie1 + '-' + Serie2 + '-' + Serie3
        final_lista = pd.Series([Serie1, Serie2, Serie3]).sort_values()
    else:
        final = Serie1 + '-' + Serie2 + '-' + Serie3 + '-' + Serie4
        # final_lista = pd.Series([Serie1,Serie2,Serie3,Serie4]).sort_values()

    # EXTRACTING DATA

    url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{}/json/{}'.format(final, periodo)
    data = requests.get(url)
    data = data.json()
    periodos = data.get("periods")

    price_index = []
    for i in periodos:
        valores_list1 = i['values'][0]
        price_index.append(valores_list1)

    if len(final) > 9:
        if nombres_series.at[Serie1, 'Frecuencia'] != nombres_series.at[Serie2, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index2 = []
        for i in periodos:
            valores_list2 = i['values'][1]
            price_index2.append(valores_list2)
    else:
        price_index2 = price_index

    if len(final) > 19:
        if nombres_series.at[Serie2, 'Frecuencia'] != nombres_series.at[Serie3, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index3 = []
        for i in periodos:
            valores_list3 = i['values'][2]
            price_index3.append(valores_list3)
    else:
        price_index3 = price_index

    if len(final) > 29:
        if nombres_series.at[Serie3, 'Frecuencia'] != nombres_series.at[Serie4, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index4 = []
        for i in periodos:
            valores_list4 = i['values'][3]
            price_index4.append(valores_list4)
    else:
        price_index4 = price_index

    fechas = []
    for i in periodos:
        nombres = i['name']
        fechas.append(nombres)

    # ORDENAR SERIES / SORT SERIES

    if len(final) == 9:
        diccionario = {"Fechas": fechas, "Serie1": price_index}
    elif len(final) == 19:
        if Serie1 < Serie2:
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2}
        else:
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2}
    elif len(final) == 29:
        if (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie3": price_index3}
        elif (Serie1 > Serie2) & (Serie1 < Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie3": price_index3}
        elif (Serie1 > Serie2) & (Serie1 > Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie1": price_index3}
        elif (Serie1 > Serie2) & (Serie1 > Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie1": price_index3}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie2": price_index3}
        elif (Serie1 < Serie2) & (Serie1 > Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie2": price_index3}
        else:
            ''
    else:
        if (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie3": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie4": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie2": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie4": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie4": price_index2, "Serie2": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie4": price_index2, "Serie3": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie3": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie4": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie1": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie4": price_index3,
                           "Serie1": price_index4}  #
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie4": price_index2, "Serie1": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie4": price_index2, "Serie3": price_index3,
                           "Serie1": price_index4}  #
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie2": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie4": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie1": price_index3,
                           "Serie4": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie4": price_index3,
                           "Serie1": price_index4}  #
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie4": price_index2, "Serie1": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie4": price_index2, "Serie2": price_index3,
                           "Serie1": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie1": price_index2, "Serie2": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie1": price_index2, "Serie3": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie2": price_index2, "Serie1": price_index3,
                           "Serie3": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie2": price_index2, "Serie3": price_index3,
                           "Serie1": price_index4}  #
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie3": price_index2, "Serie1": price_index3,
                           "Serie2": price_index4}  #
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie3": price_index2, "Serie2": price_index3,
                           "Serie1": price_index4}  #
        else:
            ''
            # DATAFRAME

    df = pd.DataFrame(diccionario)

    df.set_index('Fechas', inplace=True)
    df = df.replace('n.d.', str(np.nan), regex=True).astype(float)

    # Operaciones / OPERATIONS

    if Modificar_Serie1 == 'Si':
        if Operacion1 == '+':
            df['Serie1'] = df['Serie1'] + Valor1
        elif Operacion1 == '-':
            df['Serie1'] = df['Serie1'] - Valor1
        elif Operacion1 == '*':
            df['Serie1'] = df['Serie1'] * Valor1
        else:
            df['Serie1'] = df['Serie1'] / Valor1
    else:
        ''
    if Serie2 != '':
        if Modificar_Serie2 == 'Si':
            if Operacion2 == '+':
                df['Serie2'] = df['Serie2'] + Valor2
            elif Operacion2 == '-':
                df['Serie2'] = df['Serie2'] - Valor2
            elif Operacion2 == '*':
                df['Serie2'] = df['Serie2'] * Valor2
            else:
                df['Serie2'] = df['Serie2'] / Valor2
        else:
            ''
    else:
        ''
    if Serie3 != '':
        if Modificar_Serie3 == 'Si':
            if Operacion3 == '+':
                df['Serie3'] = df['Serie3'] + Valor3
            elif Operacion3 == '-':
                df['Serie3'] = df['Serie3'] - Valor3
            elif Operacion3 == '*':
                df['Serie3'] = df['Serie3'] * Valor3
            else:
                df['Serie3'] = df['Serie3'] / Valor3
        else:
            ''
    else:
        ''
    if Serie4 != '':
        if Modificar_Serie4 == 'Si':
            if Operacion4 == '+':
                df['Serie4'] = df['Serie4'] + Valor4
            elif Operacion4 == '-':
                df['Serie4'] = df['Serie4'] - Valor4
            elif Operacion4 == '*':
                df['Serie4'] = df['Serie4'] * Valor4
            else:
                df['Serie4'] = df['Serie4'] / Valor4
        else:
            ''
    else:
        ''
    # Leyenda / LEGEND

    title1 = nombres_series.at[Serie1, 'Nombre de serie']

    if Modificar_Serie1 == 'Si':
        if Operacion1 == '+':
            title1 = title1 + ' ' + '+' + ' ' + str(Valor1)
        elif Operacion1 == '-':
            title1 = title1 + ' ' + '-' + ' ' + str(Valor1)
        elif Operacion1 == '*':
            title1 = title1 + ' ' + '*' + ' ' + str(Valor1)
        else:
            title1 = title1 + ' ' + '/' + ' ' + str(Valor1)
    else:
        ''

    if len(final) > 18:
        title2 = nombres_series.at[Serie2, 'Nombre de serie']
    else:
        title2 = ''

    if Modificar_Serie2 == 'Si':
        if Operacion2 == '+':
            title2 = title2 + ' ' + '+' + ' ' + str(Valor2)
        elif Operacion2 == '-':
            title2 = title2 + ' ' + '-' + ' ' + str(Valor2)
        elif Operacion2 == '*':
            title2 = title2 + ' ' + '*' + ' ' + str(Valor2)
        else:
            title2 = title2 + ' ' + '/' + ' ' + str(Valor2)
    else:
        ''

    if len(final) > 28:
        title3 = nombres_series.at[Serie3, 'Nombre de serie']
    else:
        title3 = ''

    if Modificar_Serie3 == 'Si':
        if Operacion3 == '+':
            title3 = title3 + ' ' + '+' + ' ' + str(Valor3)
        elif Operacion3 == '-':
            title3 = title3 + ' ' + '-' + ' ' + str(Valor3)
        elif Operacion3 == '*':
            title3 = title3 + ' ' + '*' + ' ' + str(Valor3)
        else:
            title3 = title3 + ' ' + '/' + ' ' + str(Valor3)
    else:
        ''

    if len(final) > 38:
        title4 = nombres_series.at[Serie4, 'Nombre de serie']
    else:
        title4 = ''

    if Modificar_Serie4 == 'Si':
        if Operacion4 == '+':
            title4 = title4 + ' ' + '+' + ' ' + str(Valor4)
        elif Operacion4 == '-':
            title4 = title4 + ' ' + '-' + ' ' + str(Valor4)
        elif Operacion4 == '*':
            title4 = title4 + ' ' + '*' + ' ' + str(Valor4)
        else:
            title4 = title4 + ' ' + '/' + ' ' + str(Valor4)
    else:
        ''

    if Cambiar_Nombre1 == '':
        ''
    else:
        title1 = Cambiar_Nombre1

    if Cambiar_Nombre2 == '':
        ''
    else:
        title2 = Cambiar_Nombre2

    if Cambiar_Nombre3 == '':
        ''
    else:
        title3 = Cambiar_Nombre3

    if Cambiar_Nombre4 == '':
        ''
    else:
        title4 = Cambiar_Nombre4

    # Verificando eje secundario / CHECKING Y AXIS

    if (Serie2 == '') & (Eje_secundario2 == 'Si'):
        print(
            "\033[1;31m" + 'Coloque el código de la Serie2 para graficar en el eje secundario. Si no la tiene coloque NO en Eje_secundario2')
        # quit()
    else:
        ''
    if (Serie3 == '') & (Eje_secundario3 == 'Si'):
        print(
            "\033[1;31m" + 'Coloque el código de la Serie3 para graficar en el eje secundario. Si no la tiene coloque NO en Eje_secundario3')
        # quit()
    else:
        ''
    if (Serie4 == '') & (Eje_secundario4 == 'Si'):
        print(
            "\033[1;31m" + 'Coloque el código de la Serie4 para graficar en el eje secundario.Si no la tiene coloque NO en Eje_secundario4')
        # quit()
    else:
        ''
    # GRAFICO / GRAPH

    fig, ax = plt.subplots(constrained_layout=False, figsize=(14, 7), facecolor=color_fondo)
    indx = np.arange(len(df))

    if len(df) == 9:
        bar_width = 0
    else:
        bar_width = 0.4
    indx2 = indx.tolist()
    indices = pd.DataFrame()
    indices['indx'] = indx2
    indices['meses'] = df.index

    # CHANGING SERIES TITLES

    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'No'):
        title1 = title1
    elif (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'No'):
        title1 = title1 + ' - eje izq'
        title3 = title3 + ' - eje izq'
        title4 = title4 + ' - eje izq'
    elif (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'No'):
        title1 = title1 + ' - eje izq'
        title4 = title4 + ' - eje izq'
    elif (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'Si'):
        title1 = title1 + ' - eje izq'
    elif (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'Si'):
        title1 = title1 + ' - eje izq'
        title3 = title3 + ' - eje izq'
    elif (Eje_secundario2 == 'No') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'No'):
        title1 = title1 + ' - eje izq'
        title2 = title2 + ' - eje izq'
        title4 = title4 + ' - eje izq'
    elif (Eje_secundario2 == 'No') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'Si'):
        title1 = title1 + ' - eje izq'
        title2 = title2 + ' - eje izq'
        title3 = title3 + ' - eje izq'
    elif (Eje_secundario2 == 'No') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'Si'):
        title1 = title1 + ' - eje izq'
        title2 = title2 + ' - eje izq'
    else:
        title1 = title1

    # Y AXIS LABEL

    ylabel = nombres_series.at[Serie1, 'Unidades']

    if Serie2 == '':
        ylabel2 = ''
    else:
        ylabel2 = nombres_series.at[Serie2, 'Unidades']

    if Serie3 == '':
        ylabel3 = ''
    else:
        ylabel3 = nombres_series.at[Serie3, 'Unidades']

    if Serie4 == '':
        ylabel4 = ''
    else:
        ylabel4 = nombres_series.at[Serie4, 'Unidades']

    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'No'):
        if ylabel == ylabel2 == ylabel3 == ylabel4:
            ''
        elif (ylabel != ylabel2) & (ylabel == ylabel3) & (ylabel == ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 == ylabel4):
            ylabel = ylabel + ', ' + ylabel2
        elif (ylabel == ylabel2) & (ylabel != ylabel3) & (ylabel == ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 == ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel3
        elif (ylabel == ylabel2) & (ylabel == ylabel3) & (ylabel != ylabel4) & (ylabel2 == ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel4
        elif (ylabel == ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 == ylabel4):
            ylabel = ylabel + ', ' + ylabel3
        elif (ylabel == ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel3 + ', ' + ylabel4
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel == ylabel4) & (ylabel2 == ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel == ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel3
        elif (ylabel != ylabel2) & (ylabel == ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 == ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2
        elif (ylabel != ylabel2) & (ylabel == ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel4
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 == ylabel3) & (
                ylabel2 == ylabel4) & (ylabel3 == ylabel4):
            ylabel = ylabel + ', ' + ylabel2
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 == ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel3
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 == ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel4
        elif (ylabel != ylabel2) & (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel2 != ylabel3) & (
                ylabel2 != ylabel4) & (ylabel3 == ylabel4):
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel3
        else:
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel3 + ', ' + ylabel4
    else:
        ''

    plt.ylabel(ylabel, fontsize=14, labelpad=15)

    a = len(df)
    if a <= 12:
        c = 1
        d = 30
        width = 0.4
    elif a < 24:
        c = 2
        d = 30
        width = 0.4
    elif a < 36:
        c = 2
        d = 30
        width = 0.4
    elif a < 72:
        c = 4
        d = 30
        width = 0.4
    elif a < 216:
        c = 6
        d = 60
        width = 0.4
    elif a < 372:
        c = 12
        d = 60
    elif a < 720:
        c = 27
        d = 60
        width = 0.4
    elif a < 1080:
        c = 54
        d = 60
        width = 0.4
    elif a < 1800:
        c = 108
        d = 60
    else:
        c = 162
        d = 90
        width = 0.4

    inicio = len(df) % c - 1

    # Linea 1
    if tipo1 == 'linea':
        linea1 = ax.plot(df.index, df.Serie1, linewidth=4, color=color_linea1, label=title1)
        plt.xticks(np.arange(inicio, len(df), c), fontsize=11.5, rotation=d)
        plt.xlim(0, len(df))
        plt.tick_params(axis='x', length=10, pad=5)
    else:
        linea1 = ax.bar(indx + (bar_width / 2), df.Serie1, label=title1, width=0.4, linewidth=0, color=color_linea1)
        linea1 = ax.bar(df.index, df.Serie1, width=0, linewidth=0, color=color_fondo)
        plt.xticks(np.arange(inicio, len(df) + 1, c), fontsize=11.5, rotation=d)
        plt.tick_params(axis='x', length=10, pad=5)

    # Linea 2
    if len(final) > 9:
        if Eje_secundario2 == 'No':
            if tipo2 == 'linea':
                linea2 = plt.plot(df.index, df.Serie2, linewidth=4, color=color_linea2, label=title2)
            else:
                linea2 = ax.bar(indx - (bar_width / 2), df.Serie2, label=title2, width=0.4, linewidth=0,
                                color=color_linea2)
                linea2 = ax.bar(df.index, df.Serie2, width=0, linewidth=0, color=color_fondo)
        else:
            ''
    else:
        ''
    # Linea 3
    if len(final) > 19:
        if Eje_secundario3 == 'No':
            if tipo3 == 'linea':
                linea3 = plt.plot(df.index, df.Serie3, linewidth=4, color=color_linea3, label=title3)
            else:
                linea3 = ax.bar(indx + (bar_width / 2), df.Serie3, label=title3, width=0.4, linewidth=0,
                                color=color_linea3)
                linea3 = ax.bar(df.index, df.Serie3, width=0, linewidth=0, color=color_fondo)
        else:
            ''
    else:
        ''
    # Linea 4
    if len(final) > 29:
        if Eje_secundario4 == 'No':
            if tipo4 == 'linea':
                linea4 = plt.plot(df.index, df.Serie4, linewidth=4, color=color_linea4, label=title4)
            else:
                linea4 = ax.bar(indx - bar_width / 2, df.Serie4, label=title4, width=0.4, linewidth=0,
                                color=color_linea4)
    else:
        ''

    # Posicion leyenda / LEGEND POSITION

    titulos = [len(title1), len(title2), len(title3), len(title4)]
    titulos.sort()
    tit_mayor = titulos[-1]

    if tit_mayor < 95:
        legend = 0
    elif tit_mayor < 120:
        legend = -0.08
    else:
        legend = -0.12

    # Altura legenda / LEGEND HEIGHT

    if len(final) == 9:
        a = 0
    elif len(final) == 19:
        a = 0.02
    elif len(final) == 29:
        a = 0.04
    else:
        a = 0.08

    # Case 1
    if (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'Si'):
        ax2 = ax.twinx()
        if tipo2 == 'linea':
            linea2 = ax2.plot(df.index, df.Serie2, linewidth=4, color=color_linea2, label=title2 + ' ' + '- eje der')
        else:
            linea2 = ax2.bar(indx - (bar_width / 2), df.Serie2, label=title2, width=0.4, linewidth=0,
                             color=color_linea2)
            linea2 = ax2.bar(df.index, df.Serie2, width=0, linewidth=0, color=color_fondo)
        if tipo3 == 'linea':
            linea3 = ax2.plot(df.index, df.Serie3, linewidth=4, color=color_linea3, label=title3 + ' ' + '- eje der')
        else:
            linea3 = ax.bar(indx + (bar_width / 2), df.Serie3, label=title3, width=0.4, linewidth=0, color=color_linea3)
            linea3 = ax.bar(df.index, df.Serie3, width=0, linewidth=0, color=color_fondo)
        if tipo4 == 'linea':
            linea4 = ax2.plot(df.index, df.Serie4, linewidth=4, color=color_linea4, label=title4 + ' ' + '- eje der')
        else:
            linea4 = ax.bar(indx - bar_width / 2, df.Serie4, label=title4, width=0.4, linewidth=0, color=color_linea4)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        if ylabel2 == ylabel3 == ylabel4:
            ''
        elif (ylabel2 != ylabel3) & (ylabel2 == ylabel4) & (ylabel3 != ylabel4):
            ylabel2 = ylabel2 + ', ' + ylabel3
        elif (ylabel2 != ylabel3) & (ylabel2 != ylabel4) & (ylabel3 == ylabel4):
            ylabel2 = ylabel2 + ', ' + ylabel3
        elif (ylabel2 != ylabel3) & (ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel2 = ylabel2 + ', ' + ylabel3 + ', ' + ylabel4
        elif (ylabel2 == ylabel3) & (ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel2 = ylabel2 + ', ' + ylabel4
        elif (ylabel2 == ylabel3) & (ylabel2 != ylabel4) & (ylabel3 != ylabel4):
            ylabel2 = ylabel2 + ', ' + ylabel4
        else:
            ylabel2 = ylabel2 + ', ' + ylabel3 + ', ' + ylabel4
        ax2.set_ylabel(ylabel2, fontsize=14, labelpad=15)
        ax.legend(fontsize=14, bbox_to_anchor=(0 + legend, 1.29), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0 + legend, 1.24), loc='upper left', frameon=False, facecolor='white')
    else:
        ''
    # Case 2
    if (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'No'):
        ax2 = ax.twinx()
        if tipo2 == 'linea':
            linea2 = ax2.plot(df.index, df.Serie2, linewidth=4, color=color_linea2, label=title2 + ' ' + '- eje der')
        else:
            linea2 = ax2.bar(indx - (bar_width / 2), df.Serie2, label=title2 + ' ' + '- eje der', width=0.4,
                             linewidth=0, color=color_linea2)
            linea2 = ax2.bar(df.index, df.Serie2, width=0, linewidth=0, color=color_fondo)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel3 == ylabel4:
            ''
        elif (ylabel != ylabel3) & (ylabel == ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel3
        elif (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel3 == ylabel4):
            ylabel = ylabel + ', ' + ylabel3
        elif (ylabel != ylabel3) & (ylabel != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel3 + ', ' + ylabel4
        elif (ylabel == ylabel3) & (ylabel != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel4
        elif (ylabel == ylabel3) & (ylabel != ylabel4) & (ylabel3 != ylabel4):
            ylabel = ylabel + ', ' + ylabel4
        else:
            ylabel = ylabel + ', ' + ylabel3 + ', ' + ylabel4
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        ax2.set_ylabel(ylabel2, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.113
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0 + legend, 1.12 + a), loc='upper left', frameon=False,
                  facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0 + legend, 1.12), loc='upper left', frameon=False, facecolor='white')
    else:
        ''
    # Case 3
    if (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'No'):
        ax2 = ax.twinx()
        if tipo2 == 'linea':
            linea2 = ax2.plot(df.index, df.Serie2, linewidth=4, color=color_linea2, label=title2 + ' ' + '- eje der')
        else:
            linea2 = ax2.bar(indx - (bar_width / 2), df.Serie2, label=title2, width=0.4, linewidth=0,
                             color=color_linea2)
            linea2 = ax2.bar(df.index, df.Serie2, width=0, linewidth=0, color=color_fondo)
        if tipo3 == 'linea':
            linea3 = ax2.plot(df.index, df.Serie3, linewidth=4, color=color_linea3, label=title3 + ' ' + '- eje der')
        else:
            linea3 = ax.bar(indx + (bar_width / 2), df.Serie3, label=title3, width=0.4, linewidth=0, color=color_linea3)
            linea3 = ax.bar(df.index, df.Serie3, width=0, linewidth=0, color=color_fondo)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel4:
            ''
        else:
            ylabel = ylabel + ', ' + ylabel4
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        if ylabel2 == ylabel3:
            ''
        else:
            ylabel2 = ylabel2 + ', ' + ylabel3
        ax2.set_ylabel(ylabel2, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.113
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0, 1.093 + a), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0, 1.15), loc='upper left', frameon=False, facecolor='white')
    else:
        ''

    # Case 4
    if (Eje_secundario2 == 'Si') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'Si'):
        ax2 = ax.twinx()
        if tipo2 == 'linea':
            linea2 = ax2.plot(df.index, df.Serie2, linewidth=4, color=color_linea2, label=title2 + ' ' + '- eje der')
        else:
            linea2 = ax2.bar(indx - (bar_width / 2), df.Serie2, label=title2, width=0.4, linewidth=0,
                             color=color_linea2)
            linea2 = ax2.bar(df.index, df.Serie2, width=0, linewidth=0, color=color_fondo)
        if tipo4 == 'linea':
            linea4 = ax2.plot(df.index, df.Serie4, linewidth=4, color=color_linea4, label=title4 + ' ' + '- eje der')
        else:
            linea4 = ax.bar(indx + bar_width / 2, df.Serie4, label=title4, width=0.4, linewidth=0, color=color_linea4)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel3:
            ''
        else:
            ylabel = ylabel + ', ' + ylabel3
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        if ylabel2 == ylabel4:
            ''
        else:
            ylabel2 = ylabel2 + ', ' + ylabel4
        ax2.set_ylabel(ylabel2, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.113
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0, 1.12 + a), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0, 1.12), loc='upper left', frameon=False, facecolor='white')
    else:
        ''
    # Case 5
    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'No'):
        ax2 = ax.twinx()
        if tipo3 == 'linea':
            linea3 = ax2.plot(df.index, df.Serie3, linewidth=4, color=color_linea3, label=title3 + ' ' + '- eje der')
        else:
            linea3 = ax.bar(indx - (bar_width / 2), df.Serie3, label=title3, width=0.4, linewidth=0, color=color_linea3)
            linea3 = ax.bar(df.index, df.Serie3, width=0, linewidth=0, color=color_fondo)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        # plt.tick_params(axis='x',length=10,pad=5)
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel2 == ylabel4:
            ''
        elif ylabel == ylabel2 != ylabel4:
            ylabel = ylabel + ', ' + ylabel4
        elif ylabel != ylabel2 == ylabel4:
            ylabel = ylabel + ', ' + ylabel2
        elif ylabel == ylabel4 != ylabel2:
            ylabel = ylabel + ', ' + ylabel2
        else:
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel4
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        ax2.set_ylabel(ylabel3, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.105
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0, 1.12 + a), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0, 1.11), loc='upper left', frameon=False, facecolor='white')
    else:
        ''

    # Case 6
    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'Si'):
        ax2 = ax.twinx()
        if tipo4 == 'linea':
            linea4 = ax2.plot(df.index, df.Serie4, linewidth=4, color=color_linea4, label=title4 + ' ' + '- eje der')
        else:
            linea4 = ax.bar(indx - bar_width / 2, df.Serie4, label=title4, width=0.4, linewidth=0, color=color_linea4)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel2 == ylabel3:
            ''
        elif ylabel == ylabel2 != ylabel3:
            ylabel = ylabel + ', ' + ylabel3
        elif ylabel != ylabel2 == ylabel3:
            ylabel = ylabel + ', ' + ylabel2
        elif ylabel == ylabel3 != ylabel2:
            ylabel = ylabel + ', ' + ylabel2
        else:
            ylabel = ylabel + ', ' + ylabel2 + ', ' + ylabel3
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        ax2.set_ylabel(ylabel4, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.113
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0, 1.12 + a), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0, 1.12), loc='upper left', frameon=False, facecolor='white')
    else:
        ''
    # Case 7
    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'Si') & (Eje_secundario4 == 'Si'):
        ax2 = ax.twinx()
        if tipo3 == 'linea':
            linea3 = ax2.plot(df.index, df.Serie3, linewidth=4, color=color_linea3, label=title3 + ' ' + '- eje der')
        else:
            linea3 = ax.bar(indx - (bar_width / 2), df.Serie3, label=title3, width=0.4, linewidth=0, color=color_linea3)
            linea3 = ax.bar(df.index, df.Serie3, width=0, linewidth=0, color=color_fondo)
        if tipo4 == 'linea':
            linea4 = ax2.plot(df.index, df.Serie4, linewidth=4, color=color_linea4, label=title4 + ' ' + '- eje der')
        else:
            linea4 = ax.bar(indx + bar_width / 2, df.Serie4, label=title4, width=0.4, linewidth=0, color=color_linea4)
        ax2.grid(which='major', axis='y', linewidth=0, color=color_area)
        ax2.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=2, width=0, labelsize=12)
        ax.yaxis.set_tick_params(which='major', labelcolor='black', length=0, pad=8, width=0, labelsize=12)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
        ax.xaxis.set_tick_params(which='major', labelcolor='black', length=10, pad=5, width=0, labelsize=12)
        ax2.yaxis.set_major_formatter(ticks_y)
        ax.yaxis.set_major_formatter(ticks_y)
        ax.set_facecolor(color_area)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['bottom'].set_linewidth(1)
        if ylabel == ylabel2:
            ''
        else:
            ylabel = ylabel + ', ' + ylabel2
        ax.set_ylabel(ylabel, fontsize=14, labelpad=15)
        if ylabel3 == ylabel4:
            ''
        else:
            ylabel3 = ylabel3 + ', ' + ylabel4
        ax2.set_ylabel(ylabel3, fontsize=14, labelpad=15)
        if len(final) == 9:
            a = 0
        elif len(final) == 19:
            a = 0.057
        elif len(final) == 29:
            a = 0.113
        else:
            a = 0.171
        ax.legend(fontsize=14, bbox_to_anchor=(0, 1.12 + a), loc='upper left', frameon=False, facecolor='white')
        ax2.legend(fontsize=14, bbox_to_anchor=(0, 1.17), loc='upper left', frameon=False, facecolor='white')
    else:
        ''

    plt.xticks(np.arange(inicio, len(df), c), fontsize=11.5, rotation=d)

    plt.yticks(fontsize=12)

    if len(title1) < 95 and len(title2) < 95:
        legend = 0
    elif len(title1) > 120 or len(title2) > 120:
        legend = -0.14
    else:
        legend = -0.08

    if len(final) == 9:
        a = 0
    elif len(final) == 19:
        a = 0.02
    elif len(final) == 29:
        a = 0.04
    else:
        a = 0.08

    if (Eje_secundario2 == 'No') & (Eje_secundario3 == 'No') & (Eje_secundario4 == 'No'):
        plt.legend(fontsize=14, bbox_to_anchor=(0 + legend, 1.2 + a), loc='upper left', frameon=False,
                   facecolor='white')

    # EJE / AXIS FORMAT

    plt.grid(visible=None)
    plt.grid(which='major', axis='y', linewidth=0.5, color='lightgray')
    plt.tick_params(axis='x', length=10, pad=5)
    plt.tick_params(axis='y', length=10, pad=5)
    if tipo1 == 'linea':
        plt.xlim(0, len(df))
    else:
        plt.xlim(-1, len(df))
    if tipo2 == 'linea':
        ''
    else:
        plt.xlim(-1, len(df))
    if tipo3 == 'linea':
        ''
    else:
        plt.xlim(-1, len(df))
    if tipo4 == 'linea':
        ''
    else:
        plt.xlim(-1, len(df))
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.1f}'.format(x))
    ax.yaxis.set_major_formatter(ticks_y)

    fuente1 = nombres_series.at[Serie1, 'Fuente']
    if len(final) > 9:
        fuente2 = nombres_series.at[Serie2, 'Fuente']
    else:
        fuente2 = ' '
    if len(final) > 19:
        fuente3 = nombres_series.at[Serie3, 'Fuente']
    else:
        fuente3 = ' '

    if (fuente1 == fuente2) & (fuente2 == fuente3):
        fuente = fuente1
    elif (fuente1 != fuente2) & (fuente2 == fuente3):
        fuente = fuente1 + ', ' + fuente2
    elif (fuente1 != fuente2) & (fuente2 != fuente3):
        fuente = fuente1 + ', ' + fuente2 + ', ' + fuente3
    elif (fuente1 == fuente3) & (fuente2 != fuente3):
        fuente = fuente2 + ', ' + fuente3
    elif (fuente1 == fuente2) & (fuente1 != fuente3):
        fuente = fuente1 + ', ' + fuente3
    else:
        fuente = fuente1 + ', ' + fuente3

        # Marcar area de recesion / DATES OF RECESSIONS

    if Marcar_recesiones == 'Si':
        plt.axvspan('Mar.2020', 'Jun.2020', color='lightgray', alpha=0.3)
        plt.axvspan('T1.20', 'T2.20', color='lightgray', alpha=0.3)
        plt.axvspan('1929', '1930', color='lightgray', alpha=0.3)
        plt.axvspan('1930', '1931', color='lightgray', alpha=0.3)
        plt.axvspan('1931', '1932', color='lightgray', alpha=0.3)
        plt.axvspan('1941', '1942', color='lightgray', alpha=0.3)
        plt.axvspan('1957', '1958', color='lightgray', alpha=0.3)
        plt.axvspan('1977', '1978', color='lightgray', alpha=0.3)
        plt.axvspan('1981', '1982', color='lightgray', alpha=0.3)
        plt.axvspan('1982', '1983', color='lightgray', alpha=0.3)
        plt.axvspan('1987', '1988', color='lightgray', alpha=0.3)
        plt.axvspan('1988', '1989', color='lightgray', alpha=0.3)
        plt.axvspan('1989', '1990', color='lightgray', alpha=0.3)
        plt.axvspan('1991', '1992', color='lightgray', alpha=0.3)
        plt.axvspan('1997', '1998', color='lightgray', alpha=0.3)
        plt.axvspan('2019', '2020', color='lightgray', alpha=0.3)
    else:
        ''

    # Cambiar nombres de ejes / CHANGE AXES NAMES

    if Cambiar_eje1 == '':
        ''
    else:
        ax.set_ylabel(Cambiar_eje1, fontsize=14, labelpad=15)

    # Colocar linea  en 0
    if Linea_cero == 'Si':
        plt.axhline(0, linestyle='--', color='black', alpha=0.6)
    else:
        ''

    # Mostrar titulos / SHOW TITLES

    if Mostrar_titulo == 'Si':
        ''
    else:
        ax.legend('', fontsize=14, bbox_to_anchor=(0, 1.20), loc='upper left', frameon=False, facecolor='white')
        ax2.legend('', fontsize=14, bbox_to_anchor=(0, 1.12), loc='upper left', frameon=False, facecolor='white')

    # PLOT AREA FORMAT

    ax3 = plt.gca()
    ax3.set_facecolor(color_area)
    ax.spines['bottom'].set_color('lightgray')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Fuente / SOURCES POSITION

    if nombres_series.at[Serie1, 'Frecuencia'] == 'Mensual':
        ax3.text(0.015, -0.28, 'Fuente:' + ' ' + fuente,
                 transform=ax3.transAxes,
                 fontsize=14)
    elif nombres_series.at[Serie1, 'Frecuencia'] == 'Trimestral':
        ax3.text(0.015, -0.25, 'Fuente:' + ' ' + fuente,
                 transform=ax3.transAxes,
                 fontsize=14)
    elif nombres_series.at[Serie1, 'Frecuencia'] == 'Anual':
        ax3.text(0.015, -0.21, 'Fuente:' + ' ' + fuente,
                 transform=ax3.transAxes,
                 fontsize=14)
    else:
        ax3.text(0.015, -0.30, 'Fuente:' + ' ' + fuente,
                 transform=ax3.transAxes,
                 fontsize=14)
    if nombres_series.at[Serie1, 'Frecuencia'] == 'Mensual':
        ax3.text(0.92, -0.36, 'www.ode.pe',
                 transform=ax3.transAxes,
                 fontsize=14)
    elif nombres_series.at[Serie1, 'Frecuencia'] == 'Trimestral':
        ax3.text(0.92, -0.33, 'www.ode.pe',
                 transform=ax3.transAxes,
                 fontsize=14)
    elif nombres_series.at[Serie1, 'Frecuencia'] == 'Anual':
        ax3.text(0.92, -0.29, 'www.ode.pe',
                 transform=ax3.transAxes,
                 fontsize=14)
    else:
        ax3.text(0.92, -0.38, 'www.ode.pe',
                 transform=ax3.transAxes,
                 fontsize=14)

    if Marcar_recesiones == 'Si':
        if nombres_series.at[Serie1, 'Frecuencia'] == 'Mensual':
            ax3.text(0.015, -0.36, '* Recesiones sombreadas',
                     fontstyle='italic',
                     transform=ax3.transAxes,
                     fontsize=14)
        elif nombres_series.at[Serie1, 'Frecuencia'] == 'Trimestral':
            ax3.text(0.015, -0.33, '* Recesiones sombreadas',
                     fontstyle='italic',
                     transform=ax3.transAxes,
                     fontsize=14)
        elif nombres_series.at[Serie1, 'Frecuencia'] == 'Anual':
            ax3.text(0.015, -0.29, '* Recesiones sombreadas',
                     fontstyle='italic',
                     transform=ax3.transAxes,
                     fontsize=14)
        else:
            ax3.text(0.015, -0.38, '* Recesiones sombreadas',
                     fontstyle='italic',
                     transform=ax3.transAxes,
                     fontsize=14)
    else:
        ''

    return fig


def generate_figure(Serie1, Serie2, Serie3, Serie4, Fechas, color_fondo, Marcar_recesiones, Linea_cero,
                    Eje_secundario2, Eje_secundario3, Eje_secundario4,
          color_linea1, color_linea2, color_linea3, color_linea4, Tipo1, Tipo2, Tipo3, Tipo4):
    # Serie1 = 'PN01660XM'
    # Serie2 = 'PN01654XM'
    # Serie3 = 'PN01273PM'
    # Serie4 = 'PN01279PM'
    # Fechas = '2019-1/2021-12'  # Dates

    Modificar_Serie1 = 'No'  # Customize data
    Operacion1 = '/'  # Operation
    Valor1 = 4672.216705 / 100  # Value
    Cambiar_Nombre1 = ''  # Change title

    Modificar_Serie2 = 'No'  # Customize data
    Operacion2 = '/'  # Operation
    Valor2 = 4009.023057 / 100
    # Eje_secundario2 = 'Si'  # Y axis rigth
    Cambiar_Nombre2 = ''  # Change title

    Modificar_Serie3 = 'No'  # Customize data
    Operacion3 = '*'  # Operation
    Valor3 = -1  # Value
    # Eje_secundario3 = 'No'  # Y axis rigth
    Cambiar_Nombre3 = ''  # Change title

    Modificar_Serie4 = 'No'  # Customize data
    Operacion4 = '/'  # Operation
    Valor4 = 10  # Value
    # Eje_secundario4 = 'No'  # Y axis rigth
    Cambiar_Nombre4 = ''  # Change title

    # Tipo1 = 'linea'  # Graph type
    # Tipo2 = 'linea'  # Graph type
    # Tipo3 = 'linea'  # Graph type
    # Tipo4 = 'linea'  # Graph type
    # color_fondo = 'lavender'  # Graph frame
    color_area = 'white'  # Plot area
    # color_linea1 = 'tomato'  # Color Serie1
    # color_linea2 = 'royalblue'  # Color Serie2
    # color_linea3 = 'gold'  # Color Serie3
    # color_linea4 = 'limegreen'  # Color Serie4
    Cambiar_eje1 = ''  # Change Y axis name
    # Marcar_recesiones = 'Si'  # Recession shading
    Mostrar_titulo = 'Si'  # Show title
    # Linea_cero = 'No'  # Line in zero

    fig = consulta_bcr3(Serie1, Serie2, Serie3, Serie4, Fechas, Tipo1, Tipo2, Tipo3, Tipo4, color_fondo, color_area,
                         color_linea1, color_linea2, color_linea3, color_linea4, Modificar_Serie1, Operacion1,
                         Valor1, Modificar_Serie2, Operacion2, Valor2, Modificar_Serie3, Operacion3, Valor3,
                         Modificar_Serie4, Operacion4, Valor4, Marcar_recesiones, Linea_cero,
                         Eje_secundario2, Eje_secundario3, Eje_secundario4, Cambiar_eje1, Mostrar_titulo,
                         Cambiar_Nombre1, Cambiar_Nombre2, Cambiar_Nombre3, Cambiar_Nombre4)
    return fig


def generate_data(Serie1, Serie2, Serie3, Serie4, periodo):
    nombres_series = get_nombres_series()
    if Serie1 == '':
        print("\033[1;31m" + 'Introduzca Serie1')
    else:
        ''
        # Revisando si series son correctas
    if len(nombres_series[nombres_series.index == Serie1]) == 0:
        print("\033[1;31m" + 'Introduzca una Serie1 válida')
    else:
        ''
    if (Serie2 != '') & (len(nombres_series[nombres_series.index == Serie2]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie2 válida')
    else:
        ''
    if (Serie3 != '') & (len(nombres_series[nombres_series.index == Serie3]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie3 válida')
    else:
        ''
    if (Serie4 != '') & (len(nombres_series[nombres_series.index == Serie4]) == 0):
        print("\033[1;31m" + 'Introduzca una Serie4 válida')
    else:
        ''
        # Generando codigo final para busqueda
    if Serie2 == '':
        final = Serie1
    elif Serie3 == '':
        final = Serie1 + '-' + Serie2
    elif Serie4 == '':
        final = Serie1 + '-' + Serie2 + '-' + Serie3
    else:
        final = Serie1 + '-' + Serie2 + '-' + Serie3 + '-' + Serie4
    url = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{}/json/{}'.format(final, periodo)
    data = requests.get(url)
    data = data.json()
    periodos = data.get("periods")

    price_index = []
    for i in periodos:
        valores_list1 = i['values'][
            0]  # Modificado para que se puedan transformar los n.d en np.nam, original: [i['values'][0]]
        price_index.append(valores_list1)

    if len(final) > 9:
        if nombres_series.at[Serie1, 'Frecuencia'] != nombres_series.at[Serie2, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index2 = []
        for i in periodos:
            valores_list2 = i['values'][1]
            price_index2.append(valores_list2)
    else:
        price_index2 = price_index

    if len(final) > 19:
        if nombres_series.at[Serie2, 'Frecuencia'] != nombres_series.at[Serie3, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index3 = []
        for i in periodos:
            valores_list3 = i['values'][2]
            price_index3.append(valores_list3)
    else:
        price_index3 = price_index

    if len(final) > 29:
        if nombres_series.at[Serie3, 'Frecuencia'] != nombres_series.at[Serie4, 'Frecuencia']:
            print("\033[1;31m" + 'Elija series con las mismas frecuencias')
        else:
            ''
        price_index4 = []
        for i in periodos:
            valores_list4 = i['values'][3]
            price_index4.append(valores_list4)
    else:
        price_index4 = price_index

    fechas = []
    for i in periodos:
        nombres = i['name']
        fechas.append(nombres)

    # ORDENAR SERIES

    if len(final) == 9:
        diccionario = {"Fechas": fechas, "Serie1": price_index}
    elif len(final) == 19:
        if Serie1 < Serie2:
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2}
        else:
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2}
    elif len(final) == 29:
        if (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie3": price_index3}
        elif (Serie1 > Serie2) & (Serie1 < Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie3": price_index3}
        elif (Serie1 > Serie2) & (Serie1 > Serie3) & (Serie2 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie1": price_index3}
        elif (Serie1 > Serie2) & (Serie1 > Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie1": price_index3}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie2": price_index3}
        elif (Serie1 < Serie2) & (Serie1 > Serie3) & (Serie2 > Serie3):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie2": price_index3}
        else:
            ''
    else:
        if (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie3": price_index3,
                           "Serie4": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie2": price_index2, "Serie4": price_index3,
                           "Serie3": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie2": price_index3,
                           "Serie4": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie3": price_index2, "Serie4": price_index3,
                           "Serie2": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie4": price_index2, "Serie2": price_index3,
                           "Serie3": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie1": price_index, "Serie4": price_index2, "Serie3": price_index3,
                           "Serie2": price_index4}
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie3": price_index3,
                           "Serie4": price_index4}
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie1": price_index2, "Serie4": price_index3,
                           "Serie3": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie1": price_index3,
                           "Serie4": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie3": price_index2, "Serie4": price_index3,
                           "Serie1": price_index4}
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie4": price_index2, "Serie1": price_index3,
                           "Serie3": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie2 < Serie4) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie2": price_index, "Serie4": price_index2, "Serie3": price_index3,
                           "Serie1": price_index4}
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie2": price_index3,
                           "Serie4": price_index4}
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie1": price_index2, "Serie4": price_index3,
                           "Serie2": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie1 < Serie4) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie1": price_index3,
                           "Serie4": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie2 < Serie4) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie2": price_index2, "Serie4": price_index3,
                           "Serie1": price_index4}
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie4": price_index2, "Serie1": price_index3,
                           "Serie2": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie3 < Serie4):
            diccionario = {"Fechas": fechas, "Serie3": price_index, "Serie4": price_index2, "Serie2": price_index3,
                           "Serie1": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie1": price_index2, "Serie2": price_index3,
                           "Serie3": price_index4}
        elif (Serie1 < Serie2) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie1": price_index2, "Serie3": price_index3,
                           "Serie2": price_index4}
        elif (Serie2 < Serie1) & (Serie1 < Serie3) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie2": price_index2, "Serie1": price_index3,
                           "Serie3": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie2 < Serie3) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie2": price_index2, "Serie3": price_index3,
                           "Serie1": price_index4}
        elif (Serie1 < Serie2) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie3": price_index2, "Serie1": price_index3,
                           "Serie2": price_index4}
        elif (Serie2 < Serie1) & (Serie3 < Serie1) & (Serie4 < Serie1) & (Serie3 < Serie2) & (Serie4 < Serie2) & (
                Serie4 < Serie3):
            diccionario = {"Fechas": fechas, "Serie4": price_index, "Serie3": price_index2, "Serie2": price_index3,
                           "Serie1": price_index4}
        else:
            ''

    df = pd.DataFrame(diccionario)

    df.set_index('Fechas', inplace=True)
    df = df.replace('n.d.', str(np.nan), regex=True).astype(float)
    # df.to_excel('Data.xlsx')
    # df = df.to_excel('Data.xlsx')

    return df
