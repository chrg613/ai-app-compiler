from pathlib import Path


class FileWriter:

    @staticmethod
    def write(
        output_dir: str,
        filename: str,
        content: str
    ):

        Path(
            output_dir
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            Path(output_dir)
            / filename
        )

        file_path.write_text(
            content
        )

        return str(
            file_path
        )