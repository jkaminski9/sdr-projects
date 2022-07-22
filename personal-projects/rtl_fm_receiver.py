#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Communications Theory FM Receiver Demo
# Author: jkaminski
# GNU Radio version: v3.8.5.0-6-g57bd109d

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import numpy
import osmosdr
import time

from gnuradio import qtgui

class rtl_fm_receiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Communications Theory FM Receiver Demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Communications Theory FM Receiver Demo")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "rtl_fm_receiver")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.use_envelope = use_envelope = True
        self.flo = flo = 0.05
        self.Channel = Channel = 99.5
        self.samp_rate = samp_rate = 228e3
        self.rtl_freq = rtl_freq = Channel if use_envelope == False else Channel + flo
        self.output_idx = output_idx = 1 if use_envelope == False else 0
        self.input_idx = input_idx = 1 if use_envelope == False else 0
        self.b = b = [0.5, 0, -0.5]
        self.Volume = Volume = 3
        self.Gain = Gain = 10

        ##################################################
        # Blocks
        ##################################################
        self._Volume_range = Range(0, 15, 1, 3, 200)
        self._Volume_win = RangeWidget(self._Volume_range, self.set_Volume, 'Volume', "counter_slider", float)
        self.top_layout.addWidget(self._Volume_win)
        self._Gain_range = Range(0, 50, 1, 10, 200)
        self._Gain_win = RangeWidget(self._Gain_range, self.set_Gain, 'Gain', "counter_slider", float)
        self.top_layout.addWidget(self._Gain_win)
        _use_envelope_check_box = Qt.QCheckBox('use_envelope')
        self._use_envelope_choices = {True: True, False: False}
        self._use_envelope_choices_inv = dict((v,k) for k,v in self._use_envelope_choices.items())
        self._use_envelope_callback = lambda i: Qt.QMetaObject.invokeMethod(_use_envelope_check_box, "setChecked", Qt.Q_ARG("bool", self._use_envelope_choices_inv[i]))
        self._use_envelope_callback(self.use_envelope)
        _use_envelope_check_box.stateChanged.connect(lambda i: self.set_use_envelope(self._use_envelope_choices[bool(i)]))
        self.top_layout.addWidget(_use_envelope_check_box)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(rtl_freq * 1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(Gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=0.00001)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=0.00001)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate / 5, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate ,
                20e3,
                5000,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                100e3,
                10e3,
                firdes.WIN_HAMMING,
                6.76))
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, (-1, 1))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(32, True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0, 0, 0)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,input_idx,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,output_idx)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(Volume)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 0)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0_0 = audio.sink(int(samp_rate/5), '', True)
        self.audio_sink_0 = audio.sink(int(samp_rate/5), '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=1,
        )
        self._Channel_range = Range(88.3, 106.9, 0.2, 99.5, 200)
        self._Channel_win = RangeWidget(self._Channel_range, self.set_Channel, 'Channel', "counter_slider", float)
        self.top_layout.addWidget(self._Channel_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rtl_fm_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_use_envelope(self):
        return self.use_envelope

    def set_use_envelope(self, use_envelope):
        self.use_envelope = use_envelope
        self.set_input_idx(1 if self.use_envelope == False else 0)
        self.set_output_idx(1 if self.use_envelope == False else 0)
        self.set_rtl_freq(self.Channel if self.use_envelope == False else self.Channel + self.flo)
        self._use_envelope_callback(self.use_envelope)

    def get_flo(self):
        return self.flo

    def set_flo(self, flo):
        self.flo = flo
        self.set_rtl_freq(self.Channel if self.use_envelope == False else self.Channel + self.flo)

    def get_Channel(self):
        return self.Channel

    def set_Channel(self, Channel):
        self.Channel = Channel
        self.set_rtl_freq(self.Channel if self.use_envelope == False else self.Channel + self.flo)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate , 20e3, 5000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate / 5)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_rtl_freq(self):
        return self.rtl_freq

    def set_rtl_freq(self, rtl_freq):
        self.rtl_freq = rtl_freq
        self.rtlsdr_source_0.set_center_freq(self.rtl_freq * 1e6, 0)

    def get_output_idx(self):
        return self.output_idx

    def set_output_idx(self, output_idx):
        self.output_idx = output_idx
        self.blocks_selector_0.set_output_index(self.output_idx)

    def get_input_idx(self):
        return self.input_idx

    def set_input_idx(self, input_idx):
        self.input_idx = input_idx
        self.blocks_selector_0_0.set_input_index(self.input_idx)

    def get_b(self):
        return self.b

    def set_b(self, b):
        self.b = b

    def get_Volume(self):
        return self.Volume

    def set_Volume(self, Volume):
        self.Volume = Volume
        self.blocks_multiply_const_vxx_0.set_k(self.Volume)

    def get_Gain(self):
        return self.Gain

    def set_Gain(self, Gain):
        self.Gain = Gain
        self.rtlsdr_source_0.set_gain(self.Gain, 0)





def main(top_block_cls=rtl_fm_receiver, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
