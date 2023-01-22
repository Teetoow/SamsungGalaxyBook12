#
#    extractVerb.py            (C) 2022-2023, Aurélien Croc (AP²C)
#
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#  
#  You should have received a copy of the GNU General Public License along with
#  this program; If not, see <http://www.gnu.org/licenses/>.

names = {
    "701": "set_connect_sel",
    "703": "set_proc_state",
    "704": "set_sdi_select",
    "705": "set_power_state",
    "706": "set_channel_streamid",
    "707": "set_pin_widget_control",
    "708": "set_unsolicited_enable",
    "709": "set_pin_sense",
    "70a": "set_beep_control",
    "70c": "set_eapd_btlenable",
    "70d": "set_digi_convert_1",
    "70e": "set_digi_convert_2",
    "73e": "set_digi_convert_3",
    "70f": "set_volume_knob_control",
    "715": "set_gpio_data",
    "716": "set_gpio_mask",
    "717": "set_gpio_direction",
    "718": "set_gpio_wake_mask",
    "719": "set_gpio_unsolicited_rsp_mask",
    "71a": "set_gpio_sticky_mask",
    "71c": "set_config_default_bytes_0",
    "71d": "set_config_default_bytes_1",
    "71e": "set_config_default_bytes_2",
    "71f": "set_config_default_bytes_3",
    "788": "set_eapd",
    "7ff": "set_codec_reset",
    "724": "set_stripe_control",
    "72d": "set_cvt_chan_count",
    "730": "set_hdmi_dip_index",
    "731": "set_hdmi_dip_data",
    "732": "set_hdmi_dip_xmit",
    "733": "set_hdmi_cp_ctrl",
    "734": "set_hdmi_chan_slot",
    "735": "set_device_sel",
    "f00": "get_parameters",
    "f01": "get_connect_sel",
    "f02": "get_connect_list",
    "f03": "get_proc_state",
    "f04": "get_sdi_select",
    "f05": "get_power_state",
    "f06": "get_channel_streamid",
    "f07": "get_pin_ctl",
    "f08": "get_unsolicited_response",
    "f09": "get_pin_sense",
    "f0a": "get_beep_control",
    "f0c": "get_eapd_btl",
    "f0d": "get_digi_convert_1",
    "f0e": "get_digi_convert_2",
    "f0f": "get_volume_knob_control",
    "f15": "get_gpio_data",
    "f16": "get_gpio_mask",
    "f17": "get_gpio_direction",
    "f18": "get_gpio_wake_mask",
    "f19": "get_gpio_unsolicited_rsp_mask",
    "f1a": "get_gpio_sticky_mask",
    "f1c": "get_config_default",
    "f20": "get_subsystem_id",
    "f24": "get_stripe_control",
    "f2d": "get_cvt_chan_count",
    "f2e": "get_hdmi_dip_size",
    "f2f": "get_hdmi_eldd",
    "f30": "get_hdmi_dip_index",
    "f31": "get_hdmi_dip_data",
    "f32": "get_hdmi_dip_xmit",
    "f33": "get_hdmi_cp_ctrl",
    "f34": "get_hdmi_chan_slot",
    "f35": "get_device_sel",
    "f36": "get_device_list",
};

params = {
    '00': 'vendor_id',
    '01': 'subsystem_id',
    '02': 'revision_id',
    '04': 'node_count',
    '05': 'function_type',
    '08': 'FG_cap',
    '09': 'audio_wid_cap',
    '0a': 'PCM',
    '0b': 'stream',
    '0c': 'pin_cap',
    '0d': 'amp_in_cap',
    '0e': 'connect_len',
    '0f': 'power_state',
    '10': 'proc_cap',
    '11': 'GPIO_cap',
    '12': 'amp_out_cap',
    '13': 'volknob_cap',
};

def extractVerb(value) :
    nid = (value >> 20) & 0xFFF
    baseVerb = (value >> 16) & 0xF
    param=''

    if baseVerb == 2 :
        name = "set_stream_format"
    elif baseVerb == 3 :
        name = "set_amp_gain_mute"
    elif baseVerb == 4 :
        name = "set_proc_coef"
    elif baseVerb == 5 :
        name = "set_coef_index"
    elif baseVerb == 0xa :
        name = "get_stream_format"
    elif baseVerb == 0xb :
        name = "get_amp_gain_mute"
    elif baseVerb == 0xc :
        name = "get_proc_coef"
    elif baseVerb == 0xd :
        name = "get_coef_index"
    elif baseVerb == 0x7 or baseVerb == 0xF :
        verb = (value >> 8) & 0xFFF
        verb = '%03x' % verb
        name = names[verb] if verb in names else 'unknown'
        if verb == 'f00' :
            extra = '%02x' % (value & 0xFF)
            if extra in params :
                param = ', param: %s' % params[extra]
    else :
        name = "unknown"

    return '0x%08x: nid=0x%02x, %s%s' % (value, nid, name, param)
