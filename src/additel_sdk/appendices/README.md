Below is the PDF content converted into Markdown. You can copy this text into your Markdown editor.

---

# Appendix 1: SCPI Unit Id List

### Units

| Unit Id | Unit         |
|---------|--------------|
| 2000    | Text unit    |
| 32767   | Empty unit   |
| 1211    | mA           |
| 1212    | μA           |
| 1209    | A            |
| 1240    | V            |
| 1243    | mV           |
| 1281    | Ω            |
| 1284    | kΩ     |
| 1283    | MΩ     |
| 1000    | K      |
| 1001    | ℃     |
| 1002    | ℉      |
| 1003    | °R     |
| 999     | °Re    |
| 1005    | °      |
| 1342    | %      |
| 1133    | kPa   |
| 1130    | Pa    |
| 1131    | GPa   |
| 1132    | MPa   |
| 1134    | mPa   |
| 1135    | μPa   |
| 1136    | hPa          |
| 1137    | bar          |
| 1138    | mbar         |
| 1139    | torr         |
| 1140    | atm          |
| 1141    | psi          |
| 1142    | psia         |
| 1143    | psig         |
| 1144    | gf/cm2       |
| 1145    | kgf/cm2      |
| 1147    | inH2O@4°C     |
| 1148    | inH2O@68°F    |
| 1150    | mmH2O@4°C     |
| 1151    | mmH2O@20°C    |
| 1153    | ftH2O@4°C     |
| 1154    | ftH2O@68°F    |
| 1156    | inHg@0°C    |
| 1158    | mmHg@0°C    |
| 2001    | mtorr       |
| 2002    | lb/ft2      |
| 2003    | tsi         |
| 2004    | psf         |
| 2005    | inH2O@60°F  |
| 2006    | ftH2O@60°F  |
| 2007    | cmH2O@4°C   |
| 2008    | mH2O@4°C    |
| 2009    | cmHg@0°C    |
| 2010    | mHg@0°C     |
| 2011    | kgf/m2      |

---

# Appendix 2: Default Industrial Sensor

| Sensor Type | Sensor Name (used in command) |
|-------------|-------------------------------|
| R100        | 100Ω                          |
| R400        | 400Ω                          |
| R4k         | 4kΩ                           |
| Pt100-385   | Pt100(385)                    |
| Pt10-385    | Pt10(385)                     |
| Pt50-385    | Pt50(385)                     |
| Pt200-385   | Pt200(385)                    |
| Pt400-385   | Pt400(385)                    |
| Pt1000-385  | Pt1000(385)                   |
| Pt25-385    | Pt25(385)                     |
| Pt100-3916  | Pt100(3916)                   |
| Pt100-3926  | Pt100(3926)                   |
| Pt100-391   | Pt100(391)                    |
| Cu100-428   | Cu100(428)                    |
| Cu50-428    | Cu50(428)                     |
| Cu10-427    | Cu10(427)                     |
| Ni100-617   | Ni100(617)                    |
| Ni100-617   | Ni100(618)                    |
| Ni120-672   | Ni120(672)                    |
| Ni1000      | Ni1000                        |
| TC-S        | S                             |
| TC-R        | R                             |
| TC-B        | B                             |
| TC-K        | K                             |
| TC-N        | N                             |
| TC-E        | E                             |
| TC-J        | J                             |
| TC-T        | T                             |
| TC-C        | C                             |
| TC-D        | D                             |
| TC-G        | G                             |
| TC-L        | L                             |
| TC-U        | U                             |
| TC-LR       | LR                            |
| TC-A        | A                             |
| mV          | mV                            |

---

# Appendix 3: Error Definition

## Command and Parameter Errors

