# coding: utf-8


# Copyright (c) 2013-2017 Shohei Tanaka(@xcir)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# https://github.com/xcir/python-varnishapi
# v52.23

from ctypes import *
import getopt
import time



class VUT (Structure):
    _fields_ = [
        ("magic" , c_uint),   #unsigned	magic;
        ("progname" , c_char_p),            #const char	*progname;
        ("d_opt" , c_int),                  #int		d_opt;
        ("D_opt" , c_int),                  #int		D_opt;
        ("g_arg" , c_int),                  #int		g_arg;
        ("k_arg" , c_int),                  #int		k_arg;
        ("n_arg" , c_char_p),               #char		*n_arg;
        ("P_arg" , c_char_p),               #char		*P_arg;
        ("q_arg" , c_char_p),               #char		*q_arg;
        ("r_arg" , c_char_p),               #char		*r_arg;
        ("t_arg" , c_char_p),               #char		*t_arg;
        ("vsl" , c_void_p),                 #struct VSL_data	*vsl;
        ("vsm" , c_void_p),                 #struct vsm	*vsm;
        ("vslq" , c_void_p),                #struct VSLQ	*vslq;
        ("sighup" , c_int),                 #int		sighup;
        ("sigint" , c_int),                 #int		sigint;
        ("sigusr1" , c_int),                #int		sigusr1;
        ("idle_f" , c_void_p),              #VUT_cb_f	*idle_f;
        ("sighup_f" , c_void_p),            #VUT_cb_f	*sighup_f;
        ("error_f" , c_void_p),             #VUT_error_f	*error_f;
        ("dispatch_f" , c_void_p),          #VSLQ_dispatch_f	*dispatch_f;
        ("dispatch_priv" , c_void_p)        #void		*dispatch_priv;
    ]

class VSC_level_desc(Structure):
    _fields_ = [
        ("verbosity", c_uint),  # unsigned verbosity;
        ("label", c_char_p),    # const char *label;  /* label */
        ("sdesc", c_char_p),    # const char *sdesc;  /* short description */
        ("ldesc", c_char_p),    # const char *ldesc;  /* long description */
    ]

class VSC_level_desc20(Structure):
    _fields_ = [
        ("name",  c_char_p),    # const char *name;   /* name */
        ("label", c_char_p),    # const char *label;  /* label */
        ("sdesc", c_char_p),    # const char *sdesc;  /* short description */
        ("ldesc", c_char_p),    # const char *ldesc;  /* long description */
    ]

class VSC_type_desc(Structure):
    _fields_ = [
        ("label", c_char_p),  # const char *label;    /* label */
        ("sdesc", c_char_p),  # const char *sdesc;    /* short description */
        ("ldesc", c_char_p),  # const char *ldesc;    /* long description */
    ]


class VSM_fantom(Structure):
    _fields_ = [
        ("chunk", c_void_p),      # struct VSM_chunk *chunk;
        ("b", c_void_p),          # void *b;   /* first byte of payload */
        ("e", c_void_p),          # void *e;   /* first byte past payload */
        ("priv", c_void_p),       # uintptr_t priv; /* VSM private */
        ("_class", c_char * 8),   # char class[VSM_MARKER_LEN];
        ("type", c_char * 8),     # char type[VSM_MARKER_LEN];
        ("ident", c_char * 128),  # char ident[VSM_IDENT_LEN];
    ]


class VSC_section(Structure):
    _fields_ = [
        ("type", c_char_p),                # const char *type;
        ("ident", c_char_p),               # const char *ident;
        ("desc", POINTER(VSC_type_desc)),  # const struct VSC_type_desc *desc;
        ("fantom", POINTER(VSM_fantom)),   # struct VSM_fantom *fantom;
    ]


class VSC_desc(Structure):
    _fields_ = [
        
        ("name", c_char_p),                 # const char *name;     /* field name                   */
        ("fmt", c_char_p),                  # const char *fmt;      /* field format ("uint64_t")    */
        ("flag", c_int),                    # int flag;             /* 'c' = counter, 'g' = gauge   */
        ("sdesc", c_char_p),                # const char *sdesc;    /* short description            */
        ("ldesc", c_char_p),                # const char *ldesc;    /* long description             */
        ("level", POINTER(VSC_level_desc)), # const struct VSC_level_desc *level;
    ]


class VSC_point(Structure):
    _fields_ = [
        ("desc", POINTER(VSC_desc)),          # const struct VSC_desc *desc;  /* point description            */
        ("ptr", POINTER(c_ulonglong)),        # const volatile void *ptr;     /* field value                  */
        ("section", POINTER(VSC_section)),    # const struct VSC_section *section;
    ]

class VSC_point20(Structure):
    _fields_ = [
        ("ptr",  POINTER(c_ulonglong)),       #const volatile uint64_t *ptr;	/* field value			*/
        ("name", c_char_p),                   #const char *name;		/* field name			*/
        ("ctype", c_char_p),                  #const char *ctype;		/* C-type			*/
        ("semantics", c_int),                 #int semantics;			/* semantics			*/
        ("format", c_int),                    #int format;			/* display format		*/
        ("level", POINTER(VSC_level_desc20)), #const struct VSC_level_desc *level; /* verbosity level		*/
        ("sdesc", c_char_p),                  #const char *sdesc;		/* short description		*/
        ("ldesc", c_char_p),                  #const char *ldesc;		/* long description		*/
        ("priv",  c_void_p),                  #void *priv;			/* return val from VSC_new_f	*/

    ]

# typedef int VSC_iter_f(void *priv, const struct VSC_point *const pt);
VSC_iter_f = CFUNCTYPE(
    c_int,
    c_void_p,
    POINTER(VSC_point)
)
# typedef int VSC_iter_f(void *priv, const struct VSC_point *const pt);
VSC_iter_f20 = CFUNCTYPE(
    c_int,
    c_void_p,
    POINTER(VSC_point20)
)

# typedef void VSL_tagfind_f(int tag, void *priv);
VSL_tagfind_f = CFUNCTYPE(
    c_int,
    c_void_p
)

#typedef void *VSC_new_f(void *priv, const struct VSC_point *const pt);
VSC_new_f = CFUNCTYPE(
    c_void_p,
    c_void_p,
    POINTER(VSC_point20)
)

#typedef void VSC_destroy_f(void *priv, const struct VSC_point *const pt);
VSC_destroy_f = CFUNCTYPE(
    None,
    c_void_p,
    POINTER(VSC_point20)
)

#


class VSLC_ptr(Structure):
    _fields_ = [
        ("ptr", POINTER(c_uint32)), # const uint32_t *ptr; /* Record pointer */
        ("priv", c_uint),           # unsigned priv;
    ]


class VSL_cursor(Structure):
    _fields_ = [
        ("rec", VSLC_ptr),        # struct VSLC_ptr rec;
        ("priv_tbl", c_void_p),   # const void      *priv_tbl;
        ("priv_data", c_void_p),  # void            *priv_data;
    ]


class VSL_transaction(Structure):
    _fields_ = [
        ("level", c_uint),           # unsigned               level;
        ("vxid", c_int32),           # int32_t                vxid;
        ("vxid_parent", c_int32),    # int32_t                vxid_parent;
        ("type", c_int),             # enum VSL_transaction_e type;
        ("reason", c_int),           # enum VSL_reason_e      reason;
        ("c", POINTER(VSL_cursor)),  # struct VSL_cursor      *c;
    ]


class VTAILQ_HEAD(Structure):
    _fields_ = [
        ("vtqh_first", c_void_p),         # struct type *vtqh_first;    /* first element */
        ("vtqh_last", POINTER(c_void_p)), # struct type **vtqh_last;    /* addr of last next element */
    ]


class vbitmap(Structure):
    _fields_ = [
        ("bits", c_void_p),  # VBITMAP_TYPE    *bits;
        ("nbits", c_uint),   # unsigned        nbits;
    ]


class vsb(Structure):
    _fields_ = [
        ("magic", c_uint),       # unsigned   magic;
        ("s_buf", c_char_p),     # char       *s_buf;    /* storage buffer */
        ("s_error", c_int),      # int        s_error;   /* current error code */
        ("s_size", c_long),      # ssize_t    s_size;    /* size of storage buffer */
        ("s_len", c_long),       # ssize_t    s_len;     /* current length of string */
        ("s_flags", c_int),      # int        s_flags;   /* flags */
    ]


