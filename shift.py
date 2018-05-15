import re
import logging
import datetime


logLevel = logging.DEBUG
logging.basicConfig(level=logLevel)
fileToShift = '/mnt/ms/movies/Ready Player One (2018)/Ready.Player.One.2018.720p.KORSUB.HDRip.x264.AAC2.0-STUTTERSHIT.en.vtt'
fileout = '/mnt/ms/movies/Ready Player One (2018)/Ready.Player.One.2018.720p.KORSUB.HDRip.x264.AAC2.0-STUTTERSHIT.en.vtt.shift'
shiftSec = 4
regex = re.compile(r'((?P<hours>\d+?)\:)?((?P<minutes>\d+?)\:)?((?P<seconds>\d+?)\.)?((?P<milliseconds>\d+))?.*$')

def shift(source, target, seconds):
    # function to check if the line can be deleted
    def parseLine(line):
        if ' --> ' not in line:
            return line
        else:
            lineSplit = line.split(' --> ')
            dateStart = lineSplit[0]
            dateEnd = lineSplit[1]
            sec = datetime.timedelta(seconds=seconds)
            deltaStart = getTimedelta(dateStart)
            newStart = addShift(deltaStart, sec)
            deltaEnd = getTimedelta(dateEnd)
            newEnd = addShift(deltaEnd, sec)
            return ftd(newStart) + ' --> ' + ftd(newEnd) + '\n'

    def ftd(timeDelta):
        newTD = str(timeDelta)[0:-3]
        tds = newTD.split(':')
        tds[0] = "{0:0>2}".format(tds[0])
        newTD = ':'.join(tds)
        return newTD

    def addShift(base, add):
        return base + add

    def getTimedelta(strDelta):
        logging.debug('strDelta: ' + strDelta)
        parts = regex.match(strDelta)
        logging.debug('part 1 : ' + str(parts))
        parts = parts.groupdict()
        logging.debug('part 2 : ' + str(parts))
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        return datetime.timedelta(**time_params)

    # generates the new lines
    with open(source, 'r') as file:
        file_out = []
        for line in file:
            newLine = parseLine(line)
            file_out.append(newLine)

    # writes the new the output to file
    with open(target, 'w') as file:
        logging.debug('writing new file')
        file.write(''.join(file_out))

shift(fileToShift, fileout, shiftSec)
