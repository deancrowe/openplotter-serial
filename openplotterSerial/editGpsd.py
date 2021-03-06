#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-serial>
#                     
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

import sys, subprocess

if sys.argv[1]=='add':
	device = sys.argv[2]
	with open('/etc/default/gpsd', 'r') as f:
		for line in f:
			if 'DEVICES=' in line:
				line = line.replace('\n', '')
				line = line.strip()
				items = line.split('=')
				item1 = items[1].replace('"', '')
				item1 = item1.strip()
				devList = item1.split(' ')
				devList.append(device)
				final0 = ' '.join(devList)
				final0 = final0.strip()
				final = '"'+final0+'"'
	fo = open('/etc/default/gpsd', "w")
	fo.write( 'START_DAEMON="true"\nUSBAUTO="false"\nDEVICES='+final+'\nGPSD_OPTIONS="-n -b"')
	fo.close()
	subprocess.call(['service', 'gpsd', 'restart'])

if sys.argv[1]=='remove':
	device = sys.argv[2]
	new = []
	with open('/etc/default/gpsd', 'r') as f:
		for line in f:
			if 'DEVICES=' in line:
				line = line.replace('\n', '')
				line = line.strip()
				items = line.split('=')
				item1 = items[1].replace('"', '')
				item1 = item1.strip()
				devList = item1.split(' ')
				for i in devList:
					if i != device: new.append(i)
	if not new:
		fo = open('/etc/default/gpsd', "w")
		fo.write( 'START_DAEMON="false"\nUSBAUTO="false"\nDEVICES=""\nGPSD_OPTIONS="-n -b"')
		fo.close()
	else:
		final0 = ' '.join(new)
		final0 = final0.strip()
		final = '"'+final0+'"'
		fo = open('/etc/default/gpsd', "w")
		fo.write( 'START_DAEMON="true"\nUSBAUTO="false"\nDEVICES='+final+'\nGPSD_OPTIONS="-n -b"')
		fo.close()
	subprocess.call(['service', 'gpsd', 'restart'])

