# Incluir modulo
from registros import *
import pickle
import os.path


def patente_pais(pat):  # Función para definir la nacionalidad de la patente
    # Tupla = ('Argentina', 'Paraguay', 'Uruguay', 'Chile', 'Bolivia', 'Brasil', 'Otro')
    if pat[0] == ' ' and pat[1:5].isalpha() and pat[5:7].isdigit():
        return 3

    elif pat[0:2].isalpha() and pat[2:5].isdigit() and pat[5:7].isalpha():
        return 0

    elif pat[0:2].isalpha() and pat[2:7].isdigit():
        return 4

    elif pat[0:3].isalpha() and pat[3].isdigit() and pat[4].isalpha() and pat[5:7].isdigit():
        return 5

    elif pat[0:4].isalpha() and pat[4:7].isdigit():
        return 1

    elif pat[0:3].isalpha() and pat[3:7].isdigit():
        return 2

    else:
        return 6


def mostrar_menu():  # Función de Menu de Opciones...
    print()
    print('====' * 38)
    print('\t\t\t\t\t\t\t GESTION DE CABINA DE PEAJES')
    print('\t\t\t\t\t\t\t\t MENU DE OPCIONES: ')
    print()
    print('1 -> Crear archivo binario a partir de los tickets de un archivo de texto')
    print()
    print('2 -> Cargar por teclado los datos de un ticket')
    print()
    print('3 -> Mostrar todos los registros del arreglo, ordenados por código de ticket, de menor a mayor')
    print()
    print('4 -> Buscar en el archivo un registro según su patente')
    print()
    print('5 -> Buscar un registro por código de ticket')
    print()
    print('6 -> Mostrar la cantidad de vehículos de cada combinación posible')
    print()
    print('7 -> Mostrar la cantidad contada de cada vehículo y la cantidad de vehículos por pais')
    print()
    print('8 -> Mostrar la distancia promedio entre todos los vehículos, y mostrar también '
          'los datos de los vehículos que la hayan superado')
    print()
    print('0 -> Salir.')
    print('====' * 38)
    print()


def generar_archivo_bin(fd):  # Función para generar el archivo binario...
    if not os.path.exists('peajes-tp4.csv'):
        print('ERROR!!!')
        print('No se puede encontrar el archivo')
        return

    texto = open('peajes-tp4.csv', 'rt')
    texto.readline()
    texto.readline()
    binario = open(fd, 'wb')
    for linea in texto:
        if linea == '':
            break
        ticket = generar_registro(linea)
        pickle.dump(ticket, binario)

    texto.close()
    binario.close()
    print('Listo...')


def generar_registro(linea):  # Genera el registro para el archivo binario...
    if linea[-1] == '\n':
        linea = linea[:-1]

    token = linea.split(',')
    cod = int(token[0])
    pat = token[1]
    vehiculo = int(token[2])
    forma_pago = int(token[3])
    pais_cabina = int(token[4])
    distancia = int(token[5])
    return Ticket(cod, pat, vehiculo, forma_pago, pais_cabina, distancia)


# Funciones de validación...
def validar_int(li=None, ls=None, men=''):  # Validación de Enteros...
    while True:
        num = input(men)
        if num.isdigit():
            num = int(num)
            lim_inf = lim_sup = False
            if li is None:
                lim_inf = True
            elif num > li:
                lim_inf = True

            if ls is None:
                lim_sup = True
            elif num < ls:
                lim_sup = True

            if lim_inf and lim_sup:
                return num
        print('Ingrese un numero valido...')


def validar_cadena(men):  # Validación de cadenas de caracteres...
    while True:
        cad = input(men)
        if isinstance(cad, str):
            return cad
        print('INVALIDO...Por favor, ingrese una cadena de caracteres')


def cargar_registro(fd):  # Función de carga manual de registro...
    codigo = validar_int(men='Ingrese el código del Ticket: ')
    patente = validar_cadena('Ingrese la patente del vehiculo: ')
    vehiculo = validar_int(0, 2, 'Ingrese el tipo de Vehiculo (0: motocicleta, 1: automóvil, 2: camión): ')
    forma_pago = validar_int(1, 2, 'Ingrese la forma de pago  (1: manual, 2 telepeaje): ')
    pais_cabina = validar_int(0, 4, 'Ingrese el pais de la cabina que realizo el cobro (0: Argentina - '
                                    '1: Bolivia - 2: Brasil - 3: Paraguay - 4: Uruguay): ')
    km_recorridos = validar_int(li=0, men='Ingrese los km recorridos desde la cabina anterior '
                                          '(ingrese un 0 si la cabina actual es la primera): ')

    ticket = Ticket(codigo, patente, vehiculo, forma_pago, pais_cabina, km_recorridos)
    binario = open(fd, 'ab')
    pickle.dump(ticket, binario)
    binario.close()


def mostrar_archivo(fd):  # Función para mostrar el contenido del archivo...
    paises = ('Argentina', 'Paraguay', 'Uruguay', 'Chile', 'Bolivia', 'Brasil', 'Otro')
    binario = open(fd, 'rb')
    tam = os.path.getsize(fd)
    while tam > binario.tell():
        reg = pickle.load(binario)
        print(reg, f' País Patente: {paises[patente_pais(reg.patente)]:<10} |')
    binario.close()


