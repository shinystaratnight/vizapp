from django.shortcuts import render
from core.utils import consulta_bcr3

def home(request):
    Serie1 = 'PN01660XM'
    Serie2 = 'PN01654XM'
    Serie3 = 'PN01273PM'
    Serie4 = 'PN01279PM'
    Fechas = '2019-1/2021-12'  # Dates

    Modificar_Serie1 = 'No'  # Customize data
    Operacion1 = '/'  # Operation
    Valor1 = 4672.216705 / 100  # Value
    Cambiar_Nombre1 = ''  # Change title

    Modificar_Serie2 = 'No'  # Customize data
    Operacion2 = '/'  # Operation
    Valor2 = 4009.023057 / 100
    Eje_secundario2 = 'No'  # Y axis rigth
    Cambiar_Nombre2 = ''  # Change title

    Modificar_Serie3 = 'No'  # Customize data
    Operacion3 = '*'  # Operation
    Valor3 = -1  # Value
    Eje_secundario3 = 'Si'  # Y axis rigth
    Cambiar_Nombre3 = ''  # Change title

    Modificar_Serie4 = 'No'  # Customize data
    Operacion4 = '/'  # Operation
    Valor4 = 10  # Value
    Eje_secundario4 = 'No'  # Y axis rigth
    Cambiar_Nombre4 = ''  # Change title

    Tipo1 = 'linea'  # Graph type
    Tipo2 = 'linea'  # Graph type
    Tipo3 = 'linea'  # Graph type
    Tipo4 = 'linea'  # Graph type
    color_fondo = 'mintcream'  # Graph frame
    color_area = 'mintcream'  # Plot area
    color_linea1 = 'tomato'  # Color Serie1
    color_linea2 = 'royalblue'  # Color Serie2
    color_linea3 = 'gold'  # Color Serie3
    color_linea4 = 'limegreen'  # Color Serie4
    Cambiar_eje1 = ''  # Change Y axis name
    Marcar_recesiones = 'Si'  # Recession shading
    Mostrar_titulo = 'Si'  # Show title
    Linea_cero = 'No'  # Line in zero
    context = {}
    context['graph'] = consulta_bcr3(Serie1, Serie2, Serie3, Serie4, Fechas, Tipo1, Tipo2, Tipo3, Tipo4, color_fondo, color_area,
                            color_linea1, color_linea2, color_linea3, color_linea4, Modificar_Serie1, Operacion1,
                            Valor1, Modificar_Serie2, Operacion2, Valor2, Modificar_Serie3, Operacion3, Valor3,
                            Modificar_Serie4, Operacion4, Valor4, Marcar_recesiones, Linea_cero,
                            Eje_secundario2, Eje_secundario3, Eje_secundario4, Cambiar_eje1, Mostrar_titulo,
                            Cambiar_Nombre1, Cambiar_Nombre2, Cambiar_Nombre3, Cambiar_Nombre4)

    return render(request, 'home.html', context)