class VSL_data(Structure):
    _fields_ = [
        ("magic", c_uint),                  # unsigned           magic;
        ("diag", POINTER(vsb)),             # struct vsb         *diag;
        ("flags", c_uint),                  # unsigned           flags;
        ("vbm_select", POINTER(vbitmap)),   # struct vbitmap     *vbm_select;
        ("vbm_supress", POINTER(vbitmap)),  # struct vbitmap     *vbm_supress;
        ("vslf_select", VTAILQ_HEAD),       # vslf_list          vslf_select;
        ("vslf_suppress", VTAILQ_HEAD),     # vslf_list          vslf_suppress;
        ("b_opt", c_int),                   # int                b_opt;
        ("c_opt", c_int),                   # int                c_opt;
        ("C_opt", c_int),                   # int                C_opt;
        ("L_opt", c_int),                   # int                L_opt;
        ("T_opt", c_double),                # double             T_opt;
        ("v_opt", c_int),                   # int                v_opt;
    ]

class timespec(Structure):
    _fields_ = [
        ("tv_sec" , c_long),             # time_t   tv_sec;        /* seconds */
        ("tv_nsec", c_long),             # long     tv_nsec;       /* nanoseconds */
    ]

class timeval (Structure):
    _fields_ = [
        ("tv_sec" , c_long),             # time_t      tv_sec;
        ("tv_usec", c_long),             # suseconds_t tv_usec
    ]

class vopt_list (Structure):
    _fields_ = [
        ("option" , c_char_p),   #const char *option;
        ("synopsis" , c_char_p), #const char *synopsis;
        ("desc" , c_char_p),     #const char *desc;
        ("ldesc" , c_char_p),    #const char *ldesc;
    ]

class vopt_spec (Structure):
    _fields_ = [
        ("vopt_list" , POINTER(vopt_list)),   #const struct  vopt_list *vopt_list;
        ("vopt_list_n" , c_uint),             #unsigned      vopt_list_n;
        ("vopt_optstring" , c_char_p),        #const char    *vopt_optstring;
        ("vopt_synopsis" , c_char_p),         #const char    *vopt_synopsis;
        ("vopt_usage" , POINTER(c_char_p)),   #const char    **vopt_usage;

    ]





class VarnishAPIDefine40:

    def __init__(self):
        self.VSL_COPT_TAIL = (1 << 0)
        self.VSL_COPT_BATCH = (1 << 1)
        self.VSL_COPT_TAILSTOP = (1 << 2)
        self.SLT_F_BINARY = (1 << 1)
        
        self.VSM_MGT_RUNNING = (1 << 1)
        self.VSM_MGT_CHANGED = (1 << 2)
        self.VSM_MGT_RESTARTED =(1 << 3)
        self.VSM_WRK_RUNNING = (1 << 9)
        self.VSM_WRK_CHANGED = (1 << 10)
        self.VSM_WRK_RESTARTED = (1 << 11)

        '''
        //////////////////////////////
        enum VSL_transaction_e {
            VSL_t_unknown,
            VSL_t_sess,
            VSL_t_req,
            VSL_t_bereq,
            VSL_t_raw,
            VSL_t__MAX,
        };
        '''
        self.VSL_t_unknown = 0
        self.VSL_t_sess = 1
        self.VSL_t_req = 2
        self.VSL_t_bereq = 3
        self.VSL_t_raw = 4
        self.VSL_t__MAX = 5

        '''
        //////////////////////////////
        enum VSL_reason_e {
            VSL_r_unknown,
            VSL_r_http_1,
            VSL_r_rxreq,
            VSL_r_esi,
            VSL_r_restart,
            VSL_r_pass,
            VSL_r_fetch,
            VSL_r_bgfetch,
            VSL_r_pipe,
            VSL_r__MAX,
        };
        '''
        self.VSL_r_unknown = 0
        self.VSL_r_http_1 = 1
        self.VSL_r_rxreq = 2
        self.VSL_r_esi = 3
        self.VSL_r_restart = 4
        self.VSL_r_pass = 5
        self.VSL_r_fetch = 6
        self.VSL_r_bgfetch = 7
        self.VSL_r_pipe = 8
        self.VSL_r__MAX = 9

        '''
        //////////////////////////////
        enum VSM_valid_e {
            VSM_invalid,
            VSM_valid,
            VSM_similar,
        };
        '''
        self.VSM_invalid = 0
        self.VSM_valid = 1
        self.VSM_similar = 2

        '''
        //////////////////////////////
        enum vas_e {
            VAS_WRONG,
            VAS_MISSING,
            VAS_ASSERT,
            VAS_INCOMPLETE,
            VAS_VCL,
        };
        '''
        self.VAS_WRONG = 0
        self.VAS_MISSING = 1
        self.VAS_ASSERT = 2
        self.VAS_INCOMPLETE = 3
        self.VAS_VCL = 4


#typedef void VUT_sighandler_f(int);
VUT_sighandler_f = CFUNCTYPE(
    None,
    c_int
)

# typedef int VSLQ_dispatch_f(struct VSL_data *vsl, struct VSL_transaction
# * const trans[], void *priv);
VSLQ_dispatch_f = CFUNCTYPE(
    c_int,
    POINTER(VSL_data),
    POINTER(POINTER(VSL_transaction)),
    c_void_p
)

