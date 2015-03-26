"""
    Example script for folks that wish to compare PokitDok provider data to data they may already use.
    Ideal for using free trial data API credits for sampling a provider list and exporting
    PokitDok provider information for the randomly selected providers
"""
import argparse
import csv
import json
import os
import zipfile

import pokitdok


def export_providers_sample(client_id, client_secret, csv_file, sample_size, output_directory):
    """
        Export PokitDok provider data based on a CSV file containing NPI values

        :param client_id: a valid PokitDok Platform client id
        :param client_secret: a valid PokitDok Platform client secret
        :param csv_file: a CSV file containing the NPI values to sample.  First column should contain NPI
        :param sample_size: the number of samples to take from the supplied file.
        :param output_directory: the directory where provider data will be exported in a zip file
    """

    pd = pokitdok.api.connect(client_id, client_secret)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(csv_file, 'r') as npi_sample_file:
        sample_count = 0
        for row in csv.reader(npi_sample_file):
            npi = row[0]
            print('Fetching data for NPI: {0} ...'.format(npi))
            response = pd.providers(npi=npi)
            api_sample_data_file = os.path.join(output_directory, '{0}_providers_json.txt'.format(npi))
            with open(api_sample_data_file, 'w') as api_data_file:
                json.dump(response.get('data', {}), api_data_file, sort_keys=True, indent=4)

            sample_count += 1
            if sample_count >= sample_size:
                break

    zip_directory, zip_file_prefix = os.path.split(output_directory)
    sample_zip_filename = os.path.join(zip_directory, '{0}.zip'.format(zip_file_prefix))
    sample_zip_file = zipfile.ZipFile(sample_zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(output_directory):
            for api_sample_file in files:
                file_to_zip = os.path.join(root, api_sample_file)
                archive_name = '{0}/{1}'.format(os.path.split(output_directory)[1], os.path.split(api_sample_file)[1])
                sample_zip_file.write(file_to_zip, archive_name)
    sample_zip_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export a sample of PokitDok Providers data')
    parser.add_argument('--client-id', type=str, dest='client_id', help='your PokitDok Platform API client id')
    parser.add_argument('--client-secret', type=str, dest='client_secret',
                        help='your PokitDok Platform API client secret')

    parser.add_argument('--sample-size', dest='sample_size', type=int, default=20,
                        help='the number of provider samples to collect (default: 20)')
    parser.add_argument('--csv-file', type=str, dest='csv_file', default='providers.csv',
                        help='a CSV file containing the set of providers to sample '
                             'the first column should contain the provider NPI. (default: providers.csv)')
    parser.add_argument('--output-dir', type=str, dest='output_directory', default='ProviderData',
                        help='provider data output directory (default: ProviderData)')

    args = parser.parse_args()
    export_providers_sample(args.client_id, args.client_secret, args.csv_file, args.sample_size, args.output_directory)