import mock
from geotiflib import gdalprocess


def test_constructor():
    prc = gdalprocess.GdalProcess("my_process")
    assert isinstance(prc, gdalprocess.GdalProcess) is True


@mock.patch('subprocess.Popen')
def test_process(mock_subproc_popen):
    process_mock = mock.Mock()
    #attrs = {'communicate.return_value': ('output', 'error')}
    attrs = {
        'stdout.readlines.return_value': "output",
        'stderr.readlines.return_value': "nothing"
    }
    process_mock.configure_mock(**attrs)
    mock_subproc_popen.return_value = process_mock
    prc = gdalprocess.GdalProcess("calc", "division", "4", "2", ret_out=True)
    result = prc.process()
    assert result == "output"
