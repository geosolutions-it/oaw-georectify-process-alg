import os
from unittest import mock
import pytest
from tests.utils import get_data_folder
from geotiflib.task.warptask import WarpTask


def test_constructor():
    task = WarpTask()
    assert isinstance(task, WarpTask) is True


def test_run_not_existing_tif():
    task = WarpTask(input="not_existing.tif", output="output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing.tif" in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file = os.path.join(get_data_folder(), 'AC04078710.tif')
    task = WarpTask(input=file, output="output.tif", log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdalwarp', '-t_srs', 'EPSG:3857', '-r', 'lanczos', '-tps', '-co', '-dstalpha',
                        file, 'output.tif']





