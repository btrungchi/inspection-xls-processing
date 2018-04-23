from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View

import sqlalchemy
import pandas as pd
import logging

from mainapp.postgresql import PostgreSQLHolder
from mainapp.postgresql import PostgreSQLHolderUtils
from mainapp.xlsparse import XlsParser


logger = logging.getLogger(__name__)

class InspectionView(View):

    def __init__(self):
        self.template = 'inspection-view.html'

    # Handle GET request for data tables
    def get(self, request, *args, **kwargs):
        try:
            table_name = request.GET.get('table', 'General Information')
            with PostgreSQLHolder.postgre_engine.begin() as connection:
                df_general_info = pd.read_sql(table_name, connection)
            html_table = df_general_info.to_html(classes=[
                "table", "table-bordered", "table-striped", "table-hover", "inspection-data-table"])
        except Exception as error:
            logger.warn("Get table '" + str(table_name) + "' with error: " + str(error))
            html_table = ""
        return render(request, self.template, {'datatable': html_table})

    # Handle POST request to drop all tables
    def drop_all(request):
        if request.method == 'POST':
            try:
                if 'action' in request.POST and request.POST['action'] == 'drop-all':
                    PostgreSQLHolderUtils.init_tables(PostgreSQLHolder.postgre_engine, drop_all=True)
                    logger.info("All tables dropped")
            except Exception as error:
                logger.warn("Drop all table failed with error: " + str(error))
        return HttpResponseRedirect("/")

    # Handle POST request to upload file
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return HttpResponseBadRequest("No file uploaded")
        else:
            try:
                filedata = request.FILES['file']
                filename = request.FILES['file'].name
                df_general_info, df_pom_info, df_pif_info, df_item_info, df_sip_elements = XlsParser.parse(
                    filedata)
            except Exception as error:
                logger.warn("Parse '" + filename + "' with error: " + str(error))
                return HttpResponseBadRequest("Invalid data format")

            try:
                # Connection context with a Transaction established
                with PostgreSQLHolder.postgre_engine.begin() as connection:
                    df_general_info.to_sql(
                        'General Information', connection, if_exists='append', index=False)
                    df_sip_elements.to_sql(
                        'SIP Elements', connection, if_exists='append', index=False)
                    df_pif_info.to_sql('PIF Info', connection,
                                       if_exists='append', index=False)
                    df_item_info.to_sql('Item Info', connection,
                                        if_exists='append', index=False)
                    df_pom_info.to_sql('POM Info', connection,
                                       if_exists='append', index=False)
            except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.DataError) as error:
                logger.warn("Store '" + filename + "' with error: " + str(error))
                return HttpResponseBadRequest("SQL Constraint Violation")
            return HttpResponse("OK")
