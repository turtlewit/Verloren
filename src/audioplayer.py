"""Audio Player

This module declares the AudioPlayer class, which inherits the GameComponent class in AdventureEngine.components.gamecomponent. 
"""

from AdventureEngine.components.gamecomponent import GameComponent

import os


class AudioPlayer(GameComponent):
	"""Declares the AudioPlayer class, which inherits the GameComponent class in AdventureEngine.components.gamecomponent."""

	def __init__(self):
		"""Initializes the AudioPlayer class and creates it's member variables."""
		self.m_name = "AudioPlayer"
		GameComponent.__init__(self)
		# self.play = True
		self.player = None
		self.audio = None
		self.loop = None

	def Update(self):
		"""Update method

		Overrides GameComponent.Update(). 
		Handles the playing of music for different worlds, or for different states. 
		"""

		# Sets the audio and player member variables. 
		if self.audio == None:
			self.audio = self.m_parent.m_engine.m_audio
		if self.player == None:
			for component in self.m_parent.m_components:
				if component.m_name == "player":
					self.player = component

		# If the 'player' member variable isn't 'None', play music based on the game state, player's world, etc. 
		#if self.play == True and self.player != None:
		if self.player:
			worldDifference = self.player.worldDifference
			
			if self.player.m_parent.m_engine.m_game.m_root.stctrl.GetState().m_name == ("explore" or "map"):
				if self.player.world.m_music:
					if self.audio.m_currentSong != self.player.world.m_name:
						self.audio.LoadSong(self.player.world.m_name, os.path.join('data', 'audio', self.player.world.m_music))
						self.audio.PlaySong(self.player.world.m_name)
						self.loop = self.player.world.m_name
				else:
					self.audio.StopMusic()
					self.loop = None

			if self.player.m_parent.m_engine.m_game.m_root.stctrl.GetState().m_name == "default" and self.audio.m_currentSong != "menu":
				self.audio.LoadSong("menu", os.path.join('data', 'audio', 'menu.wav'))
				self.audio.PlaySong("menu")
				self.loop = "menu"

		if self.loop:
			if not self.audio.m_currentSongPlayObject.is_playing():
				self.audio.PlaySong(self.loop)


