import csv


class GCP:
    def __init__(self, row):
        self.mapX = float(row[0])
        self.mapY = float(row[1])
        self.pixelX = float(row[2])
        self.pixelY = float(row[3])
        self.enable = True
        if len(row) > 4:
            self.enable = row[4] == '1'
        self.dX = None
        self.dY = None
        self.residual = None
        if len(row) > 5:
            self.dX = float(row[5])
        if len(row) > 6:
            self.dY = float(row[6])
        if len(row) > 7:
            self.residual = float(row[7])

    def __str__(self):
        return '-gcp %.2f %.2f %.2f %.2f' % (self.pixelX, -self.pixelY, self.mapX, self.mapY)


class GCPReader:
    """
    Reder of the GCPs file (*.tif.points)
    """
    def __init__(self, file_path):
        """
        Constructor of the class
        :param file_path: full path to the file containing the GCPs
        """
        self.file_path = file_path
        self.gcp_list = []

    def parse(self):
        """
        Parse the *tif.points file
        :return: boolean
        """
        try:
            with open(self.file_path, newline='') as file:
                reader = csv.reader(file, delimiter=',')
                cont = 0
                for row in reader:
                    if cont > 0:
                        self.gcp_list.append(GCP(row))
                    cont += 1
            return True
        except ValueError:
            return False

    def get_list(self, only_enabled=False):
        """
        Return the list of GCPs in the file
        :param only_enabled: read just the enabled pairs
        :return:
        """
        if only_enabled is False:
            return self.gcp_list
        else:
            return [p for p in self.gcp_list if p.enable]

    def get_list_as_string(self, only_enabled=False):
        """
        Return the list of GCPs in the file as single string
        :param only_enabled: read just the enabled pairs
        :return:
        """
        return ' '.join(map(str, self.get_list(only_enabled)))

    def count(self, only_enabled=False):
        """
        Return the number of GCPs in the file
        :param only_enabled: read just the enabled pairs
        :return: int
        """
        return len(self.get_list(only_enabled))
