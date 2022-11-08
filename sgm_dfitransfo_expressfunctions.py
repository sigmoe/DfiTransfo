# -*- coding: utf-8 -*-

"""
    ***************************************************************************
    * Plugin name:   SgmDfiTransfo
    * Plugin type:   QGIS 3 plugin
    * Module:        Dfi Express Functions
    * Description:   Add custom user functions to QGIS Field calculator.
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


# Import the PyQt and QGIS libraries
from qgis.utils import qgsfunction
from qgis.core import QgsProject,  QgsExpression, QgsFeatureRequest

from .sgm_dfitransfo_globalvars import *

def _get_lyr_names():
    return {layer.name():layer for layer in QgsProject.instance().mapLayers().values()}
    
def _get_lyr_ids():
    return {layer.id():layer for layer in QgsProject.instance().mapLayers().values()}

@qgsfunction(-1, "DFI - Filiations parcelles", register=False, usesgeometry=True)
def dfi_find_newparc(values, feature, parent):
    """
        En se basant sur la couche dfi_filiations_parcelles (couche créée grâce à la fonction 'Transfo DFI'), retrouve le(s) nouveau(x) numéro(s) de parcelle(s) à partir de l'ancien numéro de parcelle spécifié dans le champ num_ancien.
        <h4>Syntaxe</h4>
        <div class="syntax"><code>
        <span class="functionname">dfi_find_newparc(</span>
        <span class="argument">'couche_dfi_id', "champ_numparc_ancien" [,profondeur_modifs=1]</span>
        <span class="functionname">)</span>
        </code></div>
        <h4>Arguments</h4>
        <div class="arguments">
        <table>
        <tr><td class="argument">couche_dfi_id</td><td>identifiant ou nom de la couche contenant les données de filiation, par exemple 'filiations_parcelles_8e569466566'. Cet identifiant se trouve en double-cliquant sur la couche en question dans la sous-liste 'Couches'.</td></tr>
        <tr><td class="argument">champ_numparc_ancien</td><td>nom du champ contenant l'identifiant d'une parcelle à traiter (parcelle ancienne), pour retrouver le numéro de parcelle nouvelle correspondant. Ce champ se trouve en double-cliquant le bon champ dans la sous-liste 'Champs et Valeurs'.</td></tr>
        <tr><td class="argument">profondeur_modifs</td><td>niveau de profondeur des modifications à traiter pour trouver les identifiants des dernières nouvelles parcelles. Par défaut = 1.<br/>Si profondeur_modifs égal 1, les nouvelles parcelles retrounées correspondent à la première modification trouvée à partir de l'ancien numéro.<br/>Si profondeur_modifs égal 2, les nouvelles parcelles issues de la première modification sont recherchées, puis un deuxième passage vérifie si ces nouveaux numéros trouvés ont subi une autre modification et dans ce cas, les derniers numéros de parcelles trouvés après 2 modifications sont retournés.<br/>Etc ...</td></tr>
        </table>
        <i>Le nombre d'objets traités est limité à 1000000 pour éviter un traitement trop long.</i>
        </div>
        <h4>Exemples</h4>
        <!-- Show examples of function.-->
        <div class="examples"><ul>
        <li><code>dfi_find_newparc('dfi_filiations_parcelles_060048e8', "num_ancien")</code> &rarr; <code>En se basant sur la couche dfi_filiations_parcelles, retrouve les nouveaux numéros de parcelle à partir des anciens numéros de parcelles spécifiés dans le champ num_ancien, en s'arrêtant au premier niveau de modifications de parcelles.</code></li>
        <li><code>dfi_find_newparc('dfi_filiations_parcelles_060048e8', "num_ancien", 3)</code> &rarr; <code>En se basant sur la couche dfi_filiations_parcelles, retrouve les nouveaux numéros de parcelle à partir des anciens numéros de parcelles spécifiés dans le champ num_ancien, en recherchant jusqu'au 3ème niveau de modifications de parcelles.</code></li>
        </ul></div>
    """
    lyr_id = values[0]
    oldparc_idu = values[1]
    # Check if the parameter profondeur_modifs exists
    pm = 1
    if len(values) == 3:
        if values[2] > 1:
            pm = int(values[2])
    lyr_ids = _get_lyr_ids()
    lyr_names = _get_lyr_names()
    # Case of layer id
    if lyr_id in lyr_ids:
        lyr = lyr_ids[lyr_id]
    # Case of layer name
    elif lyr_id in lyr_names:
        lyr = lyr_names[lyr_id]
    else:
        parent.setEvalErrorString("Erreur: couche DFI non présente")
        return
    rslt_lst = []
    end_search = False
    nf_parcnums = [oldparc_idu]
    for nb_pass in range(pm):
        if not end_search:
            end_search = True
            nw_parcnums = []
            for nw_parcnum in nf_parcnums:
                nw_parcs = ""
                count = 0
                code_com = nw_parcnum[:3]
                # Limit the process to the dfi lines of the town of the parcel
                exp_s = "right(\"code commune\", 3) = '" + code_com + "'"
                com_exp = QgsExpression(exp_s)
                com_ft = lyr.getFeatures(QgsFeatureRequest(com_exp))
                for feat in com_ft:
                    count += 1
                    if count < 1000000:
                        ft_old_idu = feat[dfi_atts[8]].split("|")
                        if nw_parcnum in ft_old_idu:
                            nw_parcs = feat[dfi_atts[9]]
                            end_search = False
                            break
                    else:
                        parent.setEvalErrorString("Erreur: Trop d'objets à traiter !")
                        return
                if nw_parcs == "":
                    rslt_lst.append('PAS DE CHANGEMENT')
                else:
                    nw_parcnums += nw_parcs.split("|")
                    if nb_pass == pm-1:
                        for p in nw_parcnums:
                            rslt_lst.append(p)
            nf_parcnums = list(nw_parcnums)
    return "|".join(rslt_lst)
        
    

