
import os


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
    def init_sub_collection_directory(outdir):
        # type: (str) -> None
        """
        Creates a sub-collection directory
        :param outdir: the full path to the sub-collection directory
        :return: string value for the new working directory that was created.
        """
        os.mkdir(outdir)

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
    def correct_text_encoding(text_content):
        # type: (str) -> str
        """
        CONTENTdm export does not encode special characters correctly
        or consistently. This method cleans up the problem. Pass all
        strings from text elements through this filter.

        :param text_content: The element's text value
        :return: Updated text
        """
        # Some contentdm transcriptions include html markup for line break
        text_content = text_content.replace('lt;br gt;', '')
        # apostrophe (allowed in XML text)
        text_content = text_content.replace('&amp;#x27', '\'')
        text_content = text_content.replace('&#x27;', '\'')
        text_content = text_content.replace('&amp;apos;', '\'')
        text_content = text_content.replace('&apos;', '\'')
        # quote (allowed in XML text)
        text_content = text_content.replace('&amp;quot;', '"')
        text_content = text_content.replace('&quot;', '"')
        # brackets (encode these correctly)
        text_content = text_content.replace('&amp;gt;', '&gt')
        text_content = text_content.replace('&amp;lt;', '&lt')
        # When importing into DSpace as Simple Archive Format, the ampersand special character
        # is imported without decoding. It's not valid xml (I think) ... but here we need to convert the
        # &amp; to a literal ampersand (&).
        text_content = text_content.replace('&amp;', '&')
        # remove ending semicolons from the metatdata
        if text_content.endswith(';'):
            text_content = text_content[:-1]

        return text_content
