import pandas as pd

class XlsParser:

    @staticmethod
    def parse(xlsfile):
        dict_df_excel = pd.read_excel(
            xlsfile, sheet_name=["Inspection Detail", "PIF Detail - FRI"], header=None)
        df_inspection = dict_df_excel["Inspection Detail"]
        df_pif_detail = dict_df_excel["PIF Detail - FRI"]
        df_general_info = XlsParser.parse_general_info(df_inspection)
        df_pom_info = XlsParser.parse_pom_info(df_inspection)
        df_pif_info = XlsParser.parse_pif_info(df_pif_detail)
        df_item_info = XlsParser.parse_item_info(df_pif_detail)
        df_sip_elements = XlsParser.parse_sip_elements(df_pif_detail)
        return df_general_info, df_pom_info, df_pif_info, df_item_info, df_sip_elements

    @staticmethod
    def parse_general_info(df_inspection):
        df_general_info_raw = df_inspection[:7].transpose()
        # strip ending colons and whitespaces
        df_general_info_raw = df_general_info_raw.applymap(
            lambda x: x.rstrip(": ") if isinstance(x, str) else x)
        # set dataframe header
        df_general_info_raw = df_general_info_raw.rename(
            columns=df_general_info_raw.iloc[0])[1:]

        series_date = df_general_info_raw["Date"]
        date = series_date[1]

        series_vendor = df_general_info_raw["Vendor"]
        vendor = series_vendor[1]
        vendor_name = series_vendor[2]
        bmp_vendor = series_vendor[series_vendor.eq(
            'BPM Vendor(s)').idxmax()+1]

        series_vdr_contacts = df_general_info_raw["Vdr Contacts"]
        vdr_contacts = series_vdr_contacts[1]

        series_factory = df_general_info_raw["Factory"]
        factory = series_factory[1]
        factory_name = series_factory[2]
        frm_level = series_factory[series_factory.eq(
            'FRM Level').idxmax()+1]

        series_fty_address = df_general_info_raw["Fty Address"]
        fty_address = series_fty_address[1]

        series_fty_contacts = df_general_info_raw["Fty Contacts"]
        fty_contacts = series_fty_contacts[1]

        series_auditor = df_general_info_raw["Auditor"]
        auditor = series_auditor[1]

        df_general_info = pd.DataFrame([[date, vendor, bmp_vendor, vdr_contacts, factory, fty_address, fty_contacts, auditor, frm_level]],
                                        columns=["Date", "Vendor", "BMP Vendor", "Vdr Contacts", "Factory", "Fty Address", "Fty Contacts", "Auditor", "FRM Lebel"])
        return df_general_info

    @staticmethod
    def parse_pom_info(df_inspection):
        df_pom_info = df_inspection.iloc[11:]
        # remove 2 last columns
        df_pom_info = df_pom_info.drop(
            df_pom_info.columns[[-1, -2]], axis=1)
        # set dataframe header
        df_pom_info = df_pom_info.rename(columns=df_pom_info.iloc[0])[1:]
        # process the header
        df_pom_info.columns = list(map(lambda x: x.strip().replace(
            '\n', ' ') if isinstance(x, str) else x, df_pom_info.columns))
        # remove rows which do not have first three values
        df_pom_info = df_pom_info.dropna(
            subset=['PID/Style', 'DPCI', 'PO Included'], how='any')
        return df_pom_info

    @staticmethod
    def parse_pif_info(df_pif_detail):
        df_pif_info = df_pif_detail.iloc[2:, :6]
        # replace '\n' with whitespace
        df_pif_info = df_pif_info.applymap(
            lambda x: x.replace('\n', ' ') if isinstance(x, str) else x)
        # remove empty rows, colums
        df_pif_info = df_pif_info.dropna(axis=[0, 1], how='all')
        # set dataframe header
        df_pif_info = df_pif_info.rename(columns=df_pif_info.iloc[0])[1:]
        return df_pif_info

    @staticmethod
    def parse_item_info(df_pif_detail):
        df_item_info = df_pif_detail.iloc[2:, 6:14]
        # remove empty rows, colums
        df_item_info = df_item_info.dropna(axis=[0, 1], how='all')
        # set dataframe header
        df_item_info = df_item_info.rename(
            columns=df_item_info.iloc[0])[1:]
        return df_item_info

    @staticmethod
    def parse_sip_elements(df_pif_detail):
        df_sip_elements = df_pif_detail.iloc[2:, 21:38]
        # remove empty rows, colums
        df_sip_elements = df_sip_elements.dropna(axis=[0, 1], how='all')
        # set dataframe header
        df_sip_elements = df_sip_elements.rename(
            columns=df_sip_elements.iloc[0])[1:]
        return df_sip_elements
