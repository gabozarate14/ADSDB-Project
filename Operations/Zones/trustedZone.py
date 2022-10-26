
import Zones.trustedZone_control as tz1
import Zones.trustedZone_load as tz2
import Zones.trustedZone_deduplication as tz3
import Zones.trustedZone_setcorrectformats as tz4
import Zones.trustedZone_outliers as tz5
import Zones.trustedZone_fixsampling as tz6




import warnings

def fxn():
	warnings.warn("deprecated", DeprecationWarning)


def trustedZone():

	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		fxn()

		tz1.trustedZone_control()
		print('3.1 Contol Tables created')
		print('3.2 Data moved to the tables of the Trusted Zone DB')
		tz2.trustedZone_load()
		print('3.3 Deduplication')
		tz3.trustedZone_deduplication()
		print('3.4 Set correct formats')
		tz4.trustedZone_setcorrectformats()
		print('3.5 Outliers treatment')
		tz5.trustedZone_outliers()
		print('3.6 Fixing the sample')
		print('Columns fixed:')
		tz6.trustedZone_fixsampling()
	