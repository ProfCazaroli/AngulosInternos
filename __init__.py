# -*- coding: utf-8 -*-
"""
/***************************************************************************
 divideLoteBuffer
                                 A QGIS plugin
 Divide Lote com Buffer
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-06-20
        copyright            : (C) 2024 by profCazaroli
        email                : profCazaroli@geoone.com.br
 ***************************************************************************/
"""

__author__ = 'profCazaroli'
__date__ = '2024-06-20'
__copyright__ = '(C) 2024 by profCazaroli'

def classFactory(iface):  # pylint: disable=invalid-name
    from .AngulosInternos import AngulosInternosPlugin
    return AngulosInternosPlugin()
