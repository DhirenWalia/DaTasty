from pathlib import Path
import pandas as pd


def load_excel():

    project_root = Path(__file__).resolve().parent.parent

    output_folder = (
        project_root
        / "data"
        / "output"
    )

    files = list(
        output_folder.glob("*.xlsx")
    )

    if not files:

        raise FileNotFoundError(
            f"No DATATSTY reports found in: {output_folder}"
        )

    latest_report = max(
        files,
        key=lambda x: x.stat().st_ctime
    )

    import shutil
    import tempfile

    temp_file = (
    Path(tempfile.gettempdir())
    / latest_report.name
)

    shutil.copy2(
        latest_report,
        temp_file
    )

    sheets = pd.read_excel(
    temp_file,
    sheet_name=None,
    engine="openpyxl"
)

    return sheets