# -*- coding: UTF-8 -*-
"""
    Módulo que permite gestionar los distintos eventos enviados por
    los dispositivos GPS.

    Autor   : Jorge A. Toro
    email   : jolthgs@gmail.com, jolth@esdebian.org
    date    : vie jul 20 07:49:38 COT 2012
    version : 0.1.9

    Usage:

"""
import sys
import traceback

def insertEvent(evento): 
    def insert(args):
        """ 
            Llama la función PL/SQL
        """
        #print locals()
        print "DATA:", args
        print "INSERT:", evento.__name__ 
        return evento(args)
        #return evento.__name__
    return insert


def insertReport(): pass

        
# Funciones Manejadoras de Eventos:
@insertEvent
def event1(data=None): 
    print "panic"
    return "Panic" # Retornamos una cadena con el tipo de Evento 
@insertEvent
def event2(data=None): return "speeding"
def event5(data=None): return "Report" # SQL
@insertEvent
def event6(data=None): return "start"
@insertEvent
def event7(data=None): return "shutdow"
@insertEvent
def event8(data=None): return "bateri on"
@insertEvent
def event9(data=None): return "bateri off"

                       
def parseEvent(data=None): #getEvent() 
    """
        Analiza y determina que hacer con cada uno de los eventos. 
        
        Llama a getTypeEvent
    """
    # Si es llamable, se llama a la función manajadora. si no, se retorna None 
    # y no se ejecuta ninguna secuancia para el dato ingresado.
    #return callable(getTypeEvent(data)) and getTypeEvent(data)(data) # Retorna False 
    return (callable(getTypeEvent(data)) or None) and getTypeEvent(data)(data) # Retorna None.


def getTypeEvent(data=None, module=sys.modules[parseEvent.__module__]):
    """ 
        >>> import captureEvent
        >>> import datetime
        >>>data = {'codEvent': '05', 'weeks': '1693', 'dayWeek': '4', 'ageData': '2', \
        'position': '(4.81534,-75.69489)', 'type': 'R', 'address': '127.0.0.1,50637', \ 
        'geocoding': u'RUEDA MILLONARIA PEREIRA, Calle 18 # CARRERA 7, Pereira, Colombia', \
        'data': '>REV051693476454+0481534-0756948900102632;ID=ANT051<', 'course': '026', \
        'gpsSource': '3', 'time': '76454', 'lat': '4.81534', 'typeEvent': 'EV', 'lng': '-75.69489', \
        'datetime': datetime.datetime(2012, 7, 20, 8, 50, 9, 154217), 'speed': 1.0, 'id': 'ANT051', 'altura': None}
        >>> captureEvent.getTypeEvent(data)
        <function event5 at 0xb7395844>
        >>> 
    """
    try:
        # Nombre de la Función Manejadora:
        event = "event%s" % int(data['codEvent'])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print '-'*60
        print "*** print exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        print '-'*60
        return # None

    # Retorna la función Manejadora:
    return hasattr(module, event) and getattr(module, event) or None 


