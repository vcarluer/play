import mkvparser

sourceDir = '/mnt/.sb/temp'
logFileName = 'mkvKeep.log'

mkvparser.convert_all(sourceDir, logFileName)
