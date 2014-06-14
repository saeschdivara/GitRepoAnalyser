


class StdoutExporter(object):

    def __init__(self):
        """
        """

        pass


class ChartExporter(object):

    EXPORT_TYPE = {
        "PIE": 1,
        "SPLINE": 2,
    }


    def __init__(self, type):
        """
        """

        self.type = type


    def export(self, data_list):
        """
        """

        if self.type is ChartExporter.EXPORT_TYPE['PIE']:
            template = self._pie_chart_template()
            javascript = self._create_pie_chart_javascript(data_list=data_list)

            complete_html = template.replace('{{ javascript }}', javascript)

            chart_file = file('web/statics/pie_chart.html', mode='w')
            chart_file.write(complete_html)
            chart_file.close()

        elif self.type is ChartExporter.EXPORT_TYPE['SPLINE']:
            template = self._spline_chart_template()
            javascript = self._create_spline_chart_javascript(data_list=data_list)

            complete_html = template.replace('{{ javascript }}', javascript)

            chart_file = file('web/statics/spline_chart.html', mode='w')
            chart_file.write(complete_html)
            chart_file.close()


    def _create_pie_chart_javascript(self, data_list):
        """
        """

        javascript = ''

        for index, report_data in enumerate(data_list):
            javascript += "['%s', %s.0]," % (report_data.display_name, report_data.data)


        return  javascript


    def _pie_chart_template(self):

        standard_template = self._standard_template()

        basic_pie_chart_javascript = """
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Browser market shares at a specific website, 2014'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [
                {
                    type: 'pie',
                    name: 'Browser share',
                    data: [
                        {{ javascript }}
                    ]
                }
            ]
        """

        template = standard_template.replace('{{ HIGH_CHARTS_OBJECT }}', basic_pie_chart_javascript)

        return template


    def _create_spline_chart_javascript(self, data_list):
        """
        """

        javascript = ''

        javascript_template = """

                {
                    name: '{{ LINE_NAME }}',
                    data: [
                        {{ DATA_LIST }}
                    ]
                },
        """

        for index, report_data in enumerate(data_list):
            data_string_list = ''

            for time_data in report_data.data:
                data_string_list += "[Date.UTC(%s), %s]," % (time_data.display_name, time_data.data)

            clone_template = javascript_template.replace('{{ LINE_NAME }}', report_data.display_name)
            clone_template = clone_template.replace('{{ DATA_LIST }}', data_string_list)

            javascript += clone_template

        return javascript


    def _spline_chart_template(self):
        """
        """

        standard_template = self._standard_template()

        basic_spline_chart_javascript = """
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Commits per day of an author'
            },
            subtitle: {
                text: 'Irregular time data in Highcharts JS'
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    month: '%e. %b',
                    year: '%b'
                },
                title: {
                    text: 'Date'
                }
            },
            yAxis: {
                title: {
                    text: 'Commit number'
                },
                min: 0,
                max: 60
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y}'
            },

            series: [
                {{ javascript }}
            ]
        """

        template = standard_template.replace('{{ HIGH_CHARTS_OBJECT }}', basic_spline_chart_javascript)

        return template


    def _standard_template(self):
        """
        """

        template = """
            <!DOCTYPE HTML>
                <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <title>Highcharts Example</title>

                    <script type="text/javascript" src="3rdparty/javascript/jquery/jquery-1.11.0.min.js"></script>
                    <script type="text/javascript">
                        $(function () {
                            var chart;

                            $(document).ready(function () {

                                // Build the chart
                                $('#container').highcharts({

                                    {{ HIGH_CHARTS_OBJECT }}

                                });
                            });

                        });
                    </script>
                </head>
                <body>
                <script src="3rdparty/javascript/highcharts/js/highcharts.js"></script>
                <script src="3rdparty/javascript/highcharts/js/modules/exporting.js"></script>

                <div id="container" style="min-width: 310px; height: 800px; margin: 0 auto"></div>

                </body>
            </html>
        """

        return template