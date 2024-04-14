from .confirmdialog import confirm
from .confirmdialog import ConfirmDialog
from .twooptiondialog import two_option_dialog
from .twooptsdlgcustom import two_option_dialog_custom
from .timeddialog import timed_dialog

styleoptions = {
    'dialog_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (400, 300), #(350,250)
        'size': (400, 300),
        'logo_title': u'Warning !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Serial check failed.\nNo serial port connected."
    },
    'exit_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (450, 350),
        'size': (450, 350),
        'logo_title': u'Warning !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Are you sure you want to exit?"
    },
    'serial_err_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'Serial Error !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "No Serial Connection\nCheck serial port connection"
    },
    'patient_num_reminder_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'Warning !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Please select Patient number first!"
    },
    'patient_num_repeated_err_window': {
        'title': u'Warning',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (380, 280),
        'size': (380, 280),
        'logo_title': u'Warning !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Patient number already exists.\nContinue?",
        'true_btn': {
            'text': "Accept and Continue",
            'size': (200,40)
        },
        'false_btn': {
            'text': "Go Back",
            'size': (100,40)
        },
    },
    'timeout_err_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'Serial Error !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Timeout waiting for Serial Data\nCheck serial port connection"
    },
    'stop_recording_window': {
        'title': u'Notification',
        'windowicon': "../logo/care-favicon.png",
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'Warning !',
        'logo_img_url': "../skin/images/ov-orange-green.png",
        'sub_title': "Are you sure you want to stop recording?"
    },
}