| NO. | Error Code | Error Description          | Explanation                                                                               |
|-----|------------|----------------------------|-------------------------------------------------------------------------------------------|
| 1   | 0          | No error                   | No error,                                                                    |
||||**Command error**|
| 2   | 120        | Commandparameter error     | Command parameter error                                                                   |
| 3   | -108       | Parameter not allowed      | Too many parameters, or no parameters in the command with parameters                      |
| 4   | -109       | Missing parameter          | Missing parameter                                                                         |
| 5   | -110       | Command header error       | The command header is error                                                               |
| 6   | -114       | Header suffix out of range | Command header suffix overrange                                                           |
| 7   | -123       | Numeric overflow           | Digital spillover, the absolute exponential value of a number greater than 43             |
| 8   | -151       | Invalid string data        | Invalid string, such as quotation mark mismatch                                           |
| 9   | -171       | Invalid expression         | Invalid expressions, such as parentheses mismatch                                         |
|            |            |     | **Execution Errors**                                                                                             |
| 10  | -200       | Execution error                | Execution error                                                                                                           |
| 11  | -221       | Settings conflict              | Setting Conflicts                                                                                                         |
| 12  | -222       | Data out of range              | Parameter values exceed the valid range of instructions                                                                   |
| 13  | -223       | Too much data                  | Too much data to process                                                                                                  |
| 14  | -224       | Illegal parameter value        | Illegal parameter values                                                                                                  |
| 15  | -230       | Data corrupt or stale          | The data is invalid, or is reading the data, and no valid data has been obtained.                                          |
| 16  | -240       | Hardware error                 | Hardware failure                                                                                                          |
| 17  | -256       | File name not found            | No filename found                                                                                                         |
| 18  | -282       | Illegal program name           | Illegal procedure name                                                                                                    |
| 19  | 220        | Measure error                  | Measurement error                                                                                                         |
| 20  | 221        | Failed to set measure function | Failure to switch measurement items                                                                                       |
| 21  | 222        | Failed to read measure value   | Failed to read measurements                                                                                               |
| 22  | 223        | *(No description provided)*  |                                                                                                                           |
| 23  | 224        | *(No description provided)*  |                                                                                                                           |
| 24  | 240        | Control error                  | Control error                                                                                                             |
| 25  | 241        | *(No description provided)*  |                                                                                                                           |
| 26  | 242        | *(No description provided)*  |                                                                                                                           |
| 27  | 243        | *(No description provided)*  |                                                                                                                           |
| 28  | 260        | Calibration error              | Calibration error                                                                                                         |
| 29  | 261        | Calibration secured            | The equipment is in calibration protection state and cannot perform calibration.                                        |
| 30  | 262        | Invalid calibration secure code| Invalid Calibration Password                                                                                              |
| 31  | 263        | Missing calibration value      | Occurs when setting the calibration value without setting the calibration point in current/voltage calibration.           |

## Serial and Sensor Errors

| Serial NO. | Error Code |    Error Description              |                                        Explanation                                         |
|:----------:|:----------:|:-------------------------------:|:--------------------------------------------------------------------------------------------:|
| 32         | 264        | Missing calibration data         | Occurs when the calibration point is set continuously without setting the calibration value.   |
| 33         | 265        | Failed to set calibration function | Setting Calibration Item Failed                                                               |
| 34         | 266        | Calibration data is not enough   | Occurs when saving calibration data if the data does not reach three points.                   |
| 35         | 271        | Setion_name_not_found            | No paragraph name found                                                                       |
| 36         | 272        | Key_name_not_found               | No key name found                                                                             |
| 37         | 291        | Update secured                   | The equipment is upgraded and protected and cannot be upgraded.                               |
| 38         | 292        | Invalid update secure code       | Invalid upgrade password                                                                      |
| 39         | 293        | Not found the service pack       | No upgrade package found                                                                      |
| 40         | 294        | The service pack unavailable     | Upgrade package unavailable                                                                   |
| 41         | 295        | App Update not found             | Can't find AppUpdate.exe                                                                      |
|            |            | **Equipment-related Errors**     |                                                                                             |
| 42         | -310       | System error                     | System error                                                                                  |
| 43         | -311       | Memory error                     | Memory error                                                                                  |
| 44         | -350       | Queue overflow                   | Queue overflow                                                                                |
| 45         | -360       | Communication error              | Communication error                                                                           |
| 46         | 301        | Internal module is not connected | Unconnected internal module                                                                   |
| 47         | 302        | External module is not connected | Unconnected External Modules                                                                  |
| 48         | 303        | Supply module is not connected   | Unconnected positive pressure module                                                          |
| 49         | 304        | Vacuum module is not connected   | Unconnected negative pressure module                                                          |
| 50         | 361        | Open WLAN Failed                 | Failed to open WIFI                                                                           |
| 51         | 362        | Set WLAN address mode failed     | Failed to set WIFI address mode                                                               |
| 52         | 363        | Set WLAN address failed          | Failed to set WIFI address                                                                    |
| 53         | 364        | Communication port to WIFI module is not open | Communication port with WIFI module is not open                                         |
| 54         | 365        | WLAN is not connected            | WIFI not connected                                                                            |

---

# Appendix 4: State Report

