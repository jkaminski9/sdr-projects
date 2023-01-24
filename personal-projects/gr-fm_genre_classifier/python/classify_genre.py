#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 John S. Kaminski Jr..
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy
from gnuradio import gr
import pickle
from python_speech_features import mfcc
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
import matplotlib.image as img
import pmt

class classify_genre(gr.sync_block):
    """
    docstring for block classify_genre
    """
    def __init__(self, segment_len_samples, clf_file, scaler_file, lda_file, rx_rate=24000):
        gr.sync_block.__init__(self,
            name="classify_genre",
            in_sig=[(numpy.float32, segment_len_samples),],
            out_sig=[np.byte])

        self.clf = pickle.load(open(clf_file, 'rb'))
        self.lda = pickle.load(open(lda_file, 'rb'))
        self.scaler = pickle.load(open(scaler_file, 'rb'))
        self.rx_rate = rx_rate
        self.title = "Collecting Audio!"
        self.message_port_register_out(pmt.intern(
    def work(self, input_items, output_items):
        in0 = input_items[0]
        for idx in range(in0.shape[0]):
            sig = in0[idx, :]
            sig = (sig - sig.min()) / (sig.max() - sig.min())
            mfcc_feat = mfcc(sig, self.rx_rate, winlen=0.020, appendEnergy=False)
            covariance = numpy.cov(numpy.matrix.transpose(mfcc_feat))
            mean_matrix = mfcc_feat.mean(0)
            skew_matrix = skew(mfcc_feat, axis=0)
            kurt_matrix = kurtosis(mfcc_feat, axis=0)
            feat = numpy.concatenate((mean_matrix, covariance.flatten(), skew_matrix, kurt_matrix))
            feat = feat.reshape([1, len(feat)])
            feat = self.scaler.transform(feat)
            feat = self.lda.transform(feat)
            label = self.clf.predict(feat)
            label = label[0]
            self.title = "Predicted Genre: " + label
        return len(input_items[0])

