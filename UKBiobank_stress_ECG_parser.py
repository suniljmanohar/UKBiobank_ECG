import numpy as np
import xmltodict as xtd

import UKBiobank_stress_ECG_plot

# import UKBiobank_ECG_plot


""" Copyright 2023 Dr Sunil Manohar (sunil.manohar@cardiov.ox.ac.uk) """


def main():
    # EXAMPLE USAGE - adjust parameter values as required

    # names and order of leads to import
    lead_order = ["I", "2", "3"]

    # indices of median beats to import (16 indexed median beats in each file)
    indices = [0, 15]

    # pathname of XML file to import
    fname = 'G:\\UKBB\\ECG\\1000037_6025_1_0.xml'

    # pathname of output for image file
    save_image_to = 'g:\\ukbb\\1000037_6025_1_0.svg'

    # run example
    ecg, median_ecg, md = import_ecg(fname, save_image_to, lead_order, indices)


def import_ecg(fname, save_image_to, lead_order, indices):
    f = open(fname, "rt")
    raw_input = f.read()
    f.close()

    # extract ECG and metadata
    ecg, median_ecgs, md = parse_xml(raw_input, lead_order, indices)
    md['filename'] = fname

    # plot and save
    md['filename'] = fname
    UKBiobank_stress_ECG_plot.plot_long_ecg(ecg, md, display=True, save_to=save_image_to)

    for idx in median_ecgs:
        md['filename'] = f'{fname}, index = {idx}'
        UKBiobank_stress_ECG_plot.plot_iso_ecg(median_ecgs[idx], md,
                                        save_to=save_image_to + f'_index={idx}', display=True)

    # return output data
    return ecg, median_ecgs, md


def parse_xml(input_data, lead_order, indices):
    """ Takes input as raw xml data read from file (Cardiosoft specification), returns list of 12 lead waveforms
    and metadata. """
    md = {}  # metadata dictionary
    data = xtd.parse(input_data)['CardiologyXML']

    full_lead_nodes = [['StripData', 'Strip', 'WaveformData'], ['Strip', 'StripData', 'WaveformData']]
    full_leads = get_lead_data(data, full_lead_nodes, lead_order)

    median_data = get_median_data(data, lead_order, indices)

    md = get_metadata(data, md)
    md['lead order'] = lead_order

    return np.array(full_leads, dtype=np.int16), median_data, md


def get_lead_data(data, nodes, lead_order):
    leads = [[] for i in range(3)]
    raw_lead_data = get_xml_node(data, nodes)

    # check number of leads
    if len(raw_lead_data) != 3:
        print('Warning: only {} leads found'.format(len(raw_lead_data)))

    # split data into 3 leads and convert string into individual values
    else:
        for i in range(len(raw_lead_data)):
            lead_n = lead_order.index(raw_lead_data[i]['@lead'].upper())
            lead_data_string = raw_lead_data[i]['#text']
            lead_vals = [int(x) for x in lead_data_string.split(",")]
            leads[lead_n] = lead_vals

    return leads


def get_median_data(data, lead_order, indices):
    output = {}
    median_lead_nodes = [['MedianData', 'Median']]
    medians = get_xml_node(data, median_lead_nodes)
    for idx in indices:
        leads = [[]] * 3
        m = medians[idx]['WaveformData']
        for lead_n in range(3):
            lead_name = lead_order.index(m[lead_n]['@lead'].upper())
            lead_data_string = m[lead_n]['#text']
            lead_vals = [int(x) for x in lead_data_string.split(",")]
            leads[lead_name] = lead_vals

        output[idx] = np.array(leads)

    return output


def get_xml_node(data, node_list):
    output = data
    try:
        for x in node_list[0]:
            output = output[x]
    except KeyError:
        output = data[:]
        try:
            for x in node_list[1]:
                output = output[x]
        except:
            raise ValueError('No lead data found!')
    return output


def get_metadata(data, md):
    md['sample rate'] = float(data['StripData']['SampleRate']['#text'])
    md['t scale'] = 1. / md['sample rate']
    md['v scale'] = float(data['StripData']['Resolution']['#text'])
    return md


if __name__ == '__main__':
    main()
