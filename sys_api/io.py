import os


ERR_MSG = {
    1:  "Operation not permitted",
    2: "No such file or directory",
    3: "No such process",
    4: "Interrupted system call",
    5: "Input/output error",
    6: "No such device or address",
    7: "Argument list too long",
    8: "Exec format error",
    9: "Bad file descriptor",
    10:  "No child processes",
    11:  "Resource temporarily unavailable",
    12:  "Cannot allocate memory",
    13:  "Permission denied",
    14:  "Bad address",
    15:  "Block device required",
    16:  "Device or resource busy",
    17:  "File exists",
    18:  "Invalid cross-device link",
    19:  "No such device",
    20:  "Not a directory",
    21:  "Is a directory",
    22:  "Invalid argument",
    23:  "Too many open files in system",
    24:  "Too many open files",
    25:  "Inappropriate ioctl for device",
    26:  "Text file busy",
    27:  "File too large",
    28:  "No space left on device",
    29:  "Illegal seek",
    30:  "Read-only file system",
    31:  "Too many links",
    32:  "Broken pipe",
    33:  "Numerical argument out of doma in",
    34:  "Numerical result out of range",
    35:  "Resource deadlock avoided",
    36:  "File name too long",
    37:  "No locks available",
    38:  "Function not implemented",
    39:  "Directory not empty",
    40:  "Too many levels of symbolic links",
    41:  "No message of desired type",
    42:  "Identifier removed",
    43:  "Channel number out of range",
    44:  "Level 2 not synchronized",
    45:  "Level 3 halted",
    46:  "Level 3 reset",
    47:  "Link number out of range",
    48:  "Protocol driver not attached",
    49:  "No CSI structure available",
    50:  "Level 2 halted",
    51:  "Invalid exchange",
    52:  "Invalid request descriptor",
    53:  "Exchange full",
    54:  "No anode",
    55:  "Invalid request code",
    56:  "Invalid slot",
    57:  "Bad font file format",
    58:  "Device not a stream",
    59:  "No data available",
    60:  "Timer expired",
    61:  "Out of streams resources",
    62:  "Machine is not on the network",
    63:  "Package not installed",
    64:  "Object is remote",
    65:  "Link has been severed",
    66:  "Advertise error",
    67:  "Srmount error",
    68:  "Communication error on send",
    69:  "Protocol error",
    70:  "Multihop attempted",
    71:  "RFS specific error",
    72:  "Bad message",
    73:  "Value too large for defined data type",
    74:  "Name not unique on network",
    75:  "File descriptor in bad state",
    76:  "Remote address changed",
    77:  "Can not access a needed shared, library",
    78:  "Accessing a corrupted shared l,ibrary",
    79:  ".lib section in a.out corrupte,d",
    80:  "Attempting to link in too many, shared libraries",
    81:  "Cannot exec a shared library d,irectly",
    82:  "Invalid or incomplete multibyt,e or wide character",
    83:  "Interrupted system call should, be restarted",
    84:  "Streams pipe error",
    85:  "Too many users",
    86:  "Socket operation on non-socket",
    87:  "Destination address required",
    88:  "Message too long",
    89:  "Protocol wrong type for socket",
    90:  "Protocol not available",
    91:  "Protocol not supported",
    92:  "Socket type not supported",
    93:  "Operation not supported",
    94:  "Protocol family not supported",
    95:  "Address family not supported b,y protocol",
    96:  "Address already in use",
    97:  "Cannot assign requested address",
    98:  "Network is down",
    99:  "Network is unreachable",
    100:  "Network dropped connection on ,reset",
    101:  "Software caused connection abo,rt",
    102:  "Connection reset by peer",
    103:  "No buffer space available",
    104:  "Transport endpoint is already ,connected",
    105:  "Transport endpoint is not conn,ected",
    106:  "Cannot send after transport en,dpoint shutdown",
    107:  "Too many references: cannot sp,lice",
    108:  "Connection timed out",
    109:  "Connection refused",
    110:  "Host is down",
    111:  "No route to host",
    112:  "Operation already in progress",
    113:  "Operation now in progress",
    114:  "Stale NFS file handle",
    115:  "Structure needs cleaning",
    116:  "Not a XENIX named type file",
    117:  "No XENIX semaphores available",
    118:  "Is a named type file",
    119:  "Remote I/O error",
    120:  "Disk quota exceeded",
    121:  "No medium found",
    122:  "Wrong medium type",
    123:  "Operation canceled",
    124:  "Required key not available",
    125:  "Key has expired",
    126:  "Key has been revoked",
    127:  "Key was rejected by service",
    128:  "Owner died",
    129:  "State not recoverableState:",
}


class io:


    def __init__(self, sdb="/dev/sdb", mount_path="/mnt/sdb", save_path="/mnt/sdb"):
        self.__sdb = sdb
        self.__save_path = os.path.abspath(save_path)
        self.__mount_path = os.path.abspath(mount_path)
        self.mount()

    def set_save_path(self, save_path):
        self.__save_path = os.path.abspath(save_path)

    def mount(self):
        if not os.path.isdir(self.__mount_path):
            os.makedirs(self.__mount_path)

        code = os.system(f"mount '{self.__sdb}' '{self.__mount_path}'")
        if code != 0 and code < 129:
            return "%s code: %s" % (ERR_MSG[code], code)
        elif code != 0:
            return "code: %s" % code

        return code
        
    def compress_dir(self, dir_path, save_gzip_name):
            if not os.path.isdir(dir_path):
                return

            code = os.system(f"tar -zcPf '{self.__save_path}/{save_gzip_name}.tar.gz' '{dir_path}'")
            if code != 0:
                return "%s code: %s" % (ERR_MSG[code], code)
                
            if not os.path.isfile(f"{self.__save_path}/{save_gzip_name}.tar.gz"):
                return f"io err: null {self.__save_path}{save_gzip_name}.tar.gz"
            
            return code

    def cp(self, file_path):
        if not os.path.isdir(file_path):
            return

        file_name = file_path.split("/")[-1]
        save_in = f"{self.__save_path}/{file_name}"
        if not os.path.isdir(save_in):
            os.makedirs(save_in)
            
        code = os.system(f"cp -r {file_path} {self.__save_path}/{file_name}")
        if code != 0 and code < 129:
            return "%s code: %s" % (ERR_MSG[code], code)
        elif code != 0:
            return "code: %s" % code

        return code

    def __enter__(self):
        return self
    
    def __exit__(self, type, val, tra):
        os.system(f"umount '{self.__sdb}'")