## 4.1 Status Byte Register

The register of status bytes shows the information of other state registers. Its value is unlocked, so if an event register is cleared (zero cleaning), the corresponding bits in the status byte register are also cleared.

### Table 4-1 Definition of Status Byte Register Places

| Bytes | Decimalism Value | Definition          | Explanation                                                                                                 |
|-------|------------------|---------------------|-------------------------------------------------------------------------------------------------------------|
| 0     | 1                | Unused              | Always 0                                                                                                    |
| 1     | 2                | Unused              | Always 0                                                                                                    |
| 2     | 4                | Error queue error   | Error queue is not empty                                                                                    |
| 3     | 8                | Question data       | One or more bits set indicating question data (the corresponding bits in the enabling register must work)     |
| 4     | 16               | Unused              | Always 0                                                                                                    |
| 5     | 32               | Standard event      | One or more bits set indicating a standard event (the corresponding bits in the enabling register must work)    |
| 6     | 64               | Service request     | One or more bits set (except this bit) corresponding to the service request                                  |
| 7     | 128              | Operation state     | One or more bits set indicating operation state (the corresponding bits in the enabling register must work)     |

## 4.2 Standard Event Register

The standard event register shows the following events: power on, grammatical error of command, command execution error, self-testing or calibration error, or when a *OPC command has been executed.

### Table 4-3 Standard Event Register Bit Definition

| Bits | Decimalism Value | Definition         | Explanation                                                          |
|------|------------------|--------------------|----------------------------------------------------------------------|
| 0    | 1                | Finished operation | Before a *OPC command, all other commands are executed               |
| 1    | 2                | Unused             | Always 0                                                             |
| 2    | 4                | Unused             | Always 0                                                             |
| 3    | 8                | Instrument error   | Error during self-testing, calibration, or due to overloading         |
| 4    | 16               | Execution error    | An execution error occurred                                           |
| 5    | 32               | Commands error     | A grammatical error in commands occurred                              |
| 6    | 64               | Unused             |                                                                      |
| 7    | 128              | Power on           | Power on/off operation occurred                                       |

## 4.3 Question Data Register

The question data register shows testing result information (for example, overload indications).

### Table 4-3 Definition of Question Data Register Place

| Bytes | Decimalism Value | Definition         | Explanation      |
|-------|------------------|--------------------|------------------|
| 0     | 1                | Voltage overload   | Voltage overrange|
| 1     | 2                | Current overload   | Current overrange|
| 2     | 4                | Unused             | Always 0         |
| 3     | 8                | Unused             | Always 0         |
| 4     | 16               | Unused             | Always 0         |
| 5     | 32               | Unused             | Always 0         |
| 6     | 64               | Unused             | Always 0         |
| 7     | 128              | Unused             | Always 0         |
| 8     | 256              | Unused             | Always 0         |
| 9     | 512              | Pressure overload  | Pressure overrange|
| 10    | 1024             | Unused             | Always 0         |
| 11    | 2048             | Unused             | Always 0         |
| 12    | 4096             | Unused             | Always 0         |
| 13    | 8192             | Unused             | Always 0         |
| 14    | 16384            | Unused             | Always 0         |
| 15    | 32768            | Unused             | Always 0         |

## 4.4 Operation Status Register

The operation status register provides information on the normal operation of the device.

### Table 4-4 Operation Status Register Bit Definition

| Bits | Decimalism Value | Definition                                               | Explanation   |
|------|------------------|----------------------------------------------------------|---------------|
| 0    | 1                | Unused                                                   | Always 0      |
| 1    | 2                | Unused                                                   | Always 0      |
| 2    | 4                | Unused                                                   | Always 0      |
| 3    | 8                | Unused                                                   | Always 0      |
| 4    | 16               | Measuring Device is initiating pressure measurement      |               |
| 5    | 32               | Unused                                                   | Always 0      |
| 6    | 64               | Unused                                                   | Always 0      |
| 7    | 128              | Unused                                                   | Always 0      |
| 8    | 256              | Unused                                                   | Always 0      |
| 9    | 512              | Unused                                                   | Always 0      |
| 10   | 1024             | Unused                                                   | Always 0      |
| 11   | 2048             | Unused                                                   | Always 0      |
| 12   | 4096             | Unused                                                   | Always 0      |
| 13   | 8192             | Unused                                                   | Always 0      |
| 14   | 16384            | Unused                                                   | Always 0      |
| 15   | 32768            | Unused                                                   | Always 0      |

