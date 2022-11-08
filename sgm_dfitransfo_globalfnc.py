# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        Global Functions
    * Description:   Global functions
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


from qgis.core import QgsMessageLog
from qgis.PyQt.QtWidgets import (QMessageBox, QFileDialog, QLineEdit, QTextEdit, 
                                    QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit)

import os

from .sgm_dfitransfo_globalvars import * 

# Open a dialog to ask for the choice of a file
# dft_filename = the name of a file to propose in the dlg
# msgs = list of text messages for the dialogbox
# ext = extension filter. For example: "json (*.json)" or "images (*.png *.jpg *.bmp)"
# msgs = [dlg_title, wrong_file_dlg_title, wrong_file_dlg_txt]
# Return the file selected and the default dir or None if no selection
def ask_file_from_prjpath(iface, project, dft_filename, ext, msgs):
    dft_rep = os.path.expanduser("~")
    dft_file = dft_rep
    if project.absoluteFilePath() != '':
        dft_rep = project.absolutePath()
        dft_file = os.path.join(dft_rep, dft_filename)
    file_sel = QFileDialog.getOpenFileName (
            None,
            msgs[0],
            dft_file,
            ext
            )[0]
    if file_sel:
        return file_sel, dft_rep
    else:
        QMessageBox.information(iface.mainWindow(), msgs[1], msgs[2])
        return None

# Find the value of any kind of object of a dlg
def get_dlg_objval(dlg_obj):        
    if isinstance(dlg_obj, QLineEdit):
        return dlg_obj.text()
    elif isinstance(dlg_obj, QTextEdit):
        return dlg_obj.toPlainText()
    elif isinstance(dlg_obj, QComboBox):
        return dlg_obj.currentText()
    elif isinstance(dlg_obj, QSpinBox):
        return dlg_obj.value()
    elif isinstance(dlg_obj, QDoubleSpinBox):
        return dlg_obj.value()
    elif isinstance(dlg_obj, QDateEdit):
        return dlg_obj.date()
        
# Set the value (or the current id for combobox) of any kind object of a dlg
def set_dlg_objval(dlg_obj, nw_val): 
    if isinstance(dlg_obj, QLineEdit):
        return dlg_obj.setText(nw_val)
    elif isinstance(dlg_obj, QTextEdit):
        return dlg_obj.setHtml(nw_val)
    elif isinstance(dlg_obj, QComboBox):
        return dlg_obj.setCurrentIndex(nw_val)
    elif isinstance(dlg_obj, QSpinBox):
        return dlg_obj.setValue(nw_val)
    elif isinstance(dlg_obj, QDoubleSpinBox):
        return dlg_obj.setValue(nw_val)
    elif isinstance(dlg_obj, QDateEdit):
        return dlg_obj.setDate()

# Show the debug messages
# Usage: 
# debug_msg('DEBUG', "var1: %s, - var2: %s" , (str(var1), str(var2)))
def debug_msg(debug_on_off, msg_str, msg_list_var):
    if debug_on_off == 'DEBUG':
        msg = msg_str % msg_list_var
        QgsMessageLog.logMessage(msg, 'Sgm debug')

