#!/usr/bin/env python

import sys
import os


class Utils:

    def __init__(self, outdir):
        self.outdir = outdir

    @staticmethod
    def makeBatchDir(batchVal):

        newDir = '/batch_' + str(batchVal)
        return newDir

    def initWorkingDirectory(this, batch):
        """
        Creates and returns path of working directory.
        :param batch: the count used to create a new sub-directory path.
        :return: string value for the new working directory that was created.
        """
        workingdir = this.outdir + this.makeBatchDir(batch)
        os.mkdir(workingdir)
        return workingdir

    @staticmethod
    def intSafSubDirectory(workingdir, counter):
        """
        Creates the saf sub-directory and returns path.
        :param workingdir: the current working directory that contains saf output directories.
        :param counter: the current item count
        :return: string value for the saf item directory that was created.
        """
        # This works for 1 - 9999 items.
        counter_str = str(counter)
        current_dir = ''
        if len(counter_str) == 1:
            current_dir = '/item_000' + counter_str
        if len(counter_str) == 2:
            current_dir = '/item_00' + counter_str
        if len(counter_str) == 3:
            current_dir = '/item_0' + counter_str
        if len(counter_str) == 4:
            current_dir = '/item_' + counter_str

        saf_item = workingdir + current_dir

        os.mkdir(saf_item)

        return saf_item

    @staticmethod
    def getFinalCount(batch, counter):
        """
        Utility function for getting the final count of records loaded.
        :param batch: the count of saf sub-directories.
        :param counter: the current count of records loaded.
        :return: the final count, including records loaded in previous batches.
        """
        if batch == 1:
            return counter
        else:
            return (batch * 1000) + counter
