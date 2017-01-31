#------------------------------------------------------------------------------#
# Copyright 2016-2017 Golden Sierra Game Development Class                     #
# This file is part of Verloren (GSHS_RPG).                                    #
#                                                                              #
# Verloren (GSHS_RPG) is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# Verloren (GSHS_RPG) is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with Verloren (GSHS_RPG).  If not, see <http://www.gnu.org/licenses/>. #
#------------------------------------------------------------------------------#

from enum import Enum

class Slot(Enum):
    HEAD=0
    SHOULDER_L=1
    SHOULDER_R=2
    TORSO=3
    ARM_L=4
    ARM_R=5
    LEGS=6
    FEET=7

    WEAPON_A=10
    WEAPON_B=11

class Stat(Enum):
    PHYSICAL_INTEGRITY=0
    OLD_WAY=1
    NEW_WAY=2
    ACCURACY=3
    PRECISION=4
    ENGINEERING=5
    ARTIFICING=6
    MENTAL_FORTITUDE=7
    SANITY=8
    REFLEX=9
