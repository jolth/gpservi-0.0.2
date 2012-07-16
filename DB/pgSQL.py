# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro

"""
import psycopg2 as pgsql
import sys


def connection(args=None): 
    """ 
        args, puede ser una cadena con todos los datos para conectarse a la base de datos o 
        simplemente enviarse sin datos, para lo cual tomara la configuración por defecto 
        almacenada en el fichero de configuración "config.cfg" (en la sección [DATABASE]).
        así:

        
        Usage:
        >>> from DB.pgSQL import connection

        >>> connection("dbname='test010' user='postgres' host='localhost' password='qwerty'") # Con argumentos
        >>> connection() # Sin argumento
        <connection object at 0xb715a72c; dsn: 'dbname='test009' user='postgres' host='localhost' password=xxxxxxxx', closed: 0>
        >>> conn = connection()
        >>> cursor = conn.cursor()
        >>> cursor.execute("select * from gps")
        >>> print cursor.fetchall()
        [(11, 'GPS0003', 2, False, datetime.datetime(2012, 7, 13, 8, 11, 31, 945952, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=1140, name=None))), ...]
        >>>

    """
    if args is None:
        from Load.loadconfig import load

        args = {}
        
        args['dbname'] = load('DATABASE', 'DBNAME')
        args['user'] = load('DATABASE', 'USER')
        args['host'] = load('DATABASE', 'HOST')
        args['password'] = load('DATABASE', 'PASSWORD')

        args = " ".join(["%s=\'%s\'" % (k, v) for k, v in args.items()])

    # Conexión a la base de datos: 
    try:
        conn = pgsql.connect(args)
    except pgsql.OperationalError, e:
        print >> sys.stderr.write, "\nNo se pudo poner en marcha la base de datos.\n"
        print >> sys.stderr.write, e
        print >> sys.stdout.write, 'Error: Revisar el archivo de error.log'
        sys.exit(1)

    # Retornamos la conexión
    return conn

        
