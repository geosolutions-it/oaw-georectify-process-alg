import os
from unittest import mock
import pytest
from tests.utils import get_data_folder
from geotiflib.task.addoverviewtask import AddOverviewTask


def test_constructor():
    task = AddOverviewTask()
    assert isinstance(task, AddOverviewTask) is True


def test_run_not_existing_tif():
    task = AddOverviewTask(input="not_existing.tif", log_location='/tmp')
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
    file_tif = os.path.join(get_data_folder(), 'AC04078710.tif')
    task = AddOverviewTask(input=file_tif, log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdaladdo',
                        '-r', 'average',
                        '--config', 'GDAL_TIFF_OVR_BLOCKSIZE', '512',
                        file_tif]
