import rp.data
from rp.parser import State
import struct, binascii
from construct import *

POLICY_ENTER_DELIM      = u'['.encode('utf_16_le')
POLICY_EXIT_DELIM       = u']'.encode('utf_16_le')
POLICY_SECTION_DELIM    = u';'.encode('utf_16_le')
POLICY_SECTION_TERM     = u'\0'.encode('utf_16_le')
POLICY_SZ_EXIT_TERM     = u'\0\0'.encode('utf_16_le')
Temp                    = u'}'.encode('utf_16_le')

class Signature(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'version'
    
    def process(self, data):
        signature, = struct.unpack('<I', data)
        
        if signature != 0x67655250:
            raise Exception('Invalid File: Header')
        
        self.memory['rpdata'].header.signature = signature
        
        return True
    
class Version(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_enter'
    
    def process(self, data):
        version, = struct.unpack('<I', data)
        
        if version != 1:
            raise Exception('Invalid File: Version')
        
        self.memory['rpdata'].header.version = version
        
        return True   

class PolicyEnter(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_key'
    
    def process(self, data):
        if data != POLICY_ENTER_DELIM:
            raise Exception('Invalid or Corrupt File: PolicyEnter Delim Missing')
        
        self.memory['policy'] = rp.data.RPPolicy()
        
        return True

class PolicyDelim(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = None
    
    def process(self, data):
        
        if data != POLICY_SECTION_DELIM:
            raise Exception('Invalid or Corrupt File: BodyDelim Delim Missing')
        
        self.next_state = self.memory['next_state']
        
        return True
    
class PolicyExit(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_enter'
    
    def process(self, data):
        if data != POLICY_EXIT_DELIM:
            raise Exception('Invalid or Corrupt File: PolicyExit Delim Missing')

        self.memory['rpdata'].body.add_policy(self.memory['policy'])
                
        return True
    
class PolicyKey(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_delim'
        
        self.key = u''.encode('utf_16_le') 
        
        self.memory['next_state'] = 'policy_value'
    

    def process(self, data):

        if data != POLICY_SECTION_TERM:
            self.key += data
            
            return False
        
        self.memory['policy'].key = self.key
        
        return True

class PolicyValue(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_delim'
        
        self.value = u''.encode('utf_16_le')
        
        self.memory['next_state'] = 'policy_reg_type'

    def process(self, data):

        if data != POLICY_SECTION_TERM:
            self.value += data
            
            return False
        
        self.memory['policy'].value = self.value
        
        return True 

class PolicyRegType(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_delim'
        
        self.memory['next_state'] = 'policy_size'

    def process(self, data):
        
        regtype, = struct.unpack('<I', data)
        
        self.memory['policy'].regtype = regtype
        
        return True

class PolicySize(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_delim'
        
        self.memory['next_state'] = 'policy_data'

    def process(self, data):
        
        size, = struct.unpack('<I', data)
        
        self.memory['policy'].size = size
        
        return True
    
class PolicyData(object):  
    def __new__(class_object, memory):
        regtype = memory['policy'].regtype

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
        
        '''
            #define REG_NONE                0       /* no type */
            #define REG_SZ                  1       /* string type (ASCII) */
            #define REG_EXPAND_SZ           2       /* string, includes %ENVVAR% (expanded by caller) (ASCII) */
            #define REG_BINARY              3       /* binary format, callerspecific */
            #define REG_DWORD               4       /* DWORD in little endian format */
            #define REG_DWORD_LITTLE_ENDIAN 4       /* DWORD in little endian format */
            #define REG_DWORD_BIG_ENDIAN    5       /* DWORD in big endian format  */
            #define REG_LINK                6       /* symbolic link (UNICODE) */
            #define REG_MULTI_SZ            7       /* multiple strings, delimited by \0, terminated by \0\0 (ASCII) */
            #define REG_RESOURCE_LIST       8       /* resource list? huh? */
            #define REG_FULL_RESOURCE_DESCRIPTOR    9       /* full resource descriptor? huh? */
            #define REG_RESOURCE_REQUIREMENTS_LIST  10
            #define REG_QWORD               11      /* QWORD in little endian format */
            #define REG_QWORD_LITTLE_ENDIAN 11      /* QWORD in little endian format */
        '''
        
        if regtype == 0: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_NONE)
        elif regtype == 1: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_SZ)
        elif regtype == 2: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_EXPAND_SZ)
        elif regtype == 3: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_BINARY)
        elif regtype == 4: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_DWORD)
        elif regtype == 5: raise NotImplementedError('Data type 5 is not implemented')
        elif regtype == 6: raise NotImplementedError('Data type 6 is not implemented')
        elif regtype == 7: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_MULTI_SZ)
        elif regtype == 8: raise NotImplementedError('Data type 8 is not implemented')
        elif regtype == 9: raise NotImplementedError('Data type 9 is not implemented')
        elif regtype == 10: raise NotImplementedError('Data type 10 is not implemented')
        elif regtype == 11: policy_data_object = super(PolicyData, class_object).__new__(PolicyDataREG_QWORD)
        else: raise NotImplementedError('Unknown Data type')
        
        policy_data_object.__init__(memory)
        
        return policy_data_object
    
class PolicyDataREG_NONE(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 0
        self.next_state     = 'policy_exit'
        
        self.reg_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        return True

class PolicyDataREG_SZ(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_exit'
        
        self.reg_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        
        if data != POLICY_SECTION_TERM:
            self.reg_sz += data
            
            return False
        
        self.memory['policy'].data = self.reg_sz
        
        return True

class PolicyDataREG_EXPAND_SZ(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 2
        self.next_state     = 'policy_exit'
        
        self.reg_expand_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        if data != POLICY_SECTION_TERM:
            self.reg_expand_sz += data
            
            return False
        
        self.memory['policy'].data = self.reg_expand_sz
        
        return True

# @TODO Fix decoding issues
# Issue with decoding Multi_sz - doesn't seem to take the exit_delim into account for some reason
class PolicyDataREG_MULTI_SZ(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_exit'
        
        self.reg_multi_sz         = u''.encode('utf_16_le')
    
    def process(self, data):
        if data != POLICY_SZ_EXIT_TERM:
            self.reg_multi_sz += data
            
            return False
        
        self.memory['policy'].data = self.reg_multi_sz
        
        return True

class PolicyDataREG_BINARY(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = memory['policy'].size
        self.next_state     = 'policy_exit'

        self.reg_binary     = u''.encode('utf_16_le')
    
    def process(self, data):
        try:
            reg_dword = data.decode('utf-16-le').rstrip('\x00')
            
        except UnicodeDecodeError:
            try:
                reg_dword = data.decode().rstrip('\x00')
            except:
                reg_dword = data

        self.memory['policy'].data = reg_dword
        return True


class PolicyDataREG_DWORD(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 4
        self.next_state     = 'policy_exit'
    
    def process(self, data):
        reg_dword, = struct.unpack('<I', data)
        
        self.memory['policy'].data = reg_dword
        
        return True


class PolicyDataREG_QWORD(State):
    def __init__(self, memory):
        self.memory         = memory
        
        self.data_size      = 8
        self.next_state     = 'policy_exit'
    
    def process(self, data):
        
        reg_qword, = struct.unpack('<q', data)

        self.memory['policy'].data = reg_qword
        
        return True