def buscar_patente(fd):  # Funcion de busqueda de patente...
    cp = 0
    pat = validar_cadena('Ingrese la patente que desea buscar: ')
    binario = open(fd, 'rb')
    tam = os.path.getsize(fd)
    while binario.tell() < tam:
        reg = pickle.load(binario)
        if reg.patente == pat:
            print(reg)
            cp += 1
    if cp > 0:
        print(f'En total, hubo {cp} registros para la patente {pat}')
    else:
        print('No se encontró un registro con esa patente...')

    binario.close()


def busqueda_codigo(fd):  # Función de Búsqueda de ticket especifico...
    c_bus = validar_int(men='Ingrese el código que desee buscar: ')
    not_cod = False
    binario = open(fd, 'rb')
    tam = os.path.getsize(fd)
    while tam > binario.tell():
        reg = pickle.load(binario)
        if reg.codigo == c_bus:
            print('Se encontró el código buscado')
            print(reg)
            not_cod = True
            break
    if not not_cod:
        print('El código buscado no existe...')
    binario.close()


def crear_matriz(fd):  # Función de creación de la Matriz...
    binario = open(fd, 'rb')
    mc = [[0] * 5 for _ in range(3)]
    t = os.path.getsize(fd)
    while binario.tell() < t:
        r = pickle.load(binario)
        f = r.vehiculo
        c = r.pais_cabina
        mc[f][c] += 1
    binario.close()
    return mc


def mostrar_matriz(fd):  # Función para mostrar la matriz generada...
    mc = crear_matriz(fd)
    print('Resultados...')
    for f in range(3):
        for c in range(5):
            if mc[f][c] != 0:
                print('Tipo de Vehículo', f, ' - País:', c, ' - Cantidad:', mc[f][c])
    print()


def totalizar_matriz(fd):  # Función de acumulación por filas/columnas de la matriz...
    mc = crear_matriz(fd)
    f = 0

    print('Totales por tipo de vehículo')
    for f in range(len(mc)):
        ac = 0
        for c in range(len(mc[f])):
            ac += mc[f][c]
        print("Tipo:", f, " - Cantidad:", ac)
    print()

    print('Totales por países de cabinas')
    for c in range(len(mc[f])):
        ac = 0
        for f in range(len(mc)):
            ac += mc[f][c]
        print('País:', c, ' - Cantidad:', ac)
    print()


def distancia_promedio(fd):  # Funcion de calculo de promedio...
    binario = open(fd, 'rb')
    tam = os.path.getsize(fd)
    ac = cc = 0

    while binario.tell() < tam:
        reg = pickle.load(binario)
        ac += reg.km_recorridos
        cc += 1

    binario.close()
    return ac // cc


def shell_sort(vec):  # Función de Ordenamiento Shell_Sort...
    n = len(vec)
    h = 1
    while h <= n // 9:
        h = 3 * h + 1
    while h > 0:
        for j in range(h, n):
            y = vec[j].km_recorridos
            k = j - h
            while k >= 0 and y < vec[k].km_recorridos:
                vec[k + h].km_recorridos = vec[k].km_recorridos
                k -= h  # Corrected from k = h
            vec[k + h].km_recorridos = y
        h //= 3


def generar_arreglo(fd, vec, prom):  # Función de generación del arreglo (Punto 8)
    binario = open(fd, 'rb')
    tam = os.path.getsize(fd)

    while binario.tell() < tam:
        reg = pickle.load(binario)
        if reg.km_recorridos > prom:
            vec.append(reg)

    binario.close()


def principal():  # Función principal...
    # Crear arreglo de registros
    fd = 'peajes-bin.dat'
    # Menu de opciones
    op = -1

    while op != 0:
        mostrar_menu()
        op = int(input('Ingrese la opción que desee ejecutar...(con cero termina): '))

        # Evaluar opciones
        if op == 1:  # Opción para crear el archivo binario...
            print('¡¡ADVERTENCIA!!')
            print('Si presiona cualquier tecla, se borrara el archivo generado anteriormente...')
            c = input('Si presiona 0 cancela la operación: ')
            if c != '0':
                generar_archivo_bin(fd)
                print('Archivo binario generado exitosamente...')

        elif op == 2:  # Opción para cargar un ticket manualmente...
            cargar_registro(fd)

        elif op == 0:  # Opción para salir del programa...
            print('Gracias por usar nuestro programa!!!')

        elif op < 0 or op > 8:  # Muestra un mensaje de error al introducir una opción incorrecta...
            print('Opción Incorrecta..')

        elif os.path.exists(fd):
            if op == 3:  # Opción para mostrar el vector ordenado por código (de menor a mayor)...
                mostrar_archivo(fd)

            elif op == 4:  # Opción para buscar en el archivo una patente...
                buscar_patente(fd)

            elif op == 5:  # Opción para buscar en el archivo un ticket...
                busqueda_codigo(fd)

            elif op == 6:  # Opción para generar matriz...
                mostrar_matriz(fd)

            elif op == 7:  # Opción para totalizar filas/columnas de la matriz...
                totalizar_matriz(fd)

            elif op == 8:  # Opción para calcular y mostrar promedio de distancia...
                prom = distancia_promedio(fd)
                print(f'La distancia promedio es ---> {prom}')
                vec = []
                generar_arreglo(fd, vec, prom)
                shell_sort(vec)
                for linea in vec:
                    print(linea)
        else:
            print('ERROR: Primero debe generar un archivo para continuar...')


if __name__ == '__main__':
    principal()
