import logging
from typing import Dict, Type, List, Union

from calamari_ocr.ocr.dataset import DataSetType
from tfaip.base.data.pipeline.definitions import PipelineMode

from calamari_ocr.ocr.dataset.params import PipelineParams
from calamari_ocr.ocr.dataset.datareader.base import CalamariDataGenerator

from calamari_ocr.utils import keep_files_with_same_file_name

logger = logging.getLogger(__name__)


class DataReaderFactory:
    CUSTOM_READERS: Dict[str, Type[CalamariDataGenerator]] = {}

    @classmethod
    def create_data_reader(cls,
                           type: Union[DataSetType, str],
                           mode: PipelineMode,
                           images: List[str] = None,
                           texts: List[str] = None,
                           skip_invalid=False,
                           remove_invalid=True,
                           non_existing_as_empty=False,
                           ) -> CalamariDataGenerator:
        if images is None:
            images = []

        if texts is None:
            texts = []

        if args is None:
            args = dict()

        if type in cls.CUSTOM_READERS:
            return cls.CUSTOM_READERS[type](mode=mode,
                                            images=images,
                                            texts=texts,
                                            skip_invalid=skip_invalid,
                                            remove_invalid=remove_invalid,
                                            non_existing_as_empty=non_existing_as_empty,
                                            args=args,
                                            )

        if DataSetType.files(type):
            if images:
                images.sort()

            if texts:
                texts.sort()

            if images and texts and len(images) > 0 and len(texts) > 0:
                images, texts = keep_files_with_same_file_name(images, texts)

        if type == DataSetType.RAW:
            from calamari_ocr.ocr.dataset.datareader.raw import RawDataReader
            return RawDataReader(mode, images, texts)

        elif type == DataSetType.FILE:
            from calamari_ocr.ocr.dataset.datareader.file import FileDataReader
            return FileDataReader(mode, images, texts,
                                  skip_invalid=skip_invalid,
                                  remove_invalid=remove_invalid,
                                  non_existing_as_empty=non_existing_as_empty)
        elif type == DataSetType.ABBYY:
            from calamari_ocr.ocr.dataset.datareader.abbyy import AbbyyReader
            return AbbyyReader(mode, images, texts,
                               skip_invalid=skip_invalid,
                               remove_invalid=remove_invalid,
                               non_existing_as_empty=non_existing_as_empty)
        elif type == DataSetType.PAGEXML:
            from calamari_ocr.ocr.dataset.datareader.pagexml.reader import PageXMLReader
            return PageXMLReader(mode, images, texts,
                                 skip_invalid=skip_invalid,
                                 remove_invalid=remove_invalid,
                                 non_existing_as_empty=non_existing_as_empty,
                                 args=args)
        elif type == DataSetType.HDF5:
            from calamari_ocr.ocr.dataset.datareader.hdf5 import Hdf5Reader
            return Hdf5Reader(mode, images, texts)
        elif type == DataSetType.EXTENDED_PREDICTION:
            from calamari_ocr.ocr.dataset.extended_prediction_dataset import ExtendedPredictionDataSet
            return ExtendedPredictionDataSet(texts=texts)
        elif type == DataSetType.GENERATED_LINE:
            from calamari_ocr.ocr.dataset.datareader.generated_line_dataset.dataset import GeneratedLineDataset
            return GeneratedLineDataset(mode, args=args)
        else:
            raise Exception("Unsupported dataset type {}".format(type))
