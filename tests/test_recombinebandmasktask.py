import os
import mock
import pytest
from .utils import get_data_folder
from geotiflib.task.recombinebandmasktask import RecombineBandMaskTask


def test_constructor():
    task = RecombineBandMaskTask()
    assert isinstance(task, RecombineBandMaskTask) is True


def test_run_not_existing_vrt():
    task = RecombineBandMaskTask(input_vrt="not_existing_b{band}.vrt", input_mask="not_existing_mask.tif", output="output.vrt")
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing_b1.vrt" in str(exc.value)


def test_run_not_existing_mask():
    file = os.path.join(get_data_folder(), 'AC04078710_b{band}.vrt')
    task = RecombineBandMaskTask(input_vrt=file, input_mask="not_existing_mask.tif", output="output.vrt")
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing_mask.tif" in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file_vrt = os.path.join(get_data_folder(), 'AC04078710_b{band}.vrt')
    file_tif = os.path.join(get_data_folder(), 'AC04078710_mask.tif')
    task = RecombineBandMaskTask(input_vrt=file_vrt, input_mask=file_tif, output="output.vrt")
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdalbuildvrt',
                        'output.vrt',
                        file_vrt.replace("{band}", "1"),
                        file_vrt.replace("{band}", "2"),
                        file_vrt.replace("{band}", "3"),
                        file_tif
                        ]
