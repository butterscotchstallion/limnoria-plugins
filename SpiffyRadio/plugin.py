###
# Copyright (c) 2015, PrgmrBill
# Based on work by Copyright (c) 2010, melodeath
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import requests
import json
import supybot.schedule as schedule

try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('SpiffyRadio')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x

class SpiffyRadio(callbacks.Plugin):
	"""Radio information for Icecast 2 streams"""
	threaded = True
	auto_announce_interval = None
	last_track = None
	track_has_changed = False

	def __init__(self, irc):
		self.__parent = super(SpiffyRadio, self)
		self.__parent.__init__(irc)
		self.irc = irc

		if self.registryValue("autoAnnounceNewTracks"):
			self.set_auto_announce_interval()
		else:
			self.remove_announce_interval()

	def set_auto_announce_interval(self):
		interval = self.registryValue("pollingIntervalInSeconds")

		self.remove_announce_interval()

		if not self.auto_announce_interval:
			self.auto_announce_interval = schedule.addPeriodicEvent(self.announce_to_channels, 
																	interval,
																	"SpiffyRadioAutoAnnounce")

	def remove_announce_interval(self):
		try:
			schedule.removeEvent("SpiffyRadioAutoAnnounce")
			self.auto_announce_interval = None
		except:
			pass

	def doUnload(self):
		self.log.info("SpiffyRadio: unloading!")

		self.remove_announce_interval()

	def announce_to_channels(self):
		channels = list(self.registryValue("autoAnnounceChannels"))

		if self.registryValue("autoAnnounceNewTracks"):
			try:
				if len(channels) > 0:
					message = self.get_now_playing_message()

					if message is not None:
						if self.track_has_changed:
							self.log.info("SpiffyRadio: announcing to channels (%s): %s" % (len(channels), str(channels)))

							for channel in channels:
								self.irc.sendMsg(ircmsgs.privmsg(channel, message))
						else:
							track_info = (self.last_track["artist"], self.last_track["title"])
							self.log.info("SpiffyRadio: track has not changed - still playing \"%s - %s\". Not announcing." % track_info)

			except Exception as e:
				self.log.error("SpiffyRadio: exception %s", str(e))

	def get_current_track_info(self):
		""" Get JSON from Icecast API"""
		api_url = self.registryValue("icecastAPIURL")
		artistChanged = False
		trackChanged = False

		if not api_url:
			irc.error("No API URL set!")
			return

		try:
			request = requests.get(api_url, timeout=10)

			self.log.info("SpiffyRadio: fetching %s" % api_url)

			if request.status_code == requests.codes.ok:
				response = json.loads(request.text)

				if response is not None and "icestats" in response:
					try:
						current_track = response["icestats"]["source"][0]

						"""
						This horrible API returns an object if there is only one track
						and a list if there is more than one. Absolutely disgusting.
						"""
						#if current_track is None:
						#	current_track = response["icestats"]["source"]

						if self.last_track is not None:
							artistChanged = current_track["artist"] != self.last_track["artist"]
							trackChanged = current_track["title"] != self.last_track["title"]
						
						self.track_has_changed = artistChanged and trackChanged
						self.last_track = current_track

						return current_track				
					except KeyError:
						self.log.error("SpiffyRadio: unexpected JSON response from API! This probably means the stream is not currently running.")
				else:
					self.log.error("SpiffyRadio: error parsing JSON %s" % request.text)
			else:
				self.log.error("SpiffyRadio API %s - %s" % (request.status_code, request.text))

		except requests.exceptions.Timeout as e:
			self.log.error("SpiffyRadio Timeout: %s" % (str(e)))
		except requests.exceptions.ConnectionError as e:
			self.log.error("SpiffyRadio ConnectionError: %s" % (str(e)))
		except requests.exceptions.HTTPError as e:
			self.log.error("SpiffyRadio HTTPError: %s" % (str(e)))

	def get_now_playing_template(self, current_track):
		template = self.registryValue("nowPlayingTemplate")

		template = template.replace("$artist", current_track["artist"])
		template = template.replace("$title", current_track["title"])
		template = template.replace("$listeners", str(current_track["listeners"]))
		template = template.replace("$listenurl", current_track["listenurl"])

		return template

	def get_now_playing_message(self):
		current_track = self.get_current_track_info()
		track_info_message = None

		if current_track is not None:
			track_info_message = self.get_now_playing_template(current_track)
			self.last_title = track_info_message

		return track_info_message

	def np(self, irc, msg, args):
		"""Returns the current song and album playing."""
		track_info_message = self.get_now_playing_message()

		if track_info_message is not None:
			irc.reply(track_info_message)
		else:
			irc.reply(self.registryValue("errorMessage"))

Class = SpiffyRadio

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
