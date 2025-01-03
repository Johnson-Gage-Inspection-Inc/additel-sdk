# DIReading.py
from typing import List
from datetime import datetime, timedelta
from .coerce import coerce
import logging

class DIReading:
    """
    Represents a single channel's measurement data.

    Structure depends on data types:
        Electrical measurement data:
            Channel name
            Electrical unit Id
            Number of electrical
            measurement data 1
            One electrical measurement data
            electrical measurement data after filter
        Temperature data:
        0 = 'TempValues'
        1 = 'TempUnit'
        2 = 'TempDecimals'
        3 = 'ChannelName'
        4 = 'Values'
        5 = 'ValuesFiltered'
        6 = 'DateTimeTicks'
        7 = 'Unit'
        8 = 'ValueDecimals'
        9 = 'ClassName'
            Channel name
            Electrical unit Id
            Number of electrical measurement data 1 electrical measurement data
            electrical measurement data after filter
            Indication unit Id
            Number of indication data 1
            the indication data
        TC data:
            Channel name
            Electrical unit Id
            Number of electrical measurement data 1 electrical measurement data
            electrical measurement data after filter Indication unit Id
            Number of indication data 1 the indication data
            Cold junction electrical unitId
            Cold junction electrical measurement data number 1
            cold junction electrical test data
            Cold junction temperature unit Id
            Cold junction temperature data number 1
            cold junction temperature data
    """
    function_handlers = {
        'TAU.Module.Channels.DI.DITemperatureReading': {
            "TempValues": List[float],  # 'System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib'
            "TempUnit": int,
            "TempDecimals": int,
            "ChannelName": str,
            "Values": List[float],   # 'System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib'
            "ValuesFiltered": List[float],   # 'System.Collections.Generic.List`1[[System.Double, mscorlib]], mscorlib'
            "DateTimeTicks": List[datetime],   # 'System.Collections.Generic.List`1[[TAU.Module.Channels.DI.TimeTick, TAU.Module.Channels]], mscorlib'
            "Unit": int,
            "ValueDecimals": int,
            "ClassName": str
        },
        'TAU.Module.Channels.DI.DIElectricalReading': {},  # FIXME: Not yet implemented
        'TAU.Module.Channels.DI.DITCReading': {}  # FIXME: Not yet implemented
    }

    def __init__(self, **kwargs):
        try:
            coerce(kwargs)
            self.__dict__.update(kwargs)
        except Exception as e:
            print(f"Error: {e}")

    def to_json(self):
        return self.__dict__

    def to_str(self):
        def rnd(li: list, n: int = None) -> List[float]:
            if not n:
                n = self.TempDecimals
            return [f"{round(float(x), n):.{n}f}" for x in li]
        DateTimeTicks = [self.datetimeToTicks(x) for x in self.DateTimeTicks]
        Values = rnd(self.Values)
        ValuesFiltered = rnd(self.ValuesFiltered)
        TempValues = rnd(self.TempValues, 4)
        output = ''
        n = len(self.Values)
        for i in range(n):
            output += f'{self.ChannelName},{self.Unit},1,{DateTimeTicks[i]},{Values[i]},{ValuesFiltered[i]},{self.TempUnit},1,{TempValues[i]};'
        return f'"{output}"'

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

    @classmethod
    def from_json(self, dict: dict):
        return DIReading(**dict)

    def keys(self):
        return self.__dict__.keys()

    # DateTimeTicks = [self.ticksToDatetime(int(first[3]))]
    # Values = [float(first[4])]
    # ValuesFiltered = [float(first[5])]
    # TempValues=[float(first[8])]
    @classmethod
    def from_str(self, input: str):
        strings = input[1:-1].split(';')[0:-1]
        first = strings[0].split(',')

        # Static variables:
        ChannelName = first[0]
        Unit = first[1]
        # ?=first[2],  # FIXME: Figure out what this is
        TempUnit = first[6]
        # ?=first[7],  # FIXME: Figure out what this is
        TempDecimals=len(str(first[4]).split('.')[1])

        # if there is only one string... (This part is actually redundant, but it's here for clarity)
        if len(strings) == 1:
            return DIReading(ChannelName=ChannelName,
                             Unit=Unit,
                             # ?=first[2],  # FIXME: Figure out what this is
                             DateTimeTicks=[self.ticksToDatetime(int(first[3]))],
                             Values=[float(first[4])],
                             ValuesFiltered=[float(first[5])],
                             TempUnit=TempUnit,
                             # ?=first[7],  # FIXME: Figure out what this is
                             TempValues=[float(first[8])],
                             TempDecimals=TempDecimals
                             )
        
        # otherwise, if there are multiple strings...
        logging.debug(f"{len(strings)} strings were produced by DIReading.from_str")

        def packDicts(strings):
            dictionaries = []
            for string in strings:
                array = string.split(',')
                keys = ['ChannelName', 'Unit', '?', 'DateTimeTicks', 'Values', 'ValuesFiltered', 'TempUnit', '?', 'TempValues']  # FIXME: Figure out what the other keys are
                dictionary = dict(zip(keys, array))
                dictionary['TempDecimals'] = len(str(array[4]).split('.')[1])
                dictionaries.append(dictionary)
            return dictionaries
        def validate(d):
            for i in range(len(d) - 1):
                assert d[i]['ChannelName'] == d[i + 1]['ChannelName'],  f"Channel names do not match: {d[i]['ChannelName']} != {d[i + 1]['ChannelName']}"
                assert d[i]['Unit'] == d[i + 1]['Unit'],                f"Units do not match: {d[i]['Unit']} != {d[i + 1]['Unit']}"
                assert d[i]['TempUnit'] == d[i + 1]['TempUnit'],        f"Temperature units do not match: {d[i]['TempUnit']} != {d[i + 1]['TempUnit']}"
                assert d[i]['TempDecimals'] == d[i + 1]['TempDecimals'],f"Temperature decimals do not match: {d[i]['TempDecimals']} != {d[i + 1]['TempDecimals']}"

        dictionaries = packDicts(strings)
        validate(dictionaries)

        DateTimeTicks = [self.ticksToDatetime(d['DateTimeTicks']) for d in dictionaries]
        Values = [float(d['Values']) for d in dictionaries]
        ValuesFiltered = [float(d['ValuesFiltered']) for d in dictionaries]
        TempValues = [float(d['TempValues']) for d in dictionaries]
        assert len(Values) == len(ValuesFiltered) == len(TempValues) == len(DateTimeTicks), f"Lengths of data do not match for channel {ChannelName}"
        dictionary = {
            'ChannelName': ChannelName,
            'Unit': Unit,
            'DateTimeTicks': DateTimeTicks,
            'Values': Values,
            'ValuesFiltered': ValuesFiltered,
            'TempUnit': TempUnit,
            'TempDecimals': TempDecimals,
            'TempValues': TempValues
        }
        newObject = DIReading(**dictionary)
        assert input == newObject.to_str(), f"Expected {input}, got {newObject.to_str()}"
        return newObject




    @staticmethod
    def ticksToDatetime(ticks: int) -> datetime:
        return datetime(1, 1, 1) + timedelta(seconds=int(ticks) / 10_000_000)

    @staticmethod
    def datetimeToTicks(dt: datetime) -> int:
        return int((dt - datetime(1, 1, 1)) / timedelta(seconds=1) * 10_000) * 1_000
