
import Zones.persistentLanding as pl
import Zones.formattedZone as fz
import Zones.trustedZone as tz
import Zones.exploitationZone as ez
import Zones.featGenModelZone as fgmz
import warnings

def fxn():
	warnings.warn("deprecated", DeprecationWarning)

def printLine():
	print('='*70)

def main():

	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		fxn()
		printLine()
		print('DATA MANAGEMENT')
		printLine()
		print('STARTING LOADING')
		print()
		printLine()
		print('1. Landing Zone:')
		printLine()
		print('Persistent Landing Zone:')
		printLine()
		print('Copying files from Temporal Landing to Persistent Landing')
		pl.persistentLanding()
		print('Files copied')
		print()
		printLine()
		print('2. Formatted Zone:')
		printLine()
		print('Saving files from Persistent Landing in the Formatted Zone DB')
		print('(Tablename) - (num. of rows)')
		fz.formattedZone()
		print('Files saved as tables')
		print()
		printLine()
		print('3. Trusted Zone:')
		printLine()
		print('Moving data from the Formatted Zone DB to the Trusted Zone DB')
		tz.trustedZone()
		print()
		printLine()
		print('4. Exploitation Zone:')
		print('Generating views in the Exploitation Zone DB')
		ez.exploitationZone()
		printLine()
		print('LOADING FINISHED')
		printLine()
		print('DATA ANALYSIS')
		printLine()
		fgmz.featGenModelZone()


if __name__ == "__main__":
	main()