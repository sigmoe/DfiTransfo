# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        Initialization
    * Description:   Specific plugin only for French people.
    *                This plugin transform a DFI file (txt) in a geopackage 
    *                layer with a better useful structure
    *                DFI = Documents de filiation informatisés des parcelles
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
    
    This script initializes the plugin, making it known to QGIS.
"""


import os
import sys

def classFactory(iface):
    # load SgmDfiTransfo class from file sgm_dfitransfo
    from .sgm_dfitransfo import SgmDfiTransfo
    return SgmDfiTransfo(iface)
