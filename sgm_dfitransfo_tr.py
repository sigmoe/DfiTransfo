# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        DfiTransfo class
    * Description:   Class to do the job for transformation of DFI file
    * Specific lib:  none
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


from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QVariant, QDate, pyqtSignal
from qgis.PyQt.QtGui import QTextCursor
from qgis.PyQt.QtWidgets import QMessageBox, QWidget, qApp
from qgis.core import (QgsWkbTypes, QgsFields, QgsField, QgsCoordinateReferenceSystem,
                        QgsProviderRegistry, QgsFeature)

import os
import csv

from .sgm_dfitransfo_globalvars import *
from .sgm_dfitransfo_globalfnc import *

gui_dlg_dfi, _ = uic.loadUiType(
        os.path.join(os.path.dirname(__file__), r"gui/dlg_dfi.ui"))


class DfiTransfo():
    
    def __init__(self, iface, canvas, project, plugin_dir):

        self.iface = iface
        self.canvas = canvas
        self.project = project
        self.plugin_dir = plugin_dir
        
    def launch(self) :
        # Prepare the parameters window
        self.dfi_params = ParamTr(self.iface, self.project, self.plugin_dir)
        # Capture the dic of parameters when closing the dlg window
        self.dfi_params.send_nw_params.connect(self.ok_param) 
        # Modal window
        self.dfi_params.setWindowModality(Qt.ApplicationModal)
        # Show the parameters window
        self.dfi_params.show()
        
    # Launch the process of creation once the param window is validated
    def ok_param(self, dic_param):
        dfi_file = dic_param["fic"]
        
        feedback = self.dfi_params
        feedback.update_log('Transformation du fichier DFI ...')
        
        gpkg_fname = os.path.join(os.path.dirname(dfi_file), gpkg_name)
        # Create the gpkg layer
        dfi_flds = QgsFields()
        for idx, att in enumerate(dfi_atts):
            dfi_fld = QgsField(att, dfi_atts_qt[idx])
            if dfi_atts_qt[idx] == QVariant.Double:
                dfi_fld.setLength(10)
                dfi_fld.setPrecision(2)
            dfi_flds.append(dfi_fld)
        feedback.update_log('Création fichier GPKG: ' + gpkg_fname)
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        conn = md.createConnection(gpkg_fname, {})
        conn.createVectorTable('', gpkg_lyr, dfi_flds, QgsWkbTypes.NoGeometry, QgsCoordinateReferenceSystem(), True, {})
        dfi_uri = gpkg_fname + '|layername=' + gpkg_lyr
        dfi_lyr = self.iface.addVectorLayer(dfi_uri, gpkg_lyr, 'ogr')

            
        # Count the number of lines
        idx_tot = 0
        with open(dfi_file, "r", newline='') as fic:
            csv_rc = csv.reader(fic, delimiter=";")
            idx_tot = sum(1 for row in csv_rc)
        feedback.update_log(f'Nombre de lignes à traiter: {str(idx_tot)}')
        
        # Open txt file as a CSV file in read mode
        # Case: CSV UTF-8 (delimiter semi-colon)
        with open(dfi_file, "r", newline='') as fic:
            csv_r = csv.reader(fic, delimiter=";")
            # We assume that the lines follow each other for the same lot
            nw_vals = []
            to_create = False
            f_id = 1
            
            # Start editing to add the features
            if not dfi_lyr.isEditable():
                dfi_lyr.startEditing()

            for idx, csv_row in enumerate(csv_r):
                # value1 (fid)
                # First line containing parent parcel
                if idx % 2 == 0:
                    nw_vals.append(f_id)
                    # value2 (dept)
                    if csv_row[0][2] == "0":
                        nw_vals.append(csv_row[0][:2])
                    else:
                        nw_vals.append(csv_row[0])
                    # value3 (code com)
                    nw_vals.append(csv_row[0][:2] + csv_row[1])
                    # value4 to 9
                    for id in range(2, 8):
                        if id == 4:
                            nw_vals.append(dfi_nat[csv_row[id]])
                        elif id == 5:
                            nw_vals.append(QDate.fromString(csv_row[id], "yyyyMMdd"))
                        else:
                            nw_vals.append(csv_row[id])
                    # value10 (parc parent)
                    pfx_parc = csv_row[1] + csv_row[2]
                    parcs_pr = []
                    # Special case of DP
                    if len(csv_row) <= 10:
                        parcs_pr.append("DP")
                    else:
                        for id in range(9, len(csv_row)-1):
                            parc_idu = pfx_parc + csv_row[id].replace(" ","0")
                            parcs_pr.append(parc_idu)
                    nw_vals.append("|".join(parcs_pr))
                # Second line containing child parcels
                else:
                    parcs_ch = []
                    for id in range(9, len(csv_row)-1):
                        parc_idu = pfx_parc + csv_row[id].replace(" ","0")
                        parcs_ch.append(parc_idu)
                    nw_vals.append("|".join(parcs_ch))
                    # Create new object
                    nw_feat = QgsFeature()
                    nw_feat.setFields(dfi_lyr.fields())
                    nw_feat.setAttributes(nw_vals)
                    dfi_lyr.addFeature(nw_feat)
                    nw_vals = []
                    f_id += 1
                if idx % 1000 == 0 or idx == idx_tot-1:
                    feedback.update_log(f'{str(idx)} / {str(idx_tot)} lignes traitées')
            dfi_lyr.commitChanges()
        
        # End message
        QMessageBox.information(
                                feedback, 
                                dfitr_end_msgs[0], 
                                dfitr_end_msgs[1])
                                
                                
                                
        # dfi_gpkg = QgsVectorFileWriter.create(gpkg_fname, dfi_flds, QgsWkbTypes.NoGeometry, QgsProject.instance().crs(), QgsCoordinateTransformContext(), opts, QgsFeatureSink.SinkFlags(), None, gpkg_lyr)
        
        # res_file_err = QgsVectorFileWriter(shp_fname_err, "utf-8", res_flds, QgsWkbTypes.MultiLineString , crs, "csv", layerOptions = ['GEOMETRY=AS_WKT'])
        # if (dfi_gpkg.hasError() != QgsVectorFileWriter.NoError):
        #    debug_msg('DEBUG', "pb création gpkg: %s" , (str(dfi_gpkg.hasError())))
        # del dfi_gpkg