# typedef int VUT_cb_f(struct VUT *);
VUT_cb_f = CFUNCTYPE(
    c_int,
    POINTER(VUT)
)
class LIBVARNISHAPI10:
    def __init__(self, lc):
        self.lc = lc
    
    def run(self, lib):
        if hasattr(lib, "VTIM_format"):
            self.lc.apiversion = 1.6
        elif hasattr(lib, "VUT_Init"):
            self.lc.apiversion = 1.5
        elif hasattr(lib, "VSM_IsOpen"):
            self.lc.apiversion = 1.4
        else:
            self.lc.apiversion = 1.3

        #LIBVARNISHAPI_1.0
        #VSM_New;
        self.lc.VSM_New = lib.VSM_New
        self.lc.VSM_New.restype = c_void_p

        #VSM_Diag; (undefined symbol at 4.0/4.1/5.0)
        #VSM_n_Arg;
        self.lc.VSM_n_Arg = lib.VSM_n_Arg
        self.lc.VSM_n_Arg.restype = c_int
        self.lc.VSM_n_Arg.argtypes = [c_void_p, c_char_p]

        #VSM_Name;
        self.lc.VSM_Name = lib.VSM_Name
        self.lc.VSM_Name.restype = c_char_p
        self.lc.VSM_Name.argtypes = [c_void_p]

        #VSM_Delete;
        self.lc.VSM_Delete = lib.VSM_Delete
        self.lc.VSM_Delete.argtypes = [c_void_p]

        #VSM_Open;
        self.lc.VSM_Open = lib.VSM_Open
        self.lc.VSM_Open.restype = c_int
        self.lc.VSM_Open.argtypes = [c_void_p]

        #VSM_ReOpen; (undefined symbol at 4.0/4.1/5.0)
        #VSM_Seq; (undefined symbol at 4.0/4.1/5.0)
        #VSM_Head; (undefined symbol at 4.0/4.1/5.0)
        #VSM_Find_Chunk; (undefined symbol at 4.0/4.1/5.0)

        #VSM_Close;
        self.lc.VSM_Close = lib.VSM_Close
        self.lc.VSM_Close.argtypes = [c_void_p]

        #VSM_iter0; (undefined symbol at 4.0/4.1/5.0)
        #VSM_intern; (undefined symbol at 4.0/4.1/5.0)
        #
        #VSC_Setup; (undefined symbol at 4.0/4.1/5.0)
        #VSC_Arg;
        self.lc.VSC_Arg = lib.VSC_Arg
        self.lc.VSC_Arg.restype = c_int
        self.lc.VSC_Arg.argtypes = [c_void_p, c_int, c_char_p]

        #VSC_Open; (undefined symbol at 4.0/4.1/5.0)
        #VSC_Main;
        self.lc.VSC_Main = lib.VSC_Main
        self.lc.VSC_Main.restype = c_void_p
        self.lc.VSC_Main.argtypes = [c_void_p, c_void_p]

        #VSC_Iter;
        self.lc.VSC_Iter = lib.VSC_Iter
        self.lc.VSC_Iter.argtypes = [c_void_p, c_void_p, VSC_iter_f, c_void_p]

        #
        #VSL_Setup; (private func at 5.0)
        #VSL_Open; (undefined symbol at 4.0/4.1/5.0)
        #VSL_Arg;
        self.lc.VSL_Arg = lib.VSL_Arg
        self.lc.VSL_Arg.restype = c_int
        self.lc.VSL_Arg.argtypes = [c_void_p, c_int, c_char_p]

        #VSL_H_Print; (undefined symbol at 4.0/4.1/5.0)
        #VSL_Select; (undefined symbol at 4.0/4.1/5.0)
        #VSL_NonBlocking; (undefined symbol at 4.0/4.1/5.0)
        #VSL_Dispatch; (undefined symbol at 4.0/4.1/5.0)
        #VSL_NextLog; (undefined symbol at 4.0/4.1/5.0)
        #VSL_Matched; (undefined symbol at 4.0/4.1/5.0)
        #
        #VCLI_WriteResult;
        #VCLI_ReadResult;
        #VCLI_AuthResponse;
        #
        ## Variables
        #VSL_tags;

        #LIBVARNISHAPI_1.1
        # Functions:
        #VSL_Name2Tag;
        self.lc.VSL_Name2Tag = lib.VSL_Name2Tag
        self.lc.VSL_Name2Tag.restype = c_int
        self.lc.VSL_Name2Tag.argtypes = [c_char_p, c_int]

        #LIBVARNISHAPI_1.2
        # Functions:
        #VSL_NextSLT; (undefined symbol at 4.0/4.1/5.0)
        #VSM_Error;
        self.lc.VSM_Error = lib.VSM_Error
        self.lc.VSM_Error.restype = c_char_p
        self.lc.VSM_Error.argtypes = [c_void_p]

        #VSM_Get;
        self.lc.VSM_Get = lib.VSM_Get
        self.lc.VSM_Get.argtypes = [c_void_p, c_void_p, c_char_p, c_char_p, c_char_p]

        #LIBVARNISHAPI_1.3
        #VSM_Abandoned;
        self.lc.VSM_Abandoned = lib.VSM_Abandoned
        self.lc.VSM_Abandoned.argtypes = [c_void_p]

        #VSM_ResetError;
        self.lc.VSM_ResetError = lib.VSM_ResetError
        self.lc.VSM_ResetError.argtypes = [c_void_p]

        #VSM_StillValid;
        self.lc.VSM_StillValid = lib.VSM_StillValid
        self.lc.VSM_StillValid.argtypes = [c_void_p, c_void_p]

        #VSC_Mgt;
        self.lc.VSC_Mgt = lib.VSC_Mgt
        self.lc.VSC_Mgt.restype = c_void_p
        self.lc.VSC_Mgt.argtypes = [c_void_p, c_void_p]

        #VSC_LevelDesc;
        self.lc.VSC_LevelDesc = lib.VSC_LevelDesc
        self.lc.VSC_LevelDesc.restype = c_void_p
        self.lc.VSC_LevelDesc.argtypes = [c_uint]

        #VSL_New;
        self.lc.VSL_New = lib.VSL_New
        self.lc.VSL_New.restype = c_void_p

        #VSL_Delete;
        self.lc.VSL_Delete = lib.VSL_Delete
        self.lc.VSL_Delete.argtypes = [c_void_p]

        #VSL_Error;
        self.lc.VSL_Error = lib.VSL_Error
        self.lc.VSL_Error.restype = c_char_p
        self.lc.VSL_Error.argtypes = [c_void_p]

        #VSL_ResetError;
        self.lc.VSL_ResetError = lib.VSL_ResetError
        self.lc.VSL_ResetError.argtypes = [c_void_p]

        #VSL_CursorVSM;
        self.lc.VSL_CursorVSM = lib.VSL_CursorVSM
        self.lc.VSL_CursorVSM.restype = POINTER(VSL_cursor)
        self.lc.VSL_CursorVSM.argtypes = [c_void_p, c_void_p, c_uint]

        #VSL_CursorFile;
        self.lc.VSL_CursorFile = lib.VSL_CursorFile
        self.lc.VSL_CursorFile.restype = POINTER(VSL_cursor)
        self.lc.VSL_CursorFile.argtypes = [c_void_p, c_char_p, c_uint]

        #VSL_DeleteCursor;
        self.lc.VSL_DeleteCursor = lib.VSL_DeleteCursor
        self.lc.VSL_DeleteCursor.argtypes = [c_void_p]

        #VSL_Next;
        self.lc.VSL_Next = lib.VSL_Next
        self.lc.VSL_Next.restype = c_int
        self.lc.VSL_Next.argtypes = [POINTER(VSL_cursor)]

        #VSL_Match;
        self.lc.VSL_Match = lib.VSL_Match
        self.lc.VSL_Match.restype = c_int
        self.lc.VSL_Match.argtypes = [c_void_p, POINTER(VSL_cursor)]

        #VSL_Print;
        self.lc.VSL_Print = lib.VSL_Print
        self.lc.VSL_Print.argtypes = [c_void_p, c_void_p, c_void_p]

        #VSL_PrintTerse;
        self.lc.VSL_PrintTerse = lib.VSL_PrintTerse
        self.lc.VSL_PrintTerse.argtypes = [c_void_p, c_void_p, c_void_p]

        #VSL_PrintAll;
        self.lc.VSL_PrintAll = lib.VSL_PrintAll
        self.lc.VSL_PrintAll.argtypes = [c_void_p, c_void_p, c_void_p]

        #VSL_PrintTransactions;
        self.lc.VSL_PrintTransactions = lib.VSL_PrintTransactions
        self.lc.VSL_PrintTransactions.argtypes = [c_void_p, POINTER(POINTER(VSL_transaction)), c_void_p]

        #VSL_WriteOpen;
        self.lc.VSL_WriteOpen = lib.VSL_WriteOpen
        self.lc.VSL_WriteOpen.restype = c_void_p
        self.lc.VSL_WriteOpen.argtypes = [c_void_p, c_char_p, c_int, c_int]

        #VSL_Write;
        self.lc.VSL_Write = lib.VSL_Write
        self.lc.VSL_Write.argtypes = [c_void_p, c_void_p, c_void_p]

        #VSL_WriteAll;
        self.lc.VSL_WriteAll = lib.VSL_WriteAll
        self.lc.VSL_WriteAll.argtypes = [c_void_p, c_void_p, c_void_p]

        #VSL_WriteTransactions;
        self.lc.VSL_WriteTransactions = lib.VSL_WriteTransactions
        self.lc.VSL_WriteTransactions.argtypes = [c_void_p, POINTER(POINTER(VSL_transaction)), c_void_p]

        #VSLQ_New;
        self.lc.VSLQ_New = lib.VSLQ_New
        self.lc.VSLQ_New.restype = c_void_p
        self.lc.VSLQ_New.argtypes = [c_void_p, POINTER(POINTER(VSL_cursor)), c_int, c_char_p]

        #VSLQ_Delete;
        self.lc.VSLQ_Delete = lib.VSLQ_Delete
        self.lc.VSLQ_Delete.argtypes = [POINTER(c_void_p)]

        #VSLQ_Dispatch;
        self.lc.VSLQ_Dispatch = lib.VSLQ_Dispatch
        self.lc.VSLQ_Dispatch.restype = c_int
        self.lc.VSLQ_Dispatch.argtypes = [c_void_p, VSLQ_dispatch_f, c_void_p]

        #VSLQ_Flush;
        self.lc.VSLQ_Flush = lib.VSLQ_Flush
        self.lc.VSLQ_Flush.restype = c_int
        self.lc.VSLQ_Flush.argtypes = [c_void_p, VSLQ_dispatch_f, c_void_p]

        #VSLQ_Name2Grouping;
        self.lc.VSLQ_Name2Grouping = lib.VSLQ_Name2Grouping
        self.lc.VSLQ_Name2Grouping.restype = c_int
        self.lc.VSLQ_Name2Grouping.argtypes = [c_char_p, c_int]

        #VSL_Glob2Tags;
        self.lc.VSL_Glob2Tags = lib.VSL_Glob2Tags
        self.lc.VSL_Glob2Tags.argtypes = [c_char_p, c_int, VSL_tagfind_f, c_void_p]

        #VSL_List2Tags;
        self.lc.VSL_List2Tags = lib.VSL_List2Tags
        self.lc.VSL_List2Tags.argtypes = [c_char_p, c_int, VSL_tagfind_f, c_void_p]

        #VSM_N_Arg;
        self.lc.VSM_N_Arg = lib.VSM_N_Arg
        self.lc.VSM_N_Arg.restype = c_int
        self.lc.VSM_N_Arg.argtypes = [c_void_p, c_char_p]

        #VSL_Check;
        self.lc.VSL_Check = lib.VSL_Check
        self.lc.VSL_Check.argtypes = [c_void_p, c_void_p]

        #VSL_ResetCursor;
        self.lc.VSL_ResetCursor = lib.VSL_ResetCursor
        self.lc.VSL_ResetCursor.argtypes = [c_void_p]

        ## Variables:
        #VSLQ_grouping;
        #VSL_tagflags;

        #LIBVARNISHAPI_1.4
        if self.lc.apiversion < 1.4:
            return
        #VNUM;
        #VSLQ_SetCursor;
        self.lc.VSLQ_SetCursor = lib.VSLQ_SetCursor
        self.lc.VSLQ_SetCursor.argtypes = [c_void_p, POINTER(c_void_p)]

        #VSM_IsOpen;
        self.lc.VSM_IsOpen = lib.VSM_IsOpen
        self.lc.VSM_IsOpen.argtypes = [c_void_p]

        #LIBVARNISHAPI_1.5
        if self.lc.apiversion < 1.5:
            return
        #VUT_Error;
        self.lc.VUT_Error = lib.VUT_Error
        self.lc.VUT_Error.argtypes = [c_int, c_char_p]

        #VUT_g_Arg;
        self.lc.VUT_g_Arg = lib.VUT_g_Arg
        self.lc.VUT_g_Arg.argtypes = [c_char_p]

        #VUT_Arg;
        self.lc.VUT_Arg = lib.VUT_Arg
        self.lc.VUT_Arg.argtypes = [c_int, c_char_p]

        #VUT_Setup;
        self.lc.VUT_Setup = lib.VUT_Setup

        #VUT_Init;
        self.lc.VUT_Init = lib.VUT_Init
        self.lc.VUT_Init.argtypes = [c_char_p]

        #VUT_Fini;
        self.lc.VUT_Fini = lib.VUT_Fini

        #VUT_Main;
        self.lc.VUT_Main = lib.VUT_Main

        #VUT;
        #VTIM_mono;
        self.lc.VTIM_mono = lib.VTIM_mono
        self.lc.VTIM_mono.restype = c_double

        #VTIM_real;
        self.lc.VTIM_real = lib.VTIM_real
        self.lc.VTIM_real.restype = c_double

        #VTIM_sleep;
        self.lc.VTIM_sleep = lib.VTIM_sleep
        self.lc.VTIM_sleep.argtypes = [c_double]

        #VSB_new;
        self.lc.VSB_new = lib.VSB_new
        self.lc.VSB_new.restype = c_void_p
        self.lc.VSB_new.argtypes = [c_void_p, c_char_p, c_int]

        #VSB_destroy;
        self.lc.VSB_destroy = lib.VSB_destroy
        self.lc.VSB_destroy.argtypes = [POINTER(c_void_p)]

        #VSB_error;
        self.lc.VSB_error = lib.VSB_error
        self.lc.VSB_error.argtypes = [c_void_p]

        #VSB_cat;
        self.lc.VSB_cat = lib.VSB_cat
        self.lc.VSB_cat.argtypes = [c_void_p, c_char_p]

        #VSB_putc;
        self.lc.VSB_putc = lib.VSB_putc
        self.lc.VSB_putc.argtypes = [c_void_p, c_int]

        #VSB_printf;
        self.lc.VSB_printf = lib.VSB_printf
        self.lc.VSB_printf.argtypes = [c_void_p, c_char_p]

        #VSB_clear;
        self.lc.VSB_clear = lib.VSB_clear
        self.lc.VSB_clear.argtypes = [c_void_p]

        #VSB_finish;
        self.lc.VSB_finish = lib.VSB_finish
        self.lc.VSB_finish.argtypes = [c_void_p]

        #VSB_len;
        self.lc.VSB_len = lib.VSB_len
        self.lc.VSB_len.restype = c_long
        self.lc.VSB_len.argtypes = [c_void_p]

        #VSB_data;
        self.lc.VSB_data = lib.VSB_data
        self.lc.VSB_data.restype = c_char_p
        self.lc.VSB_data.argtypes = [c_void_p]

        #VAS_Fail;
        self.lc.VAS_Fail = lib.VAS_Fail
        self.lc.VAS_Fail.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]

        #VCS_Message;
        self.lc.VCS_Message = lib.VCS_Message
        self.lc.VCS_Message.argtypes = [c_char_p]

        #LIBVARNISHAPI_1.6
        if self.lc.apiversion < 1.6:
            return

        #VTIM_format
        self.lc.VTIM_format = lib.VTIM_format
        self.lc.VTIM_format.argtypes = [c_double, c_char_p]

        #VSB_bcat
        self.lc.VSB_bcat = lib.VSB_bcat
        self.lc.VSB_bcat.restype = c_int
        self.lc.VSB_bcat.argtypes = [c_void_p, c_void_p, c_long]

        #VSB_quote
        self.lc.VSB_quote = lib.VSB_quote
        self.lc.VSB_quote.argtypes = [c_void_p, c_void_p, c_int, c_int]

        #VSB_vprintf
        self.lc.VSB_vprintf = lib.VSB_vprintf
        self.lc.VSB_vprintf.restype = c_int

        #VSB_delete
        self.lc.VSB_delete = lib.VSB_delete
        self.lc.VSB_delete.argtypes = [c_void_p]

        #VSB_indent
        self.lc.VSB_indent = lib.VSB_indent
        self.lc.VSB_indent.argtypes = [c_void_p, c_int]

        #VTIM_parse
        self.lc.VTIM_parse = lib.VTIM_parse
        self.lc.VTIM_parse.restype = c_double
        self.lc.VTIM_parse.argtypes = [c_char_p]

        #VTIM_timespec
        self.lc.VTIM_timespec = lib.VTIM_timespec
        self.lc.VTIM_timespec.restype = POINTER(timespec)
        self.lc.VTIM_timespec.argtypes = [c_double]

        #VTIM_timeval
        self.lc.VTIM_timeval = lib.VTIM_timeval
        self.lc.VTIM_timeval.restype = POINTER(timeval)
        self.lc.VTIM_timeval.argtypes = [c_double]

        #VCS_Message
        self.lc.VCS_Message = lib.VCS_Message
        self.lc.VCS_Message.argtypes = [c_char_p]

