#!/usr/bin/env python

# parse geojson files to csv

import os
import glob
import json
import pandas as pd

def main():

	frames = []

	# find all matching files
	files = sorted(glob.glob('..'+os.sep+'data'+os.sep+'*.geojson'))

	for f in files:
		with open(f,'r') as fo:
			try:
				data = json.load(fo)
			except:
				print('WARNING: invalid json',f)
				continue
		
		# load json into dataframe	
		df = pd.json_normalize(data.get('features'))

		# split array of geocoords into two columns
		df['longitude'], df['latitude'] = zip(*df['geometry.coordinates'])
		
		# cleanup timestamps
		df['timestamp'] = df['properties.time'].combine_first(df['properties.timeStamp'])
		# "01/25/2020, 21:51:45"
		df['timestamp'] = pd.to_datetime(df.timestamp, format='%m/%d/%Y, %H:%M:%S', errors='ignore')

		# drop columns
		del df['properties.time']
		del df['properties.timeStamp']
		del df['geometry.coordinates']
		del df['geometry.type']
		del df['properties.address']
		del df['properties.zip']
		del df['type']

		# add filename to dataframe
		df['filename'] = f.split(os.sep)[-1]
		
		#print(df.columns)
		#df['timestamp'].to_csv('test.csv')
		#break

		# add this file's frame to the list of frames
		frames.append(df)

	# combine all dataframes into one
	df = pd.concat(frames)

	# rename columns
	df.rename(columns={'properties.range': 'range', \
						'properties.charge': 'charge', \
						'properties.manual': 'manual', \
						'properties.electric': 'electric', \
						'properties.id': 'id', \
						'properties.name': 'name', \
						'properties.provider': 'provider', \
						'properties.size': 'size'}, \
						inplace=True)

	# rearrange columns to make more sense
	#print(df.columns)
	df = df[['filename','provider', 'id', 'timestamp', 'longitude', 'latitude', \
				'name', 'charge', 'electric', 'manual',  'range', 'size']]

	df.to_csv('..'+os.sep+'data'+os.sep+'_all_bikes.csv',sep=',',index=False)

if __name__ == "__main__":
	main()