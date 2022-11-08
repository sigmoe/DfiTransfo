# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        Main
    * Description:   Main class
    * Specific lib:  None
    * First release: 2020-09-14
    * Last release:  2022-11-08
    * Copyright:     (C)2022 SIGMOE
    * Email:         em at sigmoe.fr
    * License:       GPL v3
    ***************************************************************************
 
    ***************************************************************************
    * This program is free software: you can redistribute it and/or modify
    * it under the terms of the GNU General Public License as published by
    * the Free Software Foundation, either version 3 of the License, or
    * (at your option) any later version.
    *
    * This program is distributed in the hope that it will be useful,
    * but WITHOUT ANY WARRANTY; without even the implied warranty of
    * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    * GNU General Public License for more details.
    *
    * You should have received a copy of the GNU General Public License
    * along with this program. If not, see <http://www.gnu.org/licenses/>.
    *************************************************************************** 
"""


from qgis.PyQt.QtCore import  QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsExpression
from qgis.utils import iface

import os.path

from .sgm_dfitransfo_globalvars import * 
from .sgm_dfitransfo_expressfunctions import * 
from .sgm_dfitransfo_tr import DfiTransfo
from . import sgm_dfitransfo_rc


class SgmDfiTransfo:
    
    # Initialization
    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.project = QgsProject.instance()
        
        # Initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
    
            
    # Initialisation of the menu and the toolbar
    def initGui(self):
        # Add specific menu to QGIS menu
        self.dfitr_menu = QMenu(QCoreApplication.translate("DfiTr", mnu_title_txt))
        self.iface.mainWindow().menuBar().insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dfitr_menu)
        
        # Add specific toolbar
        self.dfitr_tb = self.iface.addToolBar(mnu_title_txt)
        self.dfitr_tb.setObjectName("DfiTrToolBar")
        
        # Create actions
        self.action_tr = QAction(
            QIcon(r":sgm_dfitr"), mnu_fnc_txt, self.iface.mainWindow())
            
        # Add actions to the toolbar
        self.dfitr_tb.addActions([self.action_tr])
                                 
        # Add actions to the menu
        self.dfitr_menu.addActions([self.action_tr])
        
        # Manage signals
        self.action_tr.triggered.connect(self.dfitr_tr)
        
        # Register functions (for expression)
        QgsExpression.registerFunction(dfi_find_newparc)
        
    # Unload actions
    def unload(self) :
        # Unregister functions (for expression)
        QgsExpression.unregisterFunction('dfi_find_newparc')
        if self.dfitr_menu != None:
            self.iface.mainWindow().menuBar().removeAction(self.dfitr_menu.menuAction())
            self.dfitr_menu.deleteLater()
            self.iface.mainWindow().removeToolBar(self.dfitr_tb)
        else:
            self.iface.removePluginMenu("&DfiTr", self.dfitr_menu.menuAction())
            self.dfitr_menu.deleteLater()
        
    # First main function
    def dfitr_tr(self) :
        '''
            Transform the DFI file
        '''
        self.dfitr = DfiTransfo(self.iface, self.canvas, self.project, self.plugin_dir)
        self.dfitr.launch()
        

        
        
            