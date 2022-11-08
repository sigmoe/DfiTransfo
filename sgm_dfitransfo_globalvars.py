# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        Global Vars
    * Description:   Global variables
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


from qgis.PyQt.QtCore import QVariant


# Default file and layer names
dfi_dftname = "dfi.txt"
gpkg_name = "dfi.gpkg"
gpkg_lyr = "filiations parcelles"

# Interface and dialog messages
mnu_title_txt = "Transformation DFI"
mnu_fnc_txt = "Transformation Documents de filiation informatisés (DFI) des parcelles"
dfi_file_msgs = [   "Choix du fichier DFI à transformer",
                    "Transformation DFI annulée", 
                    "Vous n'avez pas choisi de fichier à transformer ! <br/>Transformation DFI annulée !"]
dfitr_end_msgs = [   "Création nouvelle couche filiations parcelles",
                    "Traitement terminé !"]
pgbar_msg_txt = [   "Transformation DFI en cours ...",
                    "Transformation DFI terminée !"]

# Params
dfi_atts = ["département", "code commune", "préfixe section", "id dfi", "nature dfi", "date validation", "géomètre", "numéro lot", "parcelles anciennes", "parcelles nouvelles"]
dfi_atts_qt = [QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.String, QVariant.Date, QVariant.String, QVariant.String, QVariant.String, QVariant.String]

dfi_nat = { "1" : "document d’arpentage", 
            "2" : "croquis de conservation", 
            "4" : "remaniement", 
            "5" : "document d’arpentage numérique", 
            "6" : "lotissement numérique", 
            "7" : "lotissement", 
            "8" : "rénovation"}
