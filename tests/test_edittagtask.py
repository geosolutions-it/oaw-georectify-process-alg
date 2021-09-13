import os
from unittest import mock
import pytest
from .utils import get_data_folder
from geotiflib.task.edittagtask import EditTagTask


def test_constructor():
    task = EditTagTask()
    assert isinstance(task, EditTagTask) is True


def test_run_not_existing_input_file():
    task = EditTagTask(input="not_existing_input.tif", output="not_existing_output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing_input.tif" in str(exc.value)


def test_run_not_existing_output_file():
    file = os.path.join(get_data_folder(), 'AC04078710.tif')
    task = EditTagTask(input=file, output="not_existing_output.tif", log_location='/tmp')
    with pytest.raises(FileNotFoundError) as exc:
        task.run()
    assert "not_existing_output.tif" in str(exc.value)


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    file_in = os.path.join(get_data_folder(), 'test999_0007.tif')
    file_out = os.path.join(get_data_folder(), 'AC04078710.tif')
    task = EditTagTask(input=file_in, output=file_out, log_location='/tmp')
    task.run()
    assert mock_subproc_popen.called
    assert mock_subproc_popen.call_count == 1
    calls = [item["args"] for item in [item[2] for item in mock_subproc_popen.mock_calls] if len(item) > 1]
    call = calls[0]
    assert len(call) == 23
    assert call[0] == 'python'
    assert call[1] == 'gdal_edit.py'
    # creator
    assert "OAW_CREATOR=" in call[3]
    assert "Akademie der Wissenschaften Wien" in call[3]
    # date
    assert "OAW_DATE=" in call[5]
    assert "1750" in call[5]
    # description
    assert "OAW_DESCRIPTION=" in call[7]
    assert "Bibliographische Informationen Quelle;" in call[7]
    assert "Augsburg [Verlagsort]" in call[7]
    # edition
    assert "OAW_EDITION=" in call[9]
    # format
    assert "OAW_FORMAT=" in call[11]
    assert "Massstab: 37000000" in call[11]
    # identifier
    assert "OAW_IDENTIFIER=" in call[13]
    assert "AC12708841" in call[13]
    # relation
    assert "OAW_RELATION=" in call[15]
    assert "Gesamttitel: Accurata Globi Terrestris; Reihenfolge in Serie: [5]" in call[15]
    # source
    assert "OAW_SOURCE=" in call[17]
    assert "https://goobi.acdh.oeaw.ac.at/viewer/image/AC12708841" in call[17]
    # subject
    assert "OAW_SUBJECT=" in call[19]
    assert "Kartentyp; Kontinentalkarte" in call[19]
    # title
    assert "OAW_TITLE=" in call[21]
    assert "SEUTTER Suedamerika 1750" in call[21]

    assert call[22] == file_out


"""
def test_run_real():
    qgis_scripts = "C:\\OSGeo4W64\\apps\\Python37\\Scripts\\"
    file_in = "C:/temp/oaw/staging/KIASOst71.tif"
    file_out = "C:/temp/oaw/staging/KIASOst71_grf_fin.tif"
    task = EditTagTask(input=file_in, output=file_out, qgis_scripts=qgis_scripts)
    task.run()

    from geotiflib import geotiff
    file_out = "C:/temp/oaw/staging/KIASOst71_grf_fin.tif"
    path = os.path.join(file_out)
    tif = geotiff.GeoTiff(path)
    dictionary = tif.oaw_metadata_dict()
    print(dictionary)
"""