# Manage the window of parameters
class ParamTr(QWidget, gui_dlg_dfi):
    
    send_nw_params = pyqtSignal(dict)
    
    # Initialization
    def __init__(self, iface, project, plugin_dir, parent=None):
        super(ParamTr, self).__init__(parent)
        self.setupUi(self)
        self.project = project
        self.plugin_dir = plugin_dir
        self.iface = iface
        # Initialization of the closing method (False = quit by red cross)
        self.quitValid = False
        self.params = {}
        # Connections
        self.valid_bt.clicked.connect(self.butt_ok)
        self.fic_bt.clicked.connect(self.file_choose)
        
        # Delete Widget on close event
        self.setAttribute(Qt.WA_DeleteOnClose)
        
    # To update message zone
    def update_log(self, msg):
        """
        Update the log
        """
        t = self.msg_ted
        t.ensureCursorVisible()
        prefix = '<span style="font-weight:normal;">'
        suffix = '</span>'
        t.append('%s %s %s' % (prefix, msg, suffix))
        c = t.textCursor()
        c.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        t.setTextCursor(c)
        qApp.processEvents()
    
    # Choose the file to handle
    def file_choose(self):
        # Ask the DFI file
        ext = "TXT (*.txt)"
        ask_file = ask_file_from_prjpath(self.iface, self.project, 
                                                dfi_dftname, ext, dfi_file_msgs)
        if ask_file:
            set_dlg_objval(self.rep_led, ask_file[0])
    
    # Close the window when clicking on the OK button
    def butt_ok(self):
        self.quitValid = True
        self.close()
        
    # Send the parameters when the windows is quit
    def closeEvent(self, event):
        if self.quitValid:
            # Save the different parameters
            self.params["fic"] = get_dlg_objval(self.rep_led)
            # Send the parameters
            self.send_nw_params.emit(self.params)
        else:
            # Hide the window
            self.hide()
