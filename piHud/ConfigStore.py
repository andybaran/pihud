
import os
import json
from collections import OrderedDict

import obd
from defaults import defaults, fallback_default


class ConfigStore():
	""" manages the structure of the config file """
	def __init__(self, filename):
		self.filename = filename

		self.port = None
		self.page_adv_pin = 18
		self.debug = False
		self.pages = []

		config = {}

		# read the file
		if os.path.isfile(filename):
			with open(self.filename, 'r') as f:
				config = json.loads(f.read())


		# check for the required root keys
		if not all(k in config for k in ['pages']):
			print "Config is missing the 'pages' array"

		if 'port' in config:
			self.port = config['port']

		if 'page_adv_pin' in config:
			self.page_adv_pin = config['page_adv_pin']

		if 'demo' in config:
			self.demo = config['demo']

		# process each page definition
		for page_json in config['pages']:
			page = PageConfig(self, page_json)
			self.pages.append(page)


	def add_page(self):
		""" constructs a empty page """
		page = PageConfig(self)
		self.pages.append(page)
		return page


	def delete_page(self, page):
		""" deletes a widgetConfig """
		self.pages.remove(page)


	def __config_to_json(self, config):
		""" Constructs a JSON output structure for an existing Config """
		
		config = {}

		# copy all the keys except for the command and class name		
		for key in config.__dict__.keys():
			if key not in ['command', 'class_name']:
				config[key] = config.__dict__[key]

		return OrderedDict([
			('sensor', config.command.name),
			('type', config.class_name),
			('config', config)
		])

	def __json_to_config(self, json_):
		""" Constructs a Config out of a JSON structure """

		if not all((k in json_) for k in ['sensor', 'type', 'config']):
			print "Config is missing required keys"
			return None

		sensor_name = json_['sensor'].upper()
		class_name  = json_['type']

		if sensor_name not in obd.commands:
			print "sensor '%s' is not a valid OBD command" % sensor_name
			return None

		if class_name not in widgets:
			print "widget '%s' is not a valid Widget type" % class_name
			return None

		# Make a default config for this command
		config = Config(obd.commands[sensor_name])

		config.command    = obd.commands[sensor_name]
		config.title      = config.command.name
		config.class_name = class_name

		# Overwrite default values with user values
		for key in config_props:

			# skip keys with special handling
			if key in ['command', 'class_name']:
				continue

			if self.__dict__.has_key(key):
				self.__dict__[key] = config_props[key]



	def save(self):
		""" write the config back to the file """
		
		output_pages = []

		for page in self.pages:
			output_page = []
			for w in page.widget_configs:
				output_page.append(w.to_JSON())
			output_pages.append(output_page)

		output = {
			"port": self.port,
			"page_adv_pin": self.page_adv_pin,
			"demo": self.demo,
			"pages": output_pages,
		}

		with open(self.filename, 'w') as f:
			f.write(json.dumps(output, indent=4))
