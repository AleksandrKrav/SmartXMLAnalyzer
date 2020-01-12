import argparse
import logging
from difflib import SequenceMatcher
from typing import Optional

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class ElementNotFoundError(Exception):
    pass


class SmartAnalyzer:
    def __init__(self, original_html: str, sample_html: str, target_element: str):
        self.target_element = target_element
        self.original_html_text = original_html
        self.sample_html_text = sample_html
        self.bs = BeautifulSoup(original_html, 'lxml')
        self.other_bs = BeautifulSoup(sample_html, 'lxml')
        self._tag = None
        self._other_tag = None

    @property
    def tag(self) -> Tag:
        if self._tag is None:
            tag = self.bs.find(id=self.target_element)
            if tag is None:
                raise ElementNotFoundError(f'Element {self.target_element} not found.')
            self._tag = tag
        return self._tag

    def find_similar_element(self) -> Optional[Tag]:
        sequence_matcher = SequenceMatcher()
        max_similar_ratio = 0.0
        result_elem = None

        elems = self.other_bs.find_all(self.tag.name)

        for elem in elems:
            sequence_matcher.set_seqs(str(self.tag), str(elem))
            ratio = sequence_matcher.ratio()
            if max_similar_ratio < ratio:
                max_similar_ratio = ratio
                result_elem = elem

        return result_elem

    @staticmethod
    def build_path_to_elem(elem: Tag) -> str:
        path = [elem.name]
        for parent in elem.parents:
            if parent.name == '[document]':
                break
            path.insert(0, parent.name)
        return ' > '.join(path)


def setLoggerConfig():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    setLoggerConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-of', '--original_path',
        type=str, help='path to original file',
        required=True
    )
    parser.add_argument(
        '-sf', '--sample_path',
        type=str, help='path to sample file',
        required=True
    )
    parser.add_argument(
        '-te', '--target_element',
        type=str, help='element that needed to find in sample file',
        default='make-everything-ok-button'
    )

    args = parser.parse_args()

    original_file_path = args.original_path
    sample_file_path = args.sample_path
    target_element = args.target_element

    logger.info(f'Original file path: {original_file_path}')
    logger.info(f'Sample file path: {sample_file_path}')
    logger.info(f'Target element: {target_element}')

    with open(original_file_path) as f1, open(sample_file_path) as f2:
        orignal_content = f1.read()
        sample_content = f2.read()

    analyzer = SmartAnalyzer(orignal_content, sample_content, target_element)
    try:
        element = analyzer.find_similar_element()
    except ElementNotFoundError as e:
        logger.error('Failed analyzed on finding similar elements.', exc_info=True, extra={
            'target_element': target_element,
        })
    else:
        logger.info(f'Path to the element: {analyzer.build_path_to_elem(element)}')