class LIBVARNISHAPI20:
    def __init__(self, lc):
        self.lc = lc
    
    def run(self, lib):
        if hasattr(lib, "VSM_Map"):
            self.lc.apiversion = 2.0

        #	# vas.c
        #		VAS_Fail;
        self.lc.VAS_Fail = lib.VAS_Fail
        self.lc.VAS_Fail.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
        
        #		VAS_Fail_Func;
        #
        #	# vcli.c
        #		VCLI_AuthResponse;
        self.lc.VCLI_AuthResponse = lib.VCLI_AuthResponse
        self.lc.VCLI_AuthResponse.argtypes = [c_int, c_char_p, c_int, c_char *65]

        #		VCLI_ReadResult;
        self.lc.VCLI_ReadResult = lib.VCLI_ReadResult
        self.lc.VCLI_ReadResult.argtypes = [c_int, POINTER(c_uint), POINTER(c_char_p), c_double]

        #		VCLI_WriteResult;
        self.lc.VCLI_WriteResult = lib.VCLI_WriteResult
        self.lc.VCLI_WriteResult.argtypes = [c_int, c_uint, c_char_p]

        #
        #	# vcs.c
        #		VCS_Message;
        self.lc.VCS_Message = lib.VCS_Message
        self.lc.VCS_Message.argtypes = [c_char_p]

        #
        #	# vsb.c
        #		VSB_bcat;
        self.lc.VSB_bcat = lib.VSB_bcat
        self.lc.VSB_bcat.argtypes = [c_void_p, c_void_p, c_long]

        #		VSB_cat;
        self.lc.VSB_cat = lib.VSB_cat
        self.lc.VSB_cat.argtypes = [c_void_p, c_char_p]

        #		VSB_clear;
        self.lc.VSB_clear = lib.VSB_clear
        self.lc.VSB_clear.argtypes = [c_void_p]

        #		VSB_data;
        self.lc.VSB_data = lib.VSB_data
        self.lc.VSB_data.restype = c_char_p
        self.lc.VSB_data.argtypes = [c_void_p]

        #		VSB_delete;
        self.lc.VSB_delete = lib.VSB_delete
        self.lc.VSB_delete.argtypes = [c_void_p]

        #		VSB_destroy;
        self.lc.VSB_destroy = lib.VSB_destroy
        self.lc.VSB_destroy.argtypes = [POINTER(c_void_p)]

        #		VSB_error;
        self.lc.VSB_error = lib.VSB_error
        self.lc.VSB_error.argtypes = [c_void_p]

        #		VSB_finish;
        self.lc.VSB_finish = lib.VSB_finish
        self.lc.VSB_finish.argtypes = [c_void_p]

        #		VSB_indent;
        self.lc.VSB_indent = lib.VSB_indent
        self.lc.VSB_indent.argtypes = [c_void_p, c_int]

        #		VSB_len;
        self.lc.VSB_len = lib.VSB_len
        self.lc.VSB_len.restype = c_long
        self.lc.VSB_len.argtypes = [c_void_p]

        #		VSB_new;
        self.lc.VSB_new = lib.VSB_new
        self.lc.VSB_new.restype = c_void_p
        self.lc.VSB_new.argtypes = [c_void_p, c_char_p, c_int]

        #		VSB_printf;
        self.lc.VSB_printf = lib.VSB_printf

        #		VSB_putc;
        self.lc.VSB_putc = lib.VSB_putc
        self.lc.VSB_putc.argtypes = [c_void_p, c_int]

        #		VSB_quote;
        self.lc.VSB_quote = lib.VSB_quote
        self.lc.VSB_quote.argtypes = [c_void_p, c_void_p, c_int, c_int]

        #		VSB_quote_pfx;
        self.lc.VSB_quote_pfx = lib.VSB_quote_pfx
        self.lc.VSB_quote_pfx.argtypes = [c_void_p, c_char_p, c_void_p, c_int, c_int]

        #		VSB_vprintf;
        self.lc.VSB_vprintf = lib.VSB_vprintf

        ####################################################
        #
        #	# vsc.c
        #		VSC_Arg;
        self.lc.VSC_Arg = lib.VSC_Arg
        self.lc.VSC_Arg.argtypes = [c_void_p, c_int, c_char_p]

        #		VSC_ChangeLevel;
        self.lc.VSC_ChangeLevel = lib.VSC_ChangeLevel
        self.lc.VSC_ChangeLevel.restype = POINTER(VSC_level_desc)
        self.lc.VSC_ChangeLevel.argtypes = [POINTER(VSC_level_desc), c_int]

        #		VSC_Destroy;
        self.lc.VSC_Destroy = lib.VSC_Destroy
        self.lc.VSC_Destroy.argtypes = [POINTER(c_void_p), c_void_p]

        #		VSC_Iter;
        self.lc.VSC_Iter = lib.VSC_Iter
        self.lc.VSC_Iter.argtypes = [c_void_p, c_void_p, VSC_iter_f20, c_void_p]

        #		VSC_New;
        self.lc.VSC_New = lib.VSC_New
        self.lc.VSC_New.restype = c_void_p

        #		VSC_State;
        self.lc.VSC_State = lib.VSC_State
        self.lc.VSC_State.argtypes = [c_void_p, VSC_new_f, VSC_destroy_f, c_void_p]

        #
        #	# vsl*.c
        #		VSLQ_Delete;
        self.lc.VSLQ_Delete = lib.VSLQ_Delete
        self.lc.VSLQ_Delete.argtypes = [POINTER(c_void_p)]

        #		VSLQ_Dispatch;
        self.lc.VSLQ_Dispatch = lib.VSLQ_Dispatch
        self.lc.VSLQ_Dispatch.argtypes = [c_void_p, VSLQ_dispatch_f, c_void_p]

        #		VSLQ_Flush;
        self.lc.VSLQ_Flush = lib.VSLQ_Flush
        self.lc.VSLQ_Flush.argtypes = [c_void_p, VSLQ_dispatch_f, c_void_p]

        #		VSLQ_Name2Grouping;
        self.lc.VSLQ_Name2Grouping = lib.VSLQ_Name2Grouping
        self.lc.VSLQ_Name2Grouping.argtypes = [c_char_p, c_int]

        #		VSLQ_New;
        self.lc.VSLQ_New = lib.VSLQ_New
        self.lc.VSLQ_New.restype = c_void_p
        self.lc.VSLQ_New.argtypes = [c_void_p, POINTER(POINTER(VSL_cursor)), c_int, c_char_p]

        #		VSLQ_SetCursor;
        self.lc.VSLQ_SetCursor = lib.VSLQ_SetCursor
        self.lc.VSLQ_SetCursor.argtypes = [c_void_p, POINTER(c_void_p)]

        #		VSLQ_grouping; (variables)
        #		VSL_Arg;
        self.lc.VSL_Arg = lib.VSL_Arg
        self.lc.VSL_Arg.argtypes = [c_void_p, c_int, c_char_p]

        #		VSL_Check;
        self.lc.VSL_Check = lib.VSL_Check
        self.lc.VSL_Check.argtypes = [c_void_p, c_void_p]

        #		VSL_CursorFile;
        self.lc.VSL_CursorFile = lib.VSL_CursorFile
        self.lc.VSL_CursorFile.restype = POINTER(VSL_cursor)
        self.lc.VSL_CursorFile.argtypes = [c_void_p, c_char_p, c_uint]

        #		VSL_CursorVSM;
        self.lc.VSL_CursorVSM = lib.VSL_CursorVSM
        self.lc.VSL_CursorVSM.restype = POINTER(VSL_cursor)
        self.lc.VSL_CursorVSM.argtypes = [c_void_p, c_void_p, c_uint]

        #		VSL_Delete;
        self.lc.VSL_Delete = lib.VSL_Delete
        self.lc.VSL_Delete.argtypes = [c_void_p]

        #		VSL_DeleteCursor;
        self.lc.VSL_DeleteCursor = lib.VSL_DeleteCursor
        self.lc.VSL_DeleteCursor.argtypes = [c_void_p]

        #		VSL_Error;
        self.lc.VSL_Error = lib.VSL_Error
        self.lc.VSL_Error.restype = c_char_p
        self.lc.VSL_Error.argtypes = [c_void_p]

        #		VSL_Glob2Tags;
        self.lc.VSL_Glob2Tags = lib.VSL_Glob2Tags
        self.lc.VSL_Glob2Tags.argtypes = [c_char_p, c_int, VSL_tagfind_f, c_void_p]

        #		VSL_List2Tags;
        self.lc.VSL_List2Tags = lib.VSL_List2Tags
        self.lc.VSL_List2Tags.argtypes = [c_char_p, c_int, VSL_tagfind_f, c_void_p]

        #		VSL_Match;
        self.lc.VSL_Match = lib.VSL_Match
        self.lc.VSL_Match.argtypes = [c_void_p, POINTER(VSL_cursor)]

        #		VSL_Name2Tag;
        self.lc.VSL_Name2Tag = lib.VSL_Name2Tag
        self.lc.VSL_Name2Tag.argtypes = [c_char_p, c_int]

        #		VSL_New;
        self.lc.VSL_New = lib.VSL_New
        self.lc.VSL_New.restype = c_void_p

        #		VSL_Next;
        self.lc.VSL_Next = lib.VSL_Next
        self.lc.VSL_Next.argtypes = [POINTER(VSL_cursor)]

        #		VSL_Print;
        self.lc.VSL_Print = lib.VSL_Print
        self.lc.VSL_Print.argtypes = [c_void_p, c_void_p, c_void_p]

        #		VSL_PrintAll;
        self.lc.VSL_PrintAll = lib.VSL_PrintAll
        self.lc.VSL_PrintAll.argtypes = [c_void_p, c_void_p, c_void_p]

        #		VSL_PrintTerse;
        self.lc.VSL_PrintTerse = lib.VSL_PrintTerse
        self.lc.VSL_PrintTerse.argtypes = [c_void_p, c_void_p, c_void_p]

        #		VSL_PrintTransactions;
        self.lc.VSL_PrintTransactions = lib.VSL_PrintTransactions
        self.lc.VSL_PrintTransactions.argtypes = [c_void_p, POINTER(POINTER(VSL_transaction)), c_void_p]

        #		VSL_ResetCursor;
        self.lc.VSL_ResetCursor = lib.VSL_ResetCursor
        self.lc.VSL_ResetCursor.argtypes = [c_void_p]

        #		VSL_ResetError;
        self.lc.VSL_ResetError = lib.VSL_ResetError
        self.lc.VSL_ResetError.argtypes = [c_void_p]

        #		VSL_Write;
        self.lc.VSL_Write = lib.VSL_Write
        self.lc.VSL_Write.argtypes = [c_void_p, c_void_p, c_void_p]

        #		VSL_WriteAll;
        self.lc.VSL_WriteAll = lib.VSL_WriteAll
        self.lc.VSL_WriteAll.argtypes = [c_void_p, c_void_p, c_void_p]

        #		VSL_WriteOpen;
        self.lc.VSL_WriteOpen = lib.VSL_WriteOpen
        self.lc.VSL_WriteOpen.restype = c_void_p
        self.lc.VSL_WriteOpen.argtypes = [c_void_p, c_char_p, c_int, c_int]

        #		VSL_WriteTransactions;
        self.lc.VSL_WriteTransactions = lib.VSL_WriteTransactions
        self.lc.VSL_WriteTransactions.argtypes = [c_void_p, POINTER(POINTER(VSL_transaction)), c_void_p]

        #		VSL_tagflags; (variables)
        #		VSL_tags; (variables)
        #
        #	# vsm.c
        #		VSM_Arg;
        self.lc.VSM_Arg = lib.VSM_Arg
        self.lc.VSM_Arg.argtypes = [c_void_p, c_char, c_char_p]

        #		VSM_Attach;
        self.lc.VSM_Attach = lib.VSM_Attach
        self.lc.VSM_Attach.argtypes = [c_void_p, c_int]

        #		VSM_Destroy;
        self.lc.VSM_Destroy = lib.VSM_Destroy
        self.lc.VSM_Destroy.argtypes = [POINTER(c_void_p)]

        #		VSM_Dup;
        self.lc.VSM_Dup = lib.VSM_Dup
        self.lc.VSM_Dup.argtypes = [c_void_p, c_char_p, c_char_p]

        #		VSM_Error;
        self.lc.VSM_Error = lib.VSM_Error
        self.lc.VSM_Error.restype = c_char_p
        self.lc.VSM_Error.argtypes = [c_void_p]

        #		VSM_Get;
        self.lc.VSM_Get = lib.VSM_Get
        self.lc.VSM_Get.argtypes = [c_void_p, POINTER(VSM_fantom), c_char_p, c_char_p]

        #		VSM_Map;
        self.lc.VSM_Map = lib.VSM_Map
        self.lc.VSM_Map.argtypes = [c_void_p, POINTER(VSM_fantom)]

        #		VSM_New;
        self.lc.VSM_New = lib.VSM_New
        self.lc.VSM_New.restype = c_void_p

        #		VSM_ResetError;
        self.lc.VSM_ResetError = lib.VSM_ResetError
        self.lc.VSM_ResetError.argtypes = [c_void_p]

        #		VSM_Status;
        self.lc.VSM_Status = lib.VSM_Status
        self.lc.VSM_Status.restype = c_uint
        self.lc.VSM_Status.argtypes = [c_void_p]

        #		VSM_StillValid;
        self.lc.VSM_StillValid = lib.VSM_StillValid
        self.lc.VSM_StillValid.restype = c_void_p
        self.lc.VSM_StillValid.argtypes = [c_void_p, POINTER(VSM_fantom)]

        #		VSM_Unmap;
        self.lc.VSM_Unmap = lib.VSM_Unmap
        self.lc.VSM_Unmap.argtypes = [c_void_p, POINTER(VSM_fantom)]

        #		VSM__iter0;
        self.lc.VSM__iter0 = lib.VSM__iter0
        self.lc.VSM__iter0.argtypes = [c_void_p, POINTER(VSM_fantom)]

        #		VSM__itern;
        self.lc.VSM__itern = lib.VSM__itern
        self.lc.VSM__itern.argtypes = [c_void_p, POINTER(VSM_fantom)]

        #		VSM_invalid; (valiabls)
        #		VSM_valid; (valiables)
        #
        #	# vtim.c
        #		VTIM_format;
        self.lc.VTIM_format = lib.VTIM_format
        self.lc.VTIM_format.argtypes = [c_double, c_char_p]

        #		VTIM_mono;
        self.lc.VTIM_mono = lib.VTIM_mono
        self.lc.VTIM_mono.restype = c_double

        #		VTIM_parse;
        self.lc.VTIM_parse = lib.VTIM_parse
        self.lc.VTIM_parse.restype = c_double
        self.lc.VTIM_parse.argtypes = [c_char_p]

        #		VTIM_real;
        self.lc.VTIM_real = lib.VTIM_real
        self.lc.VTIM_real.restype = c_double

        #		VTIM_sleep;
        self.lc.VTIM_sleep = lib.VTIM_sleep
        self.lc.VTIM_sleep.argtypes = [c_double]

        #		VTIM_timespec;
        self.lc.VTIM_timespec = lib.VTIM_timespec
        self.lc.VTIM_timespec.restype = POINTER(timespec)
        self.lc.VTIM_timespec.argtypes = [c_double]

        #		VTIM_timeval;
        self.lc.VTIM_timeval = lib.VTIM_timeval
        self.lc.VTIM_timeval.restype = POINTER(timeval)
        self.lc.VTIM_timeval.argtypes = [c_double]

        #
        #	# vut.c
        #		VUT_Arg;
        self.lc.VUT_Arg = lib.VUT_Arg
        self.lc.VUT_Arg.argtypes = [POINTER(VUT), c_int, c_char_p]

        #		VUT_Error;
        self.lc.VUT_Error = lib.VUT_Error

        #		VUT_Fini;
        self.lc.VUT_Fini = lib.VUT_Fini
        self.lc.VUT_Fini.argtypes = [POINTER(POINTER(VUT))]

        #		VUT_Init;
        self.lc.VUT_Init = lib.VUT_Init
        self.lc.VUT_Init.restype = POINTER(VUT)
        self.lc.VUT_Init.argtypes = [c_char_p, c_int, POINTER(c_char_p), POINTER(vopt_spec)]

        #		VUT_Main;
        self.lc.VUT_Main = lib.VUT_Main
        self.lc.VUT_Main.argtypes = [POINTER(VUT)]

        #		VUT_Setup;
        self.lc.VUT_Setup = lib.VUT_Setup
        self.lc.VUT_Setup.argtypes = [POINTER(VUT)]

        #		VUT_Signal;
        self.lc.VUT_Signal = lib.VUT_Signal
        self.lc.VUT_Signal.argtypes = [VUT_sighandler_f]

        #		VUT_Signaled;
        self.lc.VUT_Signaled = lib.VUT_Signaled
        self.lc.VUT_Signaled.argtypes = [POINTER(VUT), c_int]

