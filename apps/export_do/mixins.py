from django.http import HttpResponse
import csv
#import xlwt


class ExportDocsMixin:

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        fields_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta.verbose_name_plural)
        writer = csv.writer(response)

        writer.writerow(fields_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in fields_names])

        return response

    def export_as_xls(self, request, queryset):

        meta = self.model._meta

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta.verbose_name_plural)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(meta.verbose_name_plural)

        row_num_first = 0
        col_num_first = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.font.italic = True

        ws.write(row_num_first, col_num_first, self.title_to_print, font_style)

        row_num = 1
        columns_name = [field.verbose_name for field in meta.fields]
        columns = [field.name for field in meta.fields]
        font_style.font.italic = False

        for col_num in range(len(columns_name)):
            ws.write(row_num, col_num, columns_name[col_num], font_style)

        font_style = xlwt.XFStyle()
        for obj in queryset:
            row_num += 1
            col_num = 0
            for field_data in ([getattr(obj, field) for field in columns]):
                ws.write(row_num, col_num, str(field_data), font_style)
                col_num += 1

        wb.save(response)
        return response

    def export_as_pdf(self, request, queryset):

        meta = self.model._meta
        fields_name = [field.name for field in meta.fields]

    export_as_csv.short_description = "Exportar seleccionados a CSV"
    export_as_xls.short_description = "Exportar seleccionados a XLS"
    export_as_pdf.short_description = "Exportar seleccionados a PDF"
