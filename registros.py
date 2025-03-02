class Ticket:
    # Función constructora (asignar valores a los campos)
    def __init__(self, codigo, patente, vehiculo, forma_pago, pais_cabina, km_recorridos):
        self.codigo = codigo
        self.patente = patente
        self.vehiculo = vehiculo
        self.forma_pago = forma_pago
        self.pais_cabina = pais_cabina
        self.km_recorridos = km_recorridos

    # Función que retorna los datos del objeto ticket
    def __str__(self):
        r = f' | Código: {self.codigo:>11}' + f' | Patente: {self.patente:>8}'
        r += f' | Vehiculo: {self.vehiculo:^3}' + f' | Forma de pago: {self.forma_pago:^3}'
        r += f' | Pais Cabina: {self.pais_cabina:^3}' + f' | Kilómetros recorridos: {self.km_recorridos:>4} |'
        return r