---

# Appendix 5: ADT286 Programming Commands Illustration

1. **Read information of front panel and scanners**  
   - **Command format:**  
     ```
     [MEASure:]MODule:INFormation?
     ```  
   - **Example:**  
     ```
     MODule:INFormation?
     ```  
   - **Returned value example:**  
     ```
     0,,0,,,2,;1,6851019T10005,1,TAU-M1 V01.00.00.00,TAU-M1 V01.05,20,
     ```  
   - **Note:** N\*7 values (N may be 1,2,3,4,5). Each message is separated by a semicolon; each parameter is separated by commas.

2. **Read channel configuration of one scanner**  
   - **Command format:**  
     ```
     [Measure:]MODule:CONFig? <moduleIndex>
     ```  
   - **Example:**  
     ```
     MODule:CONFig? 0
     ```  
   - **Returned value example:**  
     ```
     REF1,1,,3,0,0,1,1,4,Pt25(385),,,0,0;REF2,0,,4,0,0,1,1,2,Auto Range,,;
     ```  
   - **Notes:**  
     - Channel names:  
       - **Front panel:** `REF1` and `REF2`  
       - **TS module:** `CHx-01A~10A` and `CHx-01B~10B`  
       - **PS module:** `CHx-01~10`  
     - **moduleIndex:** Module identifier (Front panel is 0, embedded module is 1, then serial-wound modules are in 2, 3, 4, depending on the connection).  
     - Example: `REF1` is used for industrial RTD Pt25(385) and `REF2` for thermistor.

3. **Set the channel configuration of one scanner**  
   - **Command format:**  
     ```
     [MEASure:]MODule:CONFig <moduleIndex>,<"params">
     ```  
   - **Example:**  
     ```
     MODule:CONFig 0,"REF1,1,,3,0,0,1,1,4,Pt25(385),,,0,0;REF2,1,,4,0,0,1,1,2,Auto Range,;"
     ```  
   - **Note:** You can refer to the returned value in command No.2 for the parameters.

4. **Read scanning configuration**  
   - **Command format:**  
     ```
     [MEASure:]SCAN:STARt?
     ```  
   - **Example:**  
     ```
     SCAN:STARt?
     ```  
   - **Returned value example:**  
     ```
     1000,REF1
     ```  
   - **Note:** In this example, the sampling frequency cycle is set as 1000 (can be 100, 1000, or 4000), and the channel name is REF1.

5. **Set the configuration and start scanning**  
   - **Command format:**  
     ```
     [MEASure:]SCAN:STARt <"params">
     ```  
   - **Example:**  
     ```
     SCAN:STARt "1000,REF1"
     ```  
   - **Returned value example:**  
     ```
     None
     ```

6. **Read scanning data (most recent)**  
   - **Command format:**  
     ```
     [MEASure:]SCAN:DATA:Last? [<time>]
     ```  
   - **Example:**  
     ```
     SCAN:DATA:Last?
     ```  
   - **Returned value example:**  
     ```
     "REF1,1281,1,28.258167,28.258167,1001,1,33.512077;"
     ```

7. **Read channel configuration**  
   - **Command format:**  
     ```
     [MEASure:]CHANnel:CONFig? <"channelName">
     ```  
   - **Example:**  
     ```
     CHANnel:CONFig? "REF1"
     ```  
   - **Returned value example:**  
     ```
     REF1,1,,3,0,0,1,1,4,Pt25(385),,,0,0
     ```

8. **Set channel configuration**  
   - **Command format:**  
     ```
     [MEASure:]CHANnel:CONFig <"chName">,<enable>,<"label">,<elecType>,<range>,<delay>,<autoRange>,<filter>,<"otherParam">
     ```  
   - **Example:**  
     ```
     CHANnel:CONFig "REF1",1,"",3,0,0,1,1,"4,Pt25(385),,,0,0"
     ```

9. **Set multi-channel configuration and start scanning**  
   - **Command format:**  
     ```
     [MEASure:]SCAN:MULT:STARt <Numeric>,<"List">
     ```  
   - **Example:**  
     ```
     SCAN:MULT:STARt 1000,"REF1,CH1-01A,CH1-02A"
     ```  
   - **Returned value example:**  
     ```
     None
     ```

10. **Stop scanning**  
    - **Command format:**  
      ```
      [MEASure:]SCAN:STOP
      ```  
    - **Example:**  
      ```
      SCAN:STOP
      ```  
    - **Returned value example:**  
      ```
      None
      ```