class LIBVARNISHAPI:
    def __init__(self, lib):
        #Check libvarnishapi version
        if hasattr(lib, "VSM_Map"):
            LIBVARNISHAPI20(self).run(lib)
        else:
            LIBVARNISHAPI10(self).run(lib)

class VSLUtil:

    def tag2Var(self, tag, data):
        ret = {'key': '', 'val': '', 'vkey': ''}
        if tag not in self.__tags:
            return ret

        r = self.__tags[tag]
        ret['vkey'] = r.split(' ', 1)[-1].split('.', 1)[0]
        if r == '':
            return ret
        elif r[-1:] == '.':
            spl = data.split(': ', 1)
            ret['key'] = r + spl[0].rstrip(': ')
            ret['val'] = ''
            if len(spl) > 1:
                ret['val'] = spl[1]
        else:
            ret['key'] = r
            ret['val'] = data
        return (ret)

    def tag2VarName(self, tag, data):
        return self.tag2Var(tag, data)['key']

    __tags = {
        'Debug': '',
        'Error': '',
        'CLI': '',
        'SessOpen': '',
        'SessClose': '',
        'BackendOpen': '',  # Change key count at varnish41(4->6)
        'BackendStart': '', # 4.1.3~
        'BackendReuse': '',
        'BackendClose': '',
        'HttpGarbage': '',
        'Backend': '',
        'Length': '',
        'FetchError': '',
        'BogoHeader': '',
        'LostHeader': '',
        'TTL': '',
        'Fetch_Body': '',
        'VCL_acl': '',
        'VCL_call': '',
        'VCL_trace': '',
        'VCL_return': '',
        'ReqStart': 'client.ip',
        'Hit': '',
        'HitPass': '',
        'HitMiss': '',
        'ExpBan': '',
        'ExpKill': '',
        'WorkThread': '',
        'ESI_xmlerror': '',
        'Hash': '',  # Change log data type(str->bin)
        'Backend_health': '',
        'VCL_Log': '',
        'VCL_Error': '',
        'Gzip': '',
        'Link': '',
        'Begin': '',
        'End': '',
        'VSL': '',
        'Storage': '',
        'Timestamp': '',
        'ReqAcct': '',
        'ESI_BodyBytes': '',  # Only Varnish40X
        'PipeAcct': '',
        'BereqAcct': '',
        'ReqMethod': 'req.method',
        'ReqURL': 'req.url',
        'ReqProtocol': 'req.proto',
        'ReqStatus': '',
        'ReqReason': '',
        'ReqHeader': 'req.http.',
        'ReqUnset': 'unset req.http.',
        'ReqLost': '',
        'RespMethod': '',
        'RespURL': '',
        'RespProtocol': 'resp.proto',
        'RespStatus': 'resp.status',
        'RespReason': 'resp.reason',
        'RespHeader': 'resp.http.',
        'RespUnset': 'unset resp.http.',
        'RespLost': '',
        'BereqMethod': 'bereq.method',
        'BereqURL': 'bereq.url',
        'BereqProtocol': 'bereq.proto',
        'BereqStatus': '',
        'BereqReason': '',
        'BereqHeader': 'bereq.http.',
        'BereqUnset': 'unset bereq.http.',
        'BereqLost': '',
        'BerespMethod': '',
        'BerespURL': '',
        'BerespProtocol': 'beresp.proto',
        'BerespStatus': 'beresp.status',
        'BerespReason': 'beresp.reason',
        'BerespHeader':   'beresp.http.',
        'BerespUnset':    'unset beresp.http.',
        'BerespLost':     '',
        'ObjMethod':      '',
        'ObjURL':         '',
        'ObjProtocol':    'obj.proto',
        'ObjStatus': 'obj.status',
        'ObjReason': 'obj.reason',
        'ObjHeader': 'obj.http.',
        'ObjUnset':     'unset obj.http.',
        'ObjLost':      '',
        'Proxy':        '',  # Only Varnish41x
        'ProxyGarbage': '',  # Only Varnish41x
        'VfpAcct':      '',  # Only Varnish41x
        'Witness':      '',  # Only Varnish41x
        'H2RxHdr':   '',  # Only Varnish50x
        'H2RxBody':  '',  # Only Varnish50x
        'H2TxHdr':   '',  # Only Varnish50x
        'H2TxBody':  '',  # Only Varnish50x
    }


