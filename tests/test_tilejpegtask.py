import os
import mock
import pytest
from .utils import get_data_folder
from geotiflib.task.tilejpegtask import TileJpegTask


def test_constructor():
    task = TileJpegTask()
    assert isinstance(task, TileJpegTask) is True


def test_run_not_existing_vrt():
    task = TileJpegTask(input="not_existing.vrt", output="output.tif")
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing.vrt" in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file_vrt = os.path.join(get_data_folder(), 'AC04078710_final.vrt')
    file_tif = os.path.join(get_data_folder(), 'AC04078710_final.tif')
    task = TileJpegTask(input=file_vrt, output=file_tif)
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdal_translate',
                        '-mo', 'NODATA_VALUES=0 0 0',
                        '-colorinterp', 'red,green,blue',
                        '-co', 'COMPRESS=JPEG',
                        '-co', 'PHOTOMETRIC=YCBCR',
                        '-co', 'TILED=YES',
                        '-co', 'BLOCKXSIZE=512',
                        '-co', 'BLOCKYSIZE=512',
                        '-b', '1', '-b', '2', '-b', '3', '-mask', '4',
                        file_vrt,
                        file_tif]

