# -*- coding: utf-8 -*-
__author__ = 'profCazaroli'
__date__ = '2024-06-20'
__copyright__ = '(C) 2024 by profCazaroli'
__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .AngulosInternos_algorithm import AngulosInternosAlgorithm
import os

class AngulosInternosProvider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(AngulosInternosAlgorithm())

    def id(self):
        return 'topografia'

    def name(self):
        return self.tr('Topografia')

    def icon(self):
        return QIcon(os.path.dirname(__file__) + '/images/geoincra_logo.png')

    def longName(self):
        return self.name()



