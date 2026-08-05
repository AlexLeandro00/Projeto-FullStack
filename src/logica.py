from datetime import date

def calcular_dias_restantes(recurso):
    dias_desde_compra = (date.today() - recurso.data_ultima_compra).days
    dias_restantes = recurso.intervalo_medio_dias - dias_desde_compra
    return dias_restantes
