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
#import datetime

def insertEvent(evento): 
    def insert(data):
        """ 
            Llama la función PL/pgSQL. 
        """
        from DB.pgSQL import PgSQL
            
        #print locals()
        print "DATA:", data
        print "\nINSERT:", evento.__name__ 
        
        ###### SQL:
        # Insert Positions:
        queryPositions = """SELECT fn_save_event_position_gps(%(id)s, %(position)s, %(geocoding)s, 
                         %(speed)s, %(altura)s, %(course)s, %(gpsSource)s, %(address)s, %(datetime)s);"""
        # Insert Eventos:
        queryEventos = """ """

        try:
            db = PgSQL()
            db.cur.execute(queryPositions, data) # INSERT positions_gps
            #result = db.cur.fetchone() # no exite en gps retorna (None,). active=f retorna ('(,)',). Ambos son <type 'tuple'>
            #positions_id, gps_id = db.cur.fetchone() # no exite en gps retorna (None,). active=f retorna ('(,)',). Ambos son <type 'tuple'>
            try:
                # Si no se realiza la inserción no retorna nada.
                positions_id, gps_id = eval(db.cur.fetchone()[0]) # No exite en gps retorna (None,). Si active=f retorna ('(,)',). 
                                                                  # Para lo cual sucede una excepción y se termina la ejecución. 
            except:
                print "Se termina de Gestionar el Evento"
                return # Se termina la ejecución. 
                
            print "RETURN:", positions_id, gps_id  
            #print "LEN(result)", len(result)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print >> sys.stderr, '-'*60
            print >> sys.stderr, "*** print exception <<insertEvent>>:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                               limit=2, file=sys.stderr)
            print >> sys.stderr, '-'*60
            return
        finally:
            print >> sys.stdout, "Actualizando y Cerranda la conexión"
            # Realizamos los cambios en la DB
            db.conn.commit()
            # Cerramos la comunicación
            db.cur.close()
            db.conn.close()

        # No puedo usar db.exe ya que no puedo cerrar la conexion hasta no hacer el insert en la 
        # tabla eventos.
        #db = PgSQL()
        #info = db.exe(query, data)
        #return db.exe(query, data)

        return evento(data) #+ info
        #return evento.__name__
    return insert


def insertReport(): pass

        
# Funciones Manejadoras de Eventos:
@insertEvent
def event1(data=None): 
    #print "panic"
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
        print >> sys.stderr, '-'*60
        print >> sys.stderr, "*** print exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        print >> sys.stderr, '-'*60
        return # None

    # Retorna la función Manejadora:
    return hasattr(module, event) and getattr(module, event) or None 


