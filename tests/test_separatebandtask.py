import os
from unittest import mock
import pytest
from tests.utils import get_data_folder
from geotiflib.task.separatebandtask import SeparateBandTask


def test_constructor():
    task = SeparateBandTask()
    assert isinstance(task, SeparateBandTask) is True


def test_run_not_existing_tif():
    task = SeparateBandTask(input="not_existing.tif", output="output_b{band}.vrt", log_location='/tmp')
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
    task = SeparateBandTask(input=file, output=file + "_b{band}.vrt", log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 3
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdalbuildvrt', '-b', '1', '-hidenodata', file + "_b1.vrt", file]
    assert calls[1] == ['gdalbuildvrt', '-b', '2', '-hidenodata', file + "_b2.vrt", file]
    assert calls[2] == ['gdalbuildvrt', '-b', '3', '-hidenodata', file + "_b3.vrt", file]
