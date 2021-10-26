import os
from unittest import mock
import pytest
from tests.utils import get_data_folder
from geotiflib.task.addgcptask import AddGcpTask


def test_constructor():
    task = AddGcpTask()
    assert isinstance(task, AddGcpTask) is True


def test_run_not_existing_tif():
    task = AddGcpTask(input="not_existing.tif", output="output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing.tif" in str(exc.value)


def test_run_not_existing_points():
    file = os.path.join(get_data_folder(), 'AC04078710_bis.tif')
    task = AddGcpTask(input=file, output="output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "AC04078710_bis.tif.points" in str(exc.value)


def test_run_not_enough_points():
    file = os.path.join(get_data_folder(), 'AC04078710.tif')
    task = AddGcpTask(input=file, output="output.tif", min_points=100, log_location='/tmp')
    with pytest.raises(ImportError) as exc:
        task.run()
    assert "Insufficient number of GCPs: 26 < 100" in str(exc.value)


def test_run_invalid_points():
    file = os.path.join(get_data_folder(), 'AC04078710_tris.tif')
    task = AddGcpTask(input=file, output="output.tif", min_points=100, log_location='/tmp')
    with pytest.raises(ImportError) as exc:
        task.run()
    assert "Unable to parse GCPs file: " in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file = os.path.join(get_data_folder(), 'AC04078710_mini.tif')
    task = AddGcpTask(input=file, output="output.tif", min_points=0, log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    assert calls[0] == ['gdal_translate', '-of', 'GTiff',
                        '-gcp', '8540.92', '4987.67', '1822331.48', '6141557.76', file, 'output.tif']




