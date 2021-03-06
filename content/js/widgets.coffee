class window.Controls.chart extends window.Control
    createDom: () ->
        w = @_int_to_px(@properties.width)
        h = @_int_to_px(@properties.height)
        """
        <div style="width: #{w}; height: #{h};"></div>
        """

    setupDom: (dom) ->
        super(dom)

        window.Highcharts.setOptions
            global:
                useUTC: false

        @chart ||= new window.Highcharts.Chart
            chart:
                renderTo: @dom
                type: @properties.type
                backgroundColor: 'rgb(250, 250, 250)'
            title:
                text: @properties.title
            subtitle:
                text: @properties.subtitle
            xAxis: @properties.xaxis
            yAxis: @properties.yaxis
            series: @properties.series

        series = @chart.series
        data = []
        for point in @properties.data
            x = point[0]
            for j in [1..point.length] by 1
                (data[j-1] ||= []).push([x, point[j]])

        for serie, i in series
            serie.setData(data[i], false)

        @chart.redraw()

        return this
