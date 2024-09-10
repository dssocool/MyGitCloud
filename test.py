import ctypes
import ctypes.wintypes as wintypes

def get_secure_user_token():
    # Define necessary Windows structures and constants
    advapi32 = ctypes.windll.advapi32
    kernel32 = ctypes.windll.kernel32

    # Token information structures
    class TOKEN_USER(ctypes.Structure):
        _fields_ = [
            ('User', ctypes.c_byte * 12)  # Placeholder, actual size varies
        ]
    
    TokenUser = 1
    ERROR_INSUFFICIENT_BUFFER = 122

    # Get the process token for the current process
    token_handle = wintypes.HANDLE()
    if not advapi32.OpenProcessToken(kernel32.GetCurrentProcess(), 0x0008, ctypes.byref(token_handle)):
        raise ctypes.WinError()

    # First, determine the size of the buffer needed for the TOKEN_USER structure
    token_info_length = wintypes.DWORD()
    advapi32.GetTokenInformation(token_handle, TokenUser, None, 0, ctypes.byref(token_info_length))
    
    # Check if buffer size is insufficient
    if kernel32.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError()

    # Allocate buffer for the TOKEN_USER structure
    token_user = TOKEN_USER()
    token_user_ptr = ctypes.byref(token_user)
    token_user_size = token_info_length.value

    # Allocate memory for user info
    buffer = ctypes.create_string_buffer(token_user_size)

    # Retrieve the TOKEN_USER structure with user information
    if not advapi32.GetTokenInformation(token_handle, TokenUser, buffer, token_user_size, ctypes.byref(token_info_length)):
        raise ctypes.WinError()

    # The SID (security identifier) of the user is in the TOKEN_USER structure, and
    # this needs to be translated to a human-readable name (DOMAIN\username)
    sid = ctypes.cast(buffer, ctypes.POINTER(wintypes.LPVOID))[0]
    
    # Retrieve the username
    name_size = wintypes.DWORD(0)
    domain_size = wintypes.DWORD(0)
    advapi32.LookupAccountSidW(None, sid, None, ctypes.byref(name_size), None, ctypes.byref(domain_size), None)
    
    name = ctypes.create_unicode_buffer(name_size.value)
    domain = ctypes.create_unicode_buffer(domain_size.value)
    
    sid_name_use = ctypes.c_ulong()
    
    if not advapi32.LookupAccountSidW(None, sid, name, ctypes.byref(name_size), domain, ctypes.byref(domain_size), ctypes.byref(sid_name_use)):
        raise ctypes.WinError()

    return f"{domain.value}\\{name.value}"

try:
    secure_user_token = get_secure_user_token()
    print(f"Securely logged in user via token: {secure_user_token}")
except Exception as e:
    print(f"Error: {e}")
