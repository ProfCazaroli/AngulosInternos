# -*- coding: utf-8 -*-
__author__ = 'profCazaroli'
__date__ = '2024-06-20'
__copyright__ = '(C) 2024 by profCazaroli'
__revision__ = '$Format:%H$'

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterNumber
from qgis.PyQt.QtCore import QCoreApplication
import processing

class AngulosInternosAlgorithm(QgsProcessingAlgorithm):
    def initAlgorithm(self, config=None):
        self.addParameter(
        QgsProcessingParameterNumber('distancia', 
                                     'Distância',
                                     type=QgsProcessingParameterNumber.Double, 
                                     minValue=0.1, 
                                     defaultValue=3))
        
        self.addParameter(
        QgsProcessingParameterVectorLayer('poligono', 'Polígono', 
                                          types=[QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterVectorLayer('vertices', 'Vértices', types=[QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterFeatureSink('angInt', 'Ângulos Internos'))

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        outputs = {}

        parameters['angInt'].destinationName = 'Ângulos Internos'

        # Buffer nos Vértices
        alg_params = {
            'INPUT': parameters['vertices'],
            'DISSOLVE': False,
            'DISTANCE': parameters['distancia'],
            'END_CAP_STYLE': 0,  # Arredondado
            'JOIN_STYLE': 0,     # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 9,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback,
                                           is_child_algorithm=True)
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Polígonos para linhas (a linha que define o ângulo)
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['linhaAng'] = processing.run('native:polygonstolines', alg_params, context=context,
                                                       feedback=feedback, is_child_algorithm=True)
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Interseção - Ângulo Interno
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['linhaAng']['OUTPUT'],
            'INPUT_FIELDS': [''],
            'OVERLAY': parameters['poligono'],
            'OVERLAY_FIELDS': [''],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['angInt']
        }

        outputs['OUTPUT'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback,
                                             is_child_algorithm=True)
        
        self.SAIDA = outputs['OUTPUT']
        
        return {'angInt': self.SAIDA}
    
    def name(self):
        return 'Ângulos Internos'

    def displayName(self):
        return 'Ângulos Internos'

    def group(self):
        return 'Ângulos'

    def groupId(self):
        return 'Ângulos'
        
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AngulosInternosAlgorithm()
    