class VarnishAPI:

    def __init__(self, sopath='libvarnishapi.so.1'):
        self.lib = cdll[sopath]
        self.lva = LIBVARNISHAPI(self.lib)
        self.defi = VarnishAPIDefine40()
        self._cb = None
        self.vsm = self.lva.VSM_New()
        self.d_opt = 0

        VSLTAGS = c_char_p * 256
        self.VSL_tags = []
        self.VSL_tags_rev = {}
        tmp = VSLTAGS.in_dll(self.lib, "VSL_tags")
        for i in range(0, 255):
            if tmp[i] is None:
                self.VSL_tags.append(None)
            else:
                key = tmp[i].decode("utf8", "replace")
                self.VSL_tags.append(key)
                self.VSL_tags_rev[key] = i

        VSLTAGFLAGS = c_uint * 256
        self.VSL_tagflags = []
        tmp = VSLTAGFLAGS.in_dll(self.lib, "VSL_tagflags")
        for i in range(0, 255):
            self.VSL_tagflags.append(tmp[i])

        VSLQGROUPING = c_char_p * 4
        self.VSLQ_grouping = []
        tmp = VSLQGROUPING.in_dll(self.lib, "VSLQ_grouping")
        for i in range(0, 3):
            self.VSLQ_grouping.append(tmp[i])

        self.error = ''

    def VSL_TAG(self, ptr):
        tag = ptr[0] >> 24
        return tag

    def VSL_DATA(self, ptr, isbin=False):
        length = ptr[0] & 0xffff
        if isbin:
            data = string_at(ptr, length + 8)[8:]
        else:
            data = string_at(ptr, length + 8)[8:-1].decode("utf8", "replace")
        return data

    def ArgDefault(self, op, arg):
        if self.lva.apiversion >= 2.0:
            if op == "n":
                # Set Varnish instance name.
                i = self.lva.VSM_Arg(self.vsm, 'n', arg)
                if i <= 0:
                    self.error = "%s" % self.lva.VSM_Error(self.vsm).rstrip()
                    return(i)
            elif op == "N":
                pass
        else:
            if op == "n":
                # Set Varnish instance name.
                i = self.lva.VSM_n_Arg(self.vsm, arg)
                if i <= 0:
                    self.error = "%s" % self.lva.VSM_Error(self.vsm).rstrip()
                    return(i)
            elif op == "N":
                # Set VSM file.
                i = self.lva.VSM_N_Arg(self.vsm, arg)
                if i <= 0:
                    self.error = "%s" % self.lva.VSM_Error(self.vsm).rstrip()
                    return(i)
                self.d_opt = 1
        return(None)

    def Fini(self):
        if self.vsm:
            if self.lva.apiversion >= 2.0:
                self.lva.VSM_Destroy(byref(cast(self.vsm, c_void_p)))
            else:
                self.lva.VSM_Delete(self.vsm)
                self.vsm = 0


