#!/usr/bin/env python

import os
from _elementtree import Element


class Utils:

    def __init__(self):
        pass


    @staticmethod
    def __make_batch_dir(batchVal):
        # type: (int) -> str
        """
        Creates new batch directory name.

        :param batchVal: the counter for the batch
        :return: new diretory name
        """
        newDir = '/batch_' + str(batchVal)
        return newDir

    @staticmethod
    def init_working_directory(outdir, batch):
        # type: (str, int) -> str
        """
        Creates and returns path of working directory.

        :param outdir: the base output directory
        :param batch: the count used to create a new sub-directory path.
        :return: string value for the new working directory that was created.
        """
        workingdir = outdir + Utils.__make_batch_dir(batch)
        os.mkdir(workingdir)
        return workingdir

    @staticmethod
    def int_saf_sub_directory(workingdir, counter):
        # type: (str, int) -> str
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
    def get_final_count(batch, counter):
        # type: (int, int) -> int
        """
        Utility function for getting the final count of records loaded.

        :param batch: the count of saf sub-directories.
        :param counter: the current count of records loaded.
        :return: the final count, including records loaded in previous batches.
        """
        if batch == 1:
            return counter
        else:
            return ((batch - 1) * 1000) + counter

    @staticmethod
    def correct_text_encoding(element):
        # type: (Element) -> object
        """
        CONTENTdm is sometimes exporting encoded characters that DSpace does not
        convert properly. If that problem can't be fixed in the software, use this
        function to make substitutions before importing to DSpace.

        :param element: The etree element
        :return: The etree element after substitution
        """

        # apostrophe
        element.text.replace('&amp;#x27', '&apos;')

        return element
