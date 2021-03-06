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

from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.components.world import Tile, World
from AdventureEngine.CoreEngine.input import Input
from src.createmap import CreateMap
from src.items.items import Stats
from src.npc import Attack
import os
import curses
import time


class Player(GameComponent):

	def __init__(self):
		GameComponent.__init__(self)
		# Game Properties
		self.m_name = "player"
		self.a_stats = Stats.Generate()
		self.a_health = 20
		self.m_inventory = []
		self.m_equipment = []
		self.m_weapon = (None, None)

		self.attacks = [
			Attack( # Quick Attack
				self,
				"You do a quick attack! Good job!",
				1,
				None,
				2
			),
			Attack( # Normal Attack
				self,
				"You attack normally. Nice.",
				3,
				None,
				5
			)
		]

		# Combat Variables
		self.currentCooldown = 0
		self.time1 = time.time()
		self.defending = False

		# Spacial Properties
		self.currentTile = None
		self.oldTile = Tile()
		self.world = None
		self.oldWorld = World()
		self.worldDifference=None
		self.m_spaceTransform = (0,0)

		# Print Variables
		self.printDescription = True
		self.mapText = None
		self.thingToPrint = []

		# Audio Variables
		self.playMusic = True
		try:
			pygame.mixer.init()
		except:
			self.playMusic = False

		# Technical Variables
		self.stctrl = None
		self.m_initHasRun = False


	def Init(self):
		self.GetCurrentTile()

	def Update(self):
		# Runs Player.Init() Once
		if not self.m_initHasRun:
			self.Init()
			self.m_initHasRun = True

		if self.GetRoot().stctrl.GetState().m_name == "explore":
			self.HandleInput()

			if self.world != self.currentTile.m_parent.m_parent.m_components[0]:
				self.world = self.currentTile.m_parent.m_parent.m_components[0]

			# Determines if the world has changed
			self.worldDifference = None
			try:
				if self.oldWorld != self.world:
					self.worldDifference = True
				else:
					self.worldDifference = False
			except:
				self.worldDifference = True
			if self.worldDifference == True:
				self.oldTile = self.currentTile
				self.oldWorld = self.world
				self.mapText = CreateMap.Create(self.world.m_parent, self)

			self.SendText()
		elif self.GetRoot().stctrl.GetState().m_name == "combat":
			if self.currentCooldown > 0:
				self.currentCooldown -= (time.time() - self.time1)
		self.time1 = time.time()


	def GetSpacePosition(self):
		return self.m_spaceTransform

	def Move(self, direction):
		x = 0
		y = 0
		if direction in ['n', 'north']:
			if self.currentTile.move_north_message:
				self.thingToPrint.insert(0, self.currentTile.move_north_message)
			else:
				y = 1
		elif direction in ['s', 'south']:
			if self.currentTile.move_south_message:
				self.thingToPrint.insert(0, self.currentTile.move_south_message)
			else:
				y = -1
		elif direction in ['e', 'east']:
			if self.currentTile.move_east_message:
				self.thingToPrint.insert(0, self.currentTile.move_east_message)
			else:
				x = 1
		elif direction in ['w', 'west']:
			if self.currentTile.move_west_message:
				self.thingToPrint.insert(0, self.currentTile.move_west_message)
			else:
				x = -1

		self.m_parent.m_transform = (
			self.m_parent.m_transform[0] + x,
			self.m_parent.m_transform[1] + y
		)

		self.GetCurrentTile()
		for child in self.currentTile.m_parent.m_children:
			for component in child.m_components:
				if component.m_name == "Lock":
					if component.IsTileLocked:
						self.m_parent.m_transform = (
							self.m_parent.m_transform[0] - x,
							self.m_parent.m_transform[1] - y
						)
						self.GetRoot().stctrl.GetState("explore").AddText(
						component.m_tileLockedText, 5)
						self.GetCurrentTile()
						break

		self.mapText = CreateMap.Create(
			self.currentTile.m_parent.m_parent,
			self
		)

	def SendText(self):
		'''Sends the current tile description and player.thingToPrint to the explore state'''
		if self.currentTile:
			if self.currentTile.m_description \
				not in self.thingToPrint and self.printDescription == True:
				#self.m_parent.m_renderer.m_mainTextBox = ""
				self.thingToPrint.append(self.currentTile.m_name)
				self.thingToPrint.append(self.currentTile.m_description)

		for textItem in self.thingToPrint:
			self.GetRoot().stctrl.GetState("explore").AddText(textItem)

	def GetCurrentTile(self):
		"""Get Current Tile Method

		This method of the Player class both returns
		and sets the player's current tile.
		"""
		for child1 in self.GetRoot().m_children:
			if child1.m_transform == self.m_spaceTransform \
				and child1.m_components[0].m_type == "world":
				for child2 in child1.m_children:
					if child2.m_transform == self.m_parent.m_transform \
						and child2.m_components[0].m_type == "tile":
						self.currentTile = child2.m_components[0]
						return child2.m_components[0]

	def HandleInput(self):
		if Input().command:
			self.thingToPrint = []
			self.printDescription = True

			if type(Input().command) is not str:
				self.GetRoot().stctrl.GetState().ClearText()
				if Input().command in [
					curses.KEY_UP,
					curses.KEY_DOWN,
					curses.KEY_LEFT,
					curses.KEY_RIGHT
					]:
					directiondict = {
						curses.KEY_UP: 'n',
						curses.KEY_DOWN: 's',
						curses.KEY_LEFT: 'w',
						curses.KEY_RIGHT: 'e'
					}
					self.Move(directiondict[Input().command])

			else:
				if len(Input().command.lower().split()) > 0:

					if Input().command.lower().split()[0] \
						in ['move', 'go', 'walk', 'n', 's', 'e', 'w']:
						self.GetRoot().stctrl.GetState().ClearText()
						try:
							direction = Input().command.lower().split()[1]
						except:
							try:
								direction = Input().command.lower().split()[0]
							except:
								direction = None

						if direction:
							self.Move(direction)

				if Input().command.lower() in ['map']:
					self.GetRoot().stctrl.ChangeState("map")

				elif Input().command.lower() in ['down']:
					self.GetRoot().stctrl.GetState().ClearText()
					self.m_spaceTransform = (
						self.m_spaceTransform[0],
						self.m_spaceTransform[1] + 1
					)
					self.m_parent.m_transform = (0,0)
					self.GetCurrentTile()

				elif Input().command.lower().split()[0] in ['stat']:
					if len(Input.command.split()) > 1:
						newinp = Input().command.lower().split()
						newinp.pop(0)
						newinp = ' '.join(newinp)
						for stat in self.m_stats:
							if newinp == stat.m_name.lower():
								self.GetRoot().stctrl.GetState('explore')\
								.AddText(
									'%s, %s'
									% (
										stat.m_name,
										stat.GetRating()
									),
									5
								)
				elif Input().command.lower().split()[0] in ['attack']:
					if len(Input().command.lower().split()) > 1:
						enemy = None
						for child in self.currentTile.m_parent.m_children:
							for component in child.m_components:
								if component.m_type == "npc":
									if component.m_name.lower() \
										== Input().command.lower().split()[1]:
										enemy = component
						if enemy:
							self.GetRoot().stctrl.GetState("combat")\
								.Initiate(self, enemy)

				elif Input().command.lower() in ['up']:
					self.GetRoot().stctrl.GetState().ClearText()
					self.m_spaceTransform = (
						self.m_spaceTransform[0],
						self.m_spaceTransform[1] - 1
					)
					self.m_parent.m_transform = (0,0)
					self.GetCurrentTile()
				
				elif Input().command.split()[0].lower() in ['equip'] and len(Input.command.split()) > 1:
					found = False
					for item in self.m_equipment:
						if Input().command.split()[1].lower() == item.m_name.lower():
							self.Equip(item)
							found = True
					if not found:
						self.thingToPrint.append("%s isn't in your inventory!" % Input().command.split()[1].capitalize())
							


				elif Input().command.lower() in ['quit', 'exit']:
					self.m_parent.m_engine.m_isRunning = False

	def TakeDamage(self, damage, type):
		self.a_health -= damage
	
	def Equip(self, item):
		if item.m_equipable == True:
			if item.m_type == "weapon":
				if self.m_weapon[0]:
					self.m_weapon = (self.m_weapon[0], item)
				else:
					self.m_weapon = (item, self.m_weapon[1])
			else:
				self.m_equipment[item.m_slot] = item
				
		else:
			self.thingToPrint.append("%s cannot be equipped." % item.m_name.capitalize())
