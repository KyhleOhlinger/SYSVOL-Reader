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
```
python3 gpread.py -s/--sysvol
```
| Parameter Name	  |  Description |
|---|---|
| -s / --sysvol  | Specifies that the .pol files need to be parsed. |


## Configuration and Setup File Parsing
Reads either the entire SYSVOL structure or a single .ini or .inf file. It then outputs the information contained within these files. After specifying the "config" parameter, the user will be prompted for a path to the SYSVOL directory or individual .ini or .inf files.

### Syntax
```
python3 gpread.py -c/--config
```
| Parameter Name	  |  Description |
|---|---|
| -c / --config  | Specifies that the .ini and .inf files need to be parsed. |
