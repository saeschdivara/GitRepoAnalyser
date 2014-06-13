


class StdoutExporter(object):

    def __init__(self):
        """
        """

        pass


class ChartExporter(object):

    EXPORT_TYPE = {
        "PIE": 1
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

            chart_file = file('web/statics/foo.html', mode='w')
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

                <div id="container" style="min-width: 310px; height: 400px; max-width: 600px; margin: 0 auto"></div>

                </body>
            </html>
        """

        return template