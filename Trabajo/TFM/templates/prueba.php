{% load static %}

<!DOCTYPE HTML>
<html>

<head>
	{% load static %}

	<title>TFM</title>
	<script src="https://code.highcharts.com/highcharts.js"></script>
	<script src="https://code.highcharts.com/modules/data.js"></script>
	<script src="https://code.highcharts.com/modules/exporting.js"></script>
	<script src="https://code.highcharts.com/modules/export-data.js"></script>
	
</head>
    
<body>

	<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

	<table id="datatable">
		<thead>
			<tr>
				<th></th>
				<th>Sufre Episodio</th>
				<th>No Sufre Episodio</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<th>2016</th>
				<td>2</td>
				<td>4</td>
			</tr>
			<tr>
				<th>2017</th>
				<td>1</td>
				<td>1</td>
			</tr>
			<tr>
				<th>2008</th>
				<td>2</td>
				<td>2</td>
			</tr>
			<tr>
				<th>2009</th>
				<td>3</td>
				<td>3</td>
			</tr>
				<tr>
				<th>2010</th>
				<td>3</td>
				<td>4</td>
			</tr>
			<tr>
				<th>2011</th>
				<td>4</td>
				<td>2</td>
			</tr>
			<tr>
				<th>2012</th>
				<td>3</td>
				<td>6</td>
			</tr>
			<tr>
				<th>2013</th>
				<td>3</td>
				<td>1</td>
			</tr>
			<tr>
				<th>2014</th>
				<td>5</td>
				<td>2</td>
			</tr>
			<tr>
				<th>2015</th>
				<td>4</td>
				<td>5</td>
			</tr>
		</tbody>
	</table>
	
</body>

<script>

Highcharts.chart('container', {
	data: {
		table: 'datatable'
	},
	chart: {
		type: 'column'
	},
	title: {
		text: 'Histórico de los pacientes'
	},
	yAxis: {
		allowDecimals: false,
		title: {
		text: 'Units'
		}
	},
	tooltip: {
		formatter: function () {
			return '<b>' + this.series.name + '</b><br/>' +
			this.point.y + ' en ' + this.key;
		}
	}
});
	
</script>

</html>