class VarnishStat(VarnishAPI):

    def __init__(self, opt='', sopath='libvarnishapi.so.1'):
        VarnishAPI.__init__(self, sopath)
        self.name = ''
        if len(opt) > 0:
            self.__setArg(opt)

        if self.lva.apiversion >= 2.0:
            self.vsc = self.lva.VSC_New();
            self.__Setup20()
        else:
            self.__Setup10()

    def Fini(self):
        if self.lva.apiversion >= 2.0:
            self.lva.VSC_Destroy(byref(cast(self.vsc, c_void_p)), self.vsm)
        VarnishAPI.Fini(self)

    def __Setup20(self):
        if self.lva.VSM_Attach(self.vsm, 2):
            self.error = "VSM: %s" % self.lva.VSM_Error(
                self.vsm).decode("utf8", "replace").rstrip()
            return(0)

    def __Setup10(self):
        if self.lva.VSM_Open(self.vsm):
            self.error = "Can't open VSM file (%s)" % self.lva.VSM_Error(
                self.vsm).rstrip()
        else:
            self.name = self.lva.VSM_Name(self.vsm)

    def __setArg(self, opt):
        opts, args = getopt.getopt(opt, "N:n:")
        error = 0
        for o in opts:
            op = o[0].lstrip('-')
            arg = o[1]
            self.__Arg(op, arg.encode("utf8", "replace"))

        if error:
            self.error = error
            return(0)
        return(1)

    def __Arg(self, op, arg):
        # default
        i = VarnishAPI.ArgDefault(self, op, arg)
        if i is not None:
            return(i)

    def _getstat10(self, priv, pt):
        if not bool(pt):
            return(0)
        val = pt[0].ptr[0]

        sec = pt[0].section
        key = ''

        type = sec[0].fantom[0].type.decode("utf8", "replace")
        ident = sec[0].fantom[0].ident.decode("utf8", "replace")
        if type != '':
            key += type + '.'
        if ident != '':
            key += ident + '.'
        key += pt[0].desc[0].name.decode("utf8", "replace")

        self._buf[key] = {'val': val, 'desc': pt[0].desc[0].sdesc.decode("utf8", "replace")}

        return(0)

    def _getstat20(self, priv, pt):
        if not bool(pt):
            return(0)
        val = pt[0].ptr[0]
        key = pt[0].name.decode("utf8", "replace")
        self._buf[key] = {'val': val, 'desc': pt[0].sdesc.decode("utf8", "replace")}

        return(0)

    def getStats(self):
        self._buf = {}
        if self.lva.apiversion >= 2.0:
            self.lva.VSC_Iter(self.vsc, self.vsm, VSC_iter_f20(self._getstat20), None)
        else:
            self.lva.VSC_Iter(self.vsm, None, VSC_iter_f(self._getstat10), None)
        return self._buf


