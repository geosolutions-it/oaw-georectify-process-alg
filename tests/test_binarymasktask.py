import os
from unittest import mock
import pytest
from tests.utils import get_data_folder
from geotiflib.task.binarymasktask import BinaryMaskTask


def test_constructor():
    task = BinaryMaskTask()
    assert isinstance(task, BinaryMaskTask) is True


def test_run_not_existing_vrt():
    task = BinaryMaskTask(input="not_existing_b{band}.vrt", output="output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing_b1.vrt" in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file = os.path.join(get_data_folder(), 'AC04078710_b{band}.vrt')
    task = BinaryMaskTask(input=file, output="output.tif", log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == [
        'python', 'gdal_calc.py',
        '--type=Byte',
        '--co=NUM_THREADS=4',
        '--co=PHOTOMETRIC=MINISBLACK',
        '--co=NBITS=1',
        '--co=TILED=YES',
        '--co=COMPRESS=DEFLATE',
        '-A', file.replace("{band}", "1"),
        '-B', file.replace("{band}", "2"),
        '-C', file.replace("{band}", "3"),
        '--calc=logical_not(logical_and(logical_and(A==0,B==0),C==0))',
        '--outfile', 'output.tif']
