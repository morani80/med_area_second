# -*- coding: utf-8 -*-

import itertools
import logging
import os
import pandas as pd

class CsvParser:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def extract_second_area_from_csv(self, csv_file_path: str, out_dir: str = './output', readonly: bool = False):
        """
        Extract town data with area2 from csv file 
        Just want to check the content of the csv, set readonly=True.
        """

        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html#pandas.read_csv
        df = pd.read_csv(csv_file_path, encoding='cp932', header=None, skiprows=2,
                         usecols=[5], names=['cd_name'], dtype=str, na_filter=False)
        df = df['cd_name'].str.split(n=1, expand=True).rename(columns={0: 'town_cd', 1: 'town_name'})

        # add area2
        df['area2_cd'] = ''
        df['area2_name'] = ''
        area2_cd = ''
        area2_name = ''
        for _, s in df.iterrows():
            if len(s['town_cd']) == 4:
                area2_cd = s['town_cd']
                area2_name = s['town_name']
            s['area2_cd'] = area2_cd
            s['area2_name'] = area2_name

        # add prefecture
        pref_df = df[df['town_cd'].str.len() == 2]
        pref_dict = dict(zip(pref_df['town_cd'], pref_df['town_name']))
        df['pref_cd'] = df['town_cd'].str[:2]
        df['pref_name'] = df['pref_cd'].map(pref_dict)

        # filter only town data
        df = df[df['town_cd'].str.len() == 5]
        if readonly:
            self._logger.debug(df)
        else:
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            csv_file_path = os.path.join(out_dir, 'med_area2.csv')
            df.to_csv(csv_file_path, header=False, index=False)


if __name__ == '__main__':

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    # handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(filename)-12s: %(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    try:
        _logger.debug("start~~")

        parser = CsvParser()
        csv_f = r".\tmp_data\FEH_00450021_200629102936.csv"
        parser.extract_second_area_from_csv(csv_f)

        _logger.debug("fin.")

    except Exception as e:
        _logger.exception(e)
