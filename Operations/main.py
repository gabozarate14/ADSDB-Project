
import Zones.persistentLanding as pl
import Zones.formattedZone as fz
import Zones.trustedZone as tz
 

def printLine():
	print('='*70)

def main():
	
	printLine()
	print('1. Landing Zone:')
	printLine()
	print('Persistent Landing Zone:')
	printLine()
	print('Copying files from Temporal Landing to Persistent Landing')
	pl.persistentLanding()
	print('Files copied')
	printLine()
	print('2. Formatted Zone:')
	printLine()
	print('Saving files from Persistent Landing in the Formatted Zone DB')
	print('(Tablename) - (num. of rows)')
	fz.formattedZone()
	print('Files saved as tables')
	printLine()
	print('3. Trusted Zone:')
	printLine()
	print('Moving data from the Formatted Zone DB to the Trusted Zone DB')
	tz.trustedZone()


if __name__ == "__main__":
	main()