import numpy as np
import xmltodict as xtd
import UKBiobank_ECG_plot


""" Copyright 2023 Dr Sunil Manohar (sunil.manohar@cardiov.ox.ac.uk) """


def main():
    # EXAMPLE USAGE - adjust parameter values as required

    # names and order of leads to import
    lead_order = ["I", "II", "III", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6"]

    # pathname of XML file to import
    fname = 'G:\\UKBB\\ECG\\1000037_20205_2_0.xml'

    # pathname of output for image file
    save_image_to = 'g:\\ukbb\\1000037_20205_2_0.svg'

    # run example
    ecg, median_ecg, md = import_ecg(fname, save_image_to, lead_order)


def import_ecg(fname, save_image_to, lead_order):
    f = open(fname, "rt")
    raw_input = f.read()
    f.close()

    # extract ECG and metadata
    ecg, median_ecg, md = parse_xml(raw_input, lead_order)
    md['filename'] = fname

    # plot and save
    UKBiobank_ECG_plot.plot_long_ecg(ecg, md, display=True, save_to=save_image_to)
    UKBiobank_ECG_plot.plot_iso_ecg(median_ecg, md, save_to=save_image_to, display=True)

    # return output data
    return ecg, median_ecg, md


def parse_xml(input_data, lead_order):
    """ Takes input as raw xml data read from file (Cardiosoft specification), returns list of 12 lead waveforms
    and metadata. """
    md = {}  # metadata dictionary
    data = xtd.parse(input_data)['CardiologyXML']

    full_lead_nodes = [['StripData', 'WaveformData'], ['Strip', 'StripData', 'WaveformData']]
    median_lead_nodes = [['RestingECGMeasurements', 'MedianSamples', 'WaveformData'], []]
    full_leads = get_lead_data(data, full_lead_nodes, lead_order)
    median_leads = get_lead_data(data, median_lead_nodes, lead_order)

    md = get_metadata(data, md)
    md['lead order'] = lead_order

    return np.array(full_leads, dtype=np.int16), np.array(median_leads, dtype=np.int16), md


def get_lead_data(data, nodes, lead_order):
    leads = [[] for i in range(12)]
    raw_lead_data = get_xml_node(data, nodes)

    # check number of leads
    if len(raw_lead_data) != 12:
        print('Warning: only {} leads found'.format(len(raw_lead_data)))

    # split data into 12 leads and convert string into individual values
    else:
        for i in range(len(raw_lead_data)):
            lead_n = lead_order.index(raw_lead_data[i]['@lead'].upper())
            lead_data_string = raw_lead_data[i]['#text']
            lead_vals = [int(x) for x in lead_data_string.split(",")]
            leads[lead_n] = lead_vals

    return leads


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
    md['filter 50Hz'] = data['FilterSetting']['Filter50Hz']
    md['filter 60Hz'] = data['FilterSetting']['Filter60Hz']
    md['low pass'] = float(data['FilterSetting']['LowPass']['#text'])
    md['high pass'] = float(data['FilterSetting']['HighPass']['#text'])

    return md


if __name__ == '__main__':
    main()