class VarnishLog(VarnishAPI):

    def __init__(self, opt='', sopath='libvarnishapi.so.1', dataDecode=True):
        VarnishAPI.__init__(self, sopath)

        self.vut = VSLUtil()
        self.vsl = self.lva.VSL_New()
        self.vslq = None
        self.__g_arg = 0
        self.__q_arg = None
        self.__r_arg = 0
        self.name = ''
        self.dataDecode = dataDecode

        if len(opt) > 0:
            self.__setArg(opt)
            
        if self.lva.apiversion >= 2.0:
            self.__Setup20()
        else:
            self.__Setup10()


    def __setArg(self, opt):
        opts, args = getopt.getopt(opt, "bcCdx:X:r:q:N:n:I:i:g:")
        error = 0
        for o in opts:
            op = o[0].lstrip('-')
            arg = o[1]
            self.__Arg(op, arg.encode("utf8", "replace"))

        # Check
        if self.__r_arg and self.vsm:
            error = "Can't have both -n and -r options"

        if error:
            self.error = error
            return(0)
        return(1)

    def __Arg(self, op, arg):
        i = VarnishAPI.ArgDefault(self, op, arg)
        if i is not None:
            return(i)

        if op == "d":
            # Set log cursor at the head.
            self.d_opt = 1
        elif op == "g":
            # Specify the grouping.
            self.__g_arg = self.__VSLQ_Name2Grouping(arg)
            if self.__g_arg == -2:
                self.error = "Ambiguous grouping type: %s" % (arg)
                return(self.__g_arg)
            elif self.__g_arg < 0:
                self.error = "Unknown grouping type: %s" % (arg)
                return(self.__g_arg)
        # elif op == "P":
        # Not support PID(-P) option.
        elif op == "q":
            # VSL-query
            self.__q_arg = arg
        elif op == "r":
            # Read log from the binary file.
            self.__r_arg = arg
        else:
            # default
            i = self.__VSL_Arg(op, arg)
            if i < 0:
                self.error = "%s" % self.lva.VSL_Error(self.vsl).decode("utf8", "replace")
            return(i)

    def __Setup20(self):
        self.hascursor = -1
        # query
        self.vslq = self.lva.VSLQ_New(self.vsl, None, self.__g_arg, self.__q_arg)
        if not self.vslq:
            self.error = "Query expression error:\n%s" % self.lva.VSL_Error(
                self.vsl).decode("utf8", "replace")
            return(0)

        if self.__r_arg:
            c = self.lva.VSL_CursorFile(self.vsl, self.__r_arg, 0)
            #self.lva.VSLQ_SetCursor(VUT.vslq, POINTER(c))
        else:
            
            if self.lva.VSM_Attach(self.vsm, 2):
                self.error = "VSM: %s" % self.lva.VSM_Error(
                    self.vsm).decode("utf8", "replace").rstrip()
                return(0)
            #self.name = self.lva.VSM_Name(self.vsm)

            if self.d_opt:
                self.cursor_opt = self.defi.VSL_COPT_TAILSTOP | self.defi.VSL_COPT_BATCH
            else:
                self.cursor_opt = self.defi.VSL_COPT_TAIL | self.defi.VSL_COPT_BATCH

            c = self.lva.VSL_CursorVSM(
                self.vsl, self.vsm, self.cursor_opt)
                
            self.lva.VSLQ_SetCursor(self.vslq, byref(cast(c, c_void_p)))
            self.lva.VSL_ResetError(self.vsl)

        if not c:
            self.error = "Can't open log (%s)" % self.lva.VSL_Error(self.vsl).decode("utf8", "replace")
            return(0)

        return(1)

    def __Setup10(self):
        if self.__r_arg:
            c = self.lva.VSL_CursorFile(self.vsl, self.__r_arg, 0)
        else:
            if self.lva.VSM_Open(self.vsm):
                self.error = "Can't open VSM file (%s)" % self.lva.VSM_Error(
                    self.vsm).decode("utf8", "replace").rstrip()
                return(0)
            self.name = self.lva.VSM_Name(self.vsm)

            if self.d_opt:
                tail = self.defi.VSL_COPT_TAILSTOP
            else:
                tail = self.defi.VSL_COPT_TAIL

            c = self.lva.VSL_CursorVSM(
                self.vsl, self.vsm, tail | self.defi.VSL_COPT_BATCH)

        if not c:
            self.error = "Can't open log (%s)" % self.lva.VSL_Error(self.vsl).decode("utf8", "replace")
            return(0)
        # query
        self.vslq = self.lva.VSLQ_New(self.vsl, c, self.__g_arg, self.__q_arg)
        if not self.vslq:
            self.error = "Query expression error:\n%s" % self.lva.VSL_Error(
                self.vsl).decode("utf8", "replace")
            return(0)

        return(1)


    def __Dispatch10(self, maxread):
        while True:
            if not self.vslq:
                # Reconnect VSM
                time.sleep(0.1)
                if self.lva.VSM_Open(self.vsm):
                    self.lva.VSM_ResetError(self.vsm)
                    return(1)
                c = self.lva.VSL_CursorVSM(
                    self.vsl, self.vsm,
                    self.defi.VSL_COPT_TAIL | self.defi.VSL_COPT_BATCH)
                if not c:
                    self.lva.VSM_ResetError(self.vsm)
                    self.lva.VSM_Close(self.vsm)
                    return(1)
                self.vslq = self.lva.VSLQ_New(
                    self.vsl, c, self.__g_arg, self.__q_arg)
                self.error = 'Log reacquired'

            i = self.lva.VSLQ_Dispatch(
                self.vslq, VSLQ_dispatch_f(self._callBack), None)

            if i == 1 and maxread != 1:
               if maxread > 1:
                   maxread-=1
               continue
            elif i > -2:
                return i
            if not self.vsm:
                return i

            self.lva.VSLQ_Flush(self.vslq, VSLQ_dispatch_f(self._callBack), None)
            self.lva.VSLQ_Delete(byref(cast(self.vslq, c_void_p)))
            self.vslq = None
            if i == -2:
                self.error = "Log abandoned"
                #self.lva.VSM_Destroy(POINTER(self.vsm))
                self.lva.VSM_Close(self.vsm)
            if i < -2:
                self.error = "Log overrun"
            return i

    def __Dispatch20(self, maxread):
        while True:
            if self.vsm:
                stat = self.lva.VSM_Status(self.vsm)
                if stat & self.defi.VSM_WRK_RESTARTED:
                    if self.hascursor < 1:
                        self.error = "Log abandoned"
                        self.lva.VSLQ_SetCursor(self.vslq, None)
                        self.hascursor = 0
                if self.hascursor < 1:
                    time.sleep(0.1)
                    c = self.lva.VSL_CursorVSM(self.vsl, self.vsm, self.cursor_opt)
                    if c == None:
                        self.lva.VSL_ResetError(self.vsl)
                        return 0
                    if self.hascursor == 0:
                        self.error = "Log reacquired"
                    self.hascursor = 1
                    self.lva.VSLQ_SetCursor(self.vslq, byref(cast(c, c_void_p)))
            
            i = self.lva.VSLQ_Dispatch(
                self.vslq, VSLQ_dispatch_f(self._callBack), None)

            if i == 1 and maxread != 1:
                if maxread > 1:
                    maxread-=1
                continue
            elif i > -2:
                return i
            if not self.vsm:
                return i

            self.lva.VSLQ_Flush(self.vslq, VSLQ_dispatch_f(self._callBack), None)
            if i == -2:
                self.error = "Log abandoned"
                self.hascursor = 0
                self.lva.VSLQ_SetCursor(self.vslq, None)
            if i < -2:
                self.error = "Log overrun"
            return i

    def Dispatch(self, cb=None, priv=None, maxread=1, vxidcb=None, groupcb=None):
        self._cb = cb
        self._vxidcb = vxidcb
        self._groupcb = groupcb
        self._priv = priv
        if self.lva.apiversion >= 2.0:
            return self.__Dispatch20(maxread)
        else:
            return self.__Dispatch10(maxread)

    def Fini(self):
        if self.vslq:
            self.lva.VSLQ_Delete(byref(cast(self.vslq, c_void_p)))
            self.vslq = 0
        if self.vsl:
            self.lva.VSL_Delete(self.vsl)
            self.vsl = 0
        VarnishAPI.Fini(self)

    def __VSL_Arg(self, opt, arg='\0'):
        return self.lva.VSL_Arg(self.vsl, ord(opt), arg)

    def __VSLQ_Name2Grouping(self, arg):
        return self.lva.VSLQ_Name2Grouping(arg, -1)

    def _callBack(self, vsl, pt, fo):
        idx = -1
        while 1:
            idx += 1
            t = pt[idx]
            if not bool(t):
                break

            tra = t[0]
            cbd = {
                'level': tra.level,
                'vxid': tra.vxid,
                'vxid_parent': tra.vxid_parent,
                'reason': tra.reason,
                'type': None,
                'transaction_type': tra.type,
            }
            while 1:
                i = self.lva.VSL_Next(tra.c)
                if i < 0:
                    return (i)
                if i == 0:
                    break
                if not self.lva.VSL_Match(self.vsl, tra.c):
                    continue

                # decode length tag type(thread)...
                ptr = tra.c[0].rec.ptr
                cbd['length'] = ptr[0] & 0xffff
                cbd['tag'] = self.VSL_TAG(ptr)
                if cbd['type'] is None:
                    if ptr[1] & 0x40000000: #1<<30
                        cbd['type'] = 'c'
                    elif ptr[1] & 0x80000000: #1<<31
                        cbd['type'] = 'b'
                    else:
                        cbd['type'] = '-'
                cbd['isbin'] = self.VSL_tagflags[cbd['tag']] & self.defi.SLT_F_BINARY
                isbin = cbd['isbin'] == self.defi.SLT_F_BINARY or not self.dataDecode
                cbd['data'] = self.VSL_DATA(ptr, isbin)

                if self._cb is not None:
                    self._cb(self, cbd, self._priv)
            if self._vxidcb is not None:
                self._vxidcb(self, self._priv)

        if self._groupcb:
            self._groupcb(self, self._priv)

        return(0)
