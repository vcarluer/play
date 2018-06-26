import mkvparser

sourceDir = '/mnt/.sb/keep'
logFileName = 'mkvKeep.log'

mkvparser.convert_all(sourceDir, logFileName)
