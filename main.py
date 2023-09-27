from rembg import remove
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)


class NotSupportedFormat(Exception):
    ...


class Remover:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

    def _clear_output_folder(self) -> None:
        logger.info("Clear output folder")
        output_dir = os.path.join(self.ROOT_PATH, 'data', 'output')

        for r, d, f in os.walk(output_dir):
            for output_file in f:
                file_to_remove = os.path.join(r, output_file)
                os.remove(file_to_remove)
        logger.info("Output folder cleared")

    def _get_input_files(self) -> list:
        logger.info("Get input files")
        # input_dir = f'{self.ROOT_PATH}\\data\\input'
        input_dir = os.path.join(self.ROOT_PATH, 'data', 'input')
        input_files = []

        for r, d, f in os.walk(input_dir):
            for input_file in f:
                input_files.append(os.path.join(r, input_file))

        logger.info("Input files: %s", input_files)

        return input_files

    def _get_output_filename(self, input_file: str) -> str:
        filename = input_file.split("\\")[-1]
        logger.info("Generate output path for file: %s", filename)
        if 'jpg' in filename:
            output_file_path = os.path.join(self.ROOT_PATH, 'data', 'output', filename.replace('jpg', 'png'))
        elif 'jpeg' in filename:
            output_file_path = os.path.join(self.ROOT_PATH, 'data', 'output', filename.replace('jpeg', 'png'))
        elif 'png' in filename:
            output_file_path = os.path.join(self.ROOT_PATH, 'data', 'output', filename)
        else:
            raise NotSupportedFormat("Not supported format")

        logger.info("Output file path: %s", output_file_path)

        return output_file_path

    def _do_remove_background(self, input_file_path: str, output_file_path: str) -> None:
        logger.info("Delete background from file: %s", input_file_path)
        aggregated_file = Image.open(input_file_path)
        outfile = remove(aggregated_file)
        outfile.save(output_file_path)
        logger.info("File saved in: %s", output_file_path)

    def remove_background(self) -> None:
        self._clear_output_folder()
        img_files = self._get_input_files()
        for img_file in img_files:
            try:
                output_filename = self._get_output_filename(img_file)
                self._do_remove_background(img_file, output_filename)
            except Exception as e:
                logger.error("Remove background error: %s", e)


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)-7s] %(message)s',
        level=logging.DEBUG,
        filename='remove_backgrounds.log'
    )
    remover = Remover()
    remover.remove_background()
