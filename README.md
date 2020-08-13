# SYSVOL-Reader

Adaptation of the [SYSVOL reader](https://github.com/DLWood1001/Registry-Policy-Module) by DLWood1001. There are some excellent [PowerShell Projects](https://github.com/PowerShell/GPRegistryPolicy) which do the same thing, I just needed to access the SYSVOL files in Python.

## Updates to the Project
Since the repository was last updated around 8 years ago at the time of creating this repository, I decided to just update it myself instead of forking and pushing new code. Updates to the project include:
* Additional windows registry data types (QWORD, EXPAND_SZ, MULTI_SZ, BINARY) 
* Updated code to Python 3
* Removed circular references for file imports
* Added functionality to read in an entire SYSVOL directory or individual files based on user requirement
* Reading additional files:
  * Policy (.pol) Files
  * Setup Information (.inf) Files
  * Configuration Settings (.ini) Files
  
## SYSVOL Parsing
Reads either the entire SYSVOL structure or a single .pol file containing group policy registry entries. It then outputs the Key, Value, and Data fields associated with the .pol files. After specifying the "sysvol" parameter, the user will be prompted for a path to the SYSVOL directory or individual .pol file.
 
### Syntax
```bat
python3 gpread.py -s/--sysvol
```
| Parameter Name	  |  Description |
|---|---|
| -s / --sysvol  | Specifies that the .pol files need to be parsed. |


## Configuration and Setup File Parsing
Reads either the entire SYSVOL structure or a single .ini or .inf file. It then outputs the information contained within these files. After specifying the "config" parameter, the user will be prompted for a path to the SYSVOL directory or individual .ini or .inf files.

### Syntax
```bat
python3 gpread.py -c/--config
```
| Parameter Name	  |  Description |
|---|---|
| -c / --config  | Specifies that the .ini and .inf files need to be parsed. |


## Debugging
Within the states.py file, I added in some basic debugging code when trying to identify issues in parsing the data. In order to run the debugging portion you simply need to change `debugging = False` to `debugging = True`.

```python
        debugging = False
        if debugging:
            print("Memory Object: " + str(memory))

            print("\n\nRPData Object: " + str(vars(memory['rpdata'])))
            print("RPData Header Object: " + str(vars(memory['rpdata'].header)))
            print("RPData Body Object: " + str(vars(memory['rpdata'].body)))
            print("RPData Body Policy Object: " + str(memory['rpdata'].body.policies))
            for i in memory['rpdata'].body.policies:
                print("Value: " + str(i.key.decode("utf_16_le")))

            print("\n\nPolicy Object: " + str(vars(memory['policy'])))
            print("Policy Object Key: " + str(memory['policy'].key.decode("utf_16_le")))
            print("Policy Object Values: " + str(memory['policy'].value.decode("utf_16_le")))
            print("Policy Object RegType: " + str(memory['policy'].regtype))
            print("Policy Object Data: " + str(memory['policy'].data))
            
            print("\n\nNextState Object: \n" + str(memory['next_state']))
```

## Current Issues
* There are still issues with decoding MULTI_SZ and BINARY: The way the script currently works, it should print out some values and not get stuck.
* Unimplemented Reg_Types: The SYSVOL structures that I currently have access to do not make use of the additional Reg_Types, so I haven't been able to determine what is required for decoding them. 



