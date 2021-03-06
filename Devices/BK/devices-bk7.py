# -*- coding: utf-8 -*-
#

import sys
import StringIO
#from UserDict import UserDict





# Clase que actua como un diccionario
class Devices(dict):
    """ Store """
    def __init__(self, data=None, deviceId=None):
        self['id'] = deviceId
        self.dataFile = None
        if data is not None: self.__parse(data) 
        else: print("No existe información para procesar...") #pass #continue()


    def __parse(self, data):
        self.clear()
        try:
            self.dataFile = StringIO.StringIO(data)

            #
            for tag, (position, bit, seek, parseFunc) in self.tagDataANT.items():
                self[tag] = parseFunc(position, bit, seek)

        except: sys.stderr.write('Error Inesperado:', sys.exc_info())
        finally: self.dataFile.close()

                
    def tagData(self, position, bit, seek=0):
        """
            Toma un punto de partida (position), cantidad de bit y un punto de 
            referencia para leer los bit(según el método seek() de los fichero).
            Además dataFile el cual es objeto StringIO.
        """
        try:
            self.dataFile.seek(position, seek)
            tagdata =  self.dataFile.read(bit)
        except: sys.stderr.write("Error al obtener el Tag Data")
        return tagdata 
        

    def deviceANT(self):
        """
            Dispositivo Antares
        """
        tagDataANT = {   # (position, bit, seek, function)
                         "id" : ( -7, 6, 2, tagData)
                     }
            
    def deviceSKP(self):
        """
            Dispositivo SkyPatrol
        """
        pass
