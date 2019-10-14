import os
from util.data_io import download_data


def download_files(base_url, file_names, data_folder):
    for file_name in file_names:
        download_data(base_url, file_name, data_folder, unzip_it=True, verbose=True)
    for file_name in os.listdir(data_folder):
        file = data_folder + '/' + file_name
        if file_name.endswith('.txt'):
            os.system('gzip %s' % file)


if __name__ == '__main__':
    data_folder = '/docker-share/data/MAG_authors'


    base_url = 'https://academicgraphv2.blob.core.windows.net/oag/mag/author'
    file_names = ('mag_authors_%d.zip' % k for k in range(3))
    download_files(base_url, file_names, data_folder)

    base_url = 'https://academicgraphv2.blob.core.windows.net/oag/aminer/author'
    file_names = ('aminer_authors_%d.zip' % k for k in range(4))
    download_files(base_url, file_names, data_folder)
