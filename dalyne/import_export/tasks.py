import xlrd
import os
import uuid
from core_module.models import ImportTable, ExportTable, CompanyMaster, User, CountryMaster, FilterDataModel
from dalyne import celery_app
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from datetime import datetime


@celery_app.task(bind=True)
def upload_excel_file_async(self, country_id, user_id, full_path, data_type):
    try:
        country_obj = CountryMaster.objects.get(id=country_id)
        user_obj = User.objects.get(id=user_id)
        book = xlrd.open_workbook(full_path)
        sheet_obj = book.sheet_by_index(0)
        max_rows = sheet_obj.nrows
        company_data = list()

        if data_type == 'export':
            export_data = list()
            for rowsCount in range(1, max_rows):
                try:
                    date_obj = datetime.strptime(sheet_obj.cell_value(rowsCount, 1), '%b %d, %Y')
                except:
                    date_obj = xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount, 1),
                                                              book.datemode).strftime('%Y-%m-%d %H:%M:%S')
                export_data.append(ExportTable(
                    SB_DATE=date_obj,
                    MONTH=sheet_obj.cell_value(rowsCount, 2),
                    YEAR=sheet_obj.cell_value(rowsCount, 3),
                    RITC=str(sheet_obj.cell_value(rowsCount, 4)).replace(".0", ""),
                    TWO_DIGIT=str(sheet_obj.cell_value(rowsCount, 5)).replace(".0", ""),
                    FOUR_DIGIT=str(sheet_obj.cell_value(rowsCount, 6)).replace(".0", ""),
                    RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount, 7),
                    commodity_description=sheet_obj.cell_value(rowsCount, 8),
                    UQC=sheet_obj.cell_value(rowsCount, 9),
                    QUANTITY=sheet_obj.cell_value(rowsCount, 10),
                    CURRENCY=sheet_obj.cell_value(rowsCount, 11),
                    UNT_PRICE_FC=sheet_obj.cell_value(rowsCount, 12),
                    INV_VALUE_FC=sheet_obj.cell_value(rowsCount, 13),
                    UNT_PRICE_INR=sheet_obj.cell_value(rowsCount, 14),
                    INVOICE_NO=str(sheet_obj.cell_value(rowsCount, 15)).replace(".0", ""),
                    SB_NO=str(sheet_obj.cell_value(rowsCount, 16)).replace(".0", ""),
                    UNIT_RATE_WITH_FOB=sheet_obj.cell_value(rowsCount, 17),
                    PER_UNT_FOB=sheet_obj.cell_value(rowsCount, 18),
                    FOB_INR=sheet_obj.cell_value(rowsCount, 19),
                    FOB_FC=sheet_obj.cell_value(rowsCount, 20),
                    FOB_USD=sheet_obj.cell_value(rowsCount, 21),
                    EXCHANGE_RATE=sheet_obj.cell_value(rowsCount, 22),
                    IMPORTER_NAME=sheet_obj.cell_value(rowsCount, 23),
                    IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 24),
                    COUNTRY_OF_ORIGIN=sheet_obj.cell_value(rowsCount, 25),
                    PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount, 26),
                    MODE_OF_PORT=sheet_obj.cell_value(rowsCount, 27),
                    PORT_OF_LOADING=sheet_obj.cell_value(rowsCount, 28),
                    PORT_CODE=sheet_obj.cell_value(rowsCount, 29),
                    EXPORTER_ID=str(sheet_obj.cell_value(rowsCount, 30)).replace(".0", ""),
                    EXPORTER_NAME=sheet_obj.cell_value(rowsCount, 31),
                    EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 32),
                    EXPORTER_CITY=sheet_obj.cell_value(rowsCount, 33),
                    EXPORTER_PIN=str(sheet_obj.cell_value(rowsCount, 34)).replace(".0", ""),
                    COUNTRY=country_obj,
                    created_by=user_obj
                )
                )
                company_name = sheet_obj.cell_value(rowsCount, 31)
                iec_code = str(sheet_obj.cell_value(rowsCount, 30)).replace(".0", "")
                if not CompanyMaster.objects.filter(Q(name=company_name) | Q(iec_code=iec_code)):
                    if iec_code in [None, '']:
                        iec_code = f"DALYNE{(str(uuid.uuid4())[-4:])}"
                    company_data.append(CompanyMaster(
                        name=company_name,
                        iec_code=iec_code,
                        created_by=user_obj
                    )
                    )

            ExportTable.objects.bulk_create(export_data)
            CompanyMaster.objects.bulk_create(company_data)
            try:
                os.remove(full_path)
            except:
                pass
            return

        elif data_type == 'import':
            import_data = list()
            for rowsCount in range(1, max_rows):

                import_data.append(ImportTable(
                    BE_DATE=xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount, 1),
                                                           book.datemode).strftime('%Y-%m-%d %H:%M:%S'),
                    MONTH=sheet_obj.cell_value(rowsCount, 2),
                    YEAR=sheet_obj.cell_value(rowsCount, 3),
                    RITC=sheet_obj.cell_value(rowsCount, 4),
                    TWO_DIGIT=sheet_obj.cell_value(rowsCount, 5),
                    FOUR_DIGIT=sheet_obj.cell_value(rowsCount, 6),
                    RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount, 7),
                    UQC=sheet_obj.cell_value(rowsCount, 8),
                    QUANTITY=sheet_obj.cell_value(rowsCount, 9),
                    CURRENCY=sheet_obj.cell_value(rowsCount, 10),
                    UNT_PRICE_FC=sheet_obj.cell_value(rowsCount, 11),
                    INV_VALUE_FC=sheet_obj.cell_value(rowsCount, 12),
                    UNT_PRICE_INR=sheet_obj.cell_value(rowsCount, 13),
                    INV_NO=sheet_obj.cell_value(rowsCount, 14),
                    BE_NO=sheet_obj.cell_value(rowsCount, 15),
                    UNT_RATE_WITH_DUTY=sheet_obj.cell_value(rowsCount, 16),
                    PER_UNT_DUTY=sheet_obj.cell_value(rowsCount, 17),
                    DUTY_INR=sheet_obj.cell_value(rowsCount, 18),
                    DUTY_FC=sheet_obj.cell_value(rowsCount, 19),
                    DUTY_PERCENT=sheet_obj.cell_value(rowsCount, 20),
                    EX_TOTAL_VALUE=sheet_obj.cell_value(rowsCount, 21),
                    ASS_VALUE_INR=sheet_obj.cell_value(rowsCount, 22),
                    ASS_VALUE_USD=sheet_obj.cell_value(rowsCount, 23),
                    ASS_VALUE_FC=sheet_obj.cell_value(rowsCount, 24),
                    EXCHANGE_RATE=sheet_obj.cell_value(rowsCount, 25),
                    EXPORTER_NAME=sheet_obj.cell_value(rowsCount, 26),
                    EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 27),
                    COUNTRY_OF_ORIGIN=sheet_obj.cell_value(rowsCount, 28),
                    PORT_OF_LOADING=sheet_obj.cell_value(rowsCount, 29),
                    PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount, 30),
                    PORT_CODE=sheet_obj.cell_value(rowsCount, 31),
                    MODE_OF_PORT=sheet_obj.cell_value(rowsCount, 32),
                    IMPORTER_ID=sheet_obj.cell_value(rowsCount, 33),
                    IMPORTER_NAME=sheet_obj.cell_value(rowsCount, 34),
                    IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 35),
                    IMPORTER_CITY_STATE=sheet_obj.cell_value(rowsCount, 36),
                    IMPORTER_PIN=sheet_obj.cell_value(rowsCount, 37),
                    IMPORTER_PHONE=sheet_obj.cell_value(rowsCount, 38),
                    IMPORTER_EMAIL=sheet_obj.cell_value(rowsCount, 39),
                    IMPORTER_CONTACT_PERSON=sheet_obj.cell_value(rowsCount, 40),
                    BE_TYPE=sheet_obj.cell_value(rowsCount, 41),
                    CHA_NAME=sheet_obj.cell_value(rowsCount, 42),
                    Item_No=sheet_obj.cell_value(rowsCount, 43),
                    COUNTRY=country_obj,
                    created_by=user_obj
                )
                )
                company_name = sheet_obj.cell_value(rowsCount, 34)
                iec_code = sheet_obj.cell_value(rowsCount, 33)

                if not CompanyMaster.objects.filter(Q(name=company_name) | Q(iec_code=iec_code)):
                    iec_code = sheet_obj.cell_value(rowsCount, 33)
                    if iec_code in [None, '']:
                        iec_code = f"DALYNE{(str(uuid.uuid4())[-4:])}"
                    company_data.append(CompanyMaster(
                        name=sheet_obj.cell_value(rowsCount, 34),
                        iec_code=iec_code,
                        created_by=user_obj

                    )
                    )
            ImportTable.objects.bulk_create(import_data)
            CompanyMaster.objects.bulk_create(company_data)
            try:
                os.remove(full_path)
            except:
                pass
            return

    except Exception as e:
        print(e.__str__())
        return


@celery_app.task(bind=True)
def upload_company_file_async(self, file_name, company_file, user_id):
    try:
        fs = FileSystemStorage('media/import_export/')
        file_extension = file_name.split('.')[1].lower()
        filename = fs.save(
            file_name.split('.')[0].lower() + '_' + str(str(uuid.uuid4())[-4:]) + '.' + file_extension, company_file
        )
        full_path = f"{fs.location}/{filename}"
        print(f"Full Path {full_path}")
        user_obj = User.objects.get(id=user_id)
        book = xlrd.open_workbook(full_path)
        sheet_obj = book.sheet_by_index(0)
        max_rows = sheet_obj.nrows
        companies_list = list()
        for rows_count in range(1, max_rows):
            companies_list.append(CompanyMaster(
                name=sheet_obj.cell_value(rows_count, 0),
                iec_code=sheet_obj.cell_value(rows_count, 1),
                created_by=user_obj
            ))
        CompanyMaster.objects.bulk_create(companies_list)
        try:
            os.remove(full_path)
        except:
            pass
        return
    except Exception as e:
        print(e.__str__())
        return