11. **Read channel configuration (alternate)**  
    - **Command format:**  
      ```
      [Measure:]CHANnel:CONFig? <"channelName">
      ```  
    - **Example:**  
      ```
      CHANnel:CONFig? "REF1"
      ```  
    - **Returned value example:**  
      ```
      REF1,1,,3,1,0,1,1,4,Pt100(385),,,0,0
      ```

12. **Set channel configuration (alternate)**  
    - **Command format:**  
      ```
      [MEASure:]CHANnel:CONFig <"chName">,<enable>,<"label">,<elecType>,<range>,<delay>,<autoRange>,<filter>,<"otherParam">
      ```  
    - **Example:**  
      ```
      CHANnel:CONFig "REF1",1,"",3,1,0,1,1,"4,Pt100(385),,,0,0"
      ```  
    - **Note:** Use the returned values of command No.7. Add double quotes for the first and third parameters, and combine the 9th and subsequent parameters into one quoted string.

13. **Create/Add temperature sensor**  
    - **Command format:**  
      ```
      SENSor:TEMPerature:ADD <SensorType>,<"Info">
      ```  
    - **Example:**  
      ```
      SENSor:TEMPerature:ADD SPRT,"SPTESensor,Sensor123,1281,1001,-189.344192504883,961.780029296875,11/2/2021,365,,False,-0.000579849,-3.60548E-5,-3.45108E-5,0,-0.000520946,-0.000296057,1,1,100.0131,0"
      ```  
    - **Note:** `<SensorType>` is a sensor type string; refer to the commands set document for details.

14. **Read the quantity of sensor**  
    - **Command format:**  
      ```
      SENSor:COUNt? <SensorType>
      ```  
    - **Example:**  
      ```
      SENSor:COUNt? SPRT
      ```  
    - **Returned value example:**  
      ```
      2
      ```

15. **Read sensor head information**  
    - **Command format:**  
      ```
      SENSor:CATalog:HEAD? <SensorType>,<offset>,<count>
      ```  
    - **Example:**  
      ```
      SENSor:CATalog:HEAD? SPRT,0,10
      ```  
    - **Returned value example:**  
      ```
      9d1b93d3-1aac-4f5b-8e62-a0853ef7c471,KPTESTSENSOR,KP12345667,SPRT,11/2/2021 12:00 AM,365&b364ea60-5da4-463e-8976-808af704c11e,SPTESensor,Sensor123,SPRT,11/2/2021 12:00 AM,365
      ```  
    - **Note:** The sensor ID is used when viewing and editing sensor information. Only the head information of existing sensors will be returned if the quantity exceeds what is present.

16. **Read the information of a single temperature sensor**  
    - **Command format:**  
      ```
      SENSor:TEMPerature:INFormations? <id>
      ```  
    - **Example:**  
      ```
      SENSor:TEMPerature:INFormations? b364ea60-5da4-463e-8976-808af704c11e
      ```  
    - **Returned value example:**  
      ```
      SPRT,"SPTESensor,Sensor123,1281,1001,-189.344192504883,961.780029296875,11/2/2021,365,,False,-0.000579849,-3.60548E-5,-3.45108E-5,0,-0.000520946,-0.000296057,1,1,100.0131,0"
      ```

17. **Edit/Change the information of an existing temperature sensor**  
    - **Command format:**  
      ```
      SENSor:TEMPerature:EDIT <id>,<"Info">
      ```  
    - **Example:**  
      ```
      SENSor:TEMPerature:EDIT b364ea60-5da4-463e-8976-808af704c11e,"SPTESensor,Sensor111,1281,1001,-189.344192504883,961.780029296875,11/2/2021,365,,False,-0.000579849,-3.60548E-5,-3.45108E-5,0,-0.000520946,-0.000296057,1,1,100.0131,0"
      ```  
    - **Note:** In this example, the sensor's S/N changes from Sensor123 to Sensor111.

18. **Delete the information of a temperature sensor**  
    - **Command format:**  
      ```
      SENSor:TEMPerature:DELete <"ids">
      ```  
    - **Example:**  
      ```
      SENSor:TEMPerature:DELete "9d1b93d3-1aac-4f5b-8e62-a0853ef7c471,b364ea60-5da4-463e-8976-808af704c11e"
      ```  
    - **Note:** Multiple sensor IDs can be deleted at once; separate different IDs with commas (no spaces).
