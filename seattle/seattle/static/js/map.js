L.mapbox.accessToken = 'pk.eyJ1IjoiamFjcXVlcyIsImEiOiJuRm9TWGYwIn0.ndryRT8IT0U94pHV6o0yng';

var sw = L.latLng(47.4849, -122.4347),
    ne = L.latLng(47.7414, -122.2406),
    bounds = L.latLngBounds(sw, ne);

// Initialize map
var map = L.mapbox.map('map', 'jacques.la14ofjk', {
    center: [47.6105411, -122.329726],
    zoom: 13,
    attributionControl: false,
    maxBounds: bounds,
    maxZoom: 17,
    minZoom: 12
});

map.addControl(L.mapbox.geocoderControl('mapbox.places', {
    keepOpen: true
}));
// Disable scrollwheel zoom
map.scrollWheelZoom.disable();

function graph() {
    var w = 960,
        h = 500,
        p = [30, 20, 40, 0],
        x = d3.scale.ordinal().rangeRoundBands([0, w - p[1] - p[3]]),
        y = d3.scale.linear().range([0, h - p[0] - p[2]]),
        z = d3.scale.ordinal().range(["#FDE668", "#FFBE1A", "#E09200"])
        yx = d3.scale.linear().range([0, h - p[0] - p[2]]),
        format = d3.time.format("%b %Y");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return "<span>" + d.y + "</span>";
        })

    var svg = d3.select(".graph").append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .append("svg:g")
        .attr("transform", "translate(" + p[3] + "," + (h - p[2]) + ")");

    var today = new Date();
    var past = new Date(today.getDate() - 365);
    // var past-year = (today.getDate() - 365);    //<<===== no need
    // var mm = today.getMonth()+1; //January is 0!   //<<===== no need
    // var yyyy = today.getFullYear();  //<<===== no need


    svg.call(tip);

    // Transpose the data into layers by type.
    var incidents = d3.layout.stack()(["fire", "mvi", "crime"].map(function(incident) {
        return data.map(function(d) {
          return {x: new Date(d.month), y: +d[incident]};
        });
    }));

    // Compute the x-domain (by date) and y-domain (by top).
    x.domain(incidents[0].map(function(d) { return d.x; }));
    y.domain([0, d3.max(incidents[incidents.length - 1], function(d) { return d.y0 + d.y; })]);
    yx.domain([d3.max(incidents[incidents.length - 1], function(d) { return d.y0 + d.y; }), 0]);

    // svg.append("line")
    //     .scale(x)
    //     .attr("x1", x(past))  //<<== change your code here
    //     .attr("y1", 0)
    //     .attr("x2", x(past))  //<<== and here
    //     .attr("y2", h - p[0] - p[2])
    //     .style("stroke-width", 2)
    //     .style("stroke", "red")
    //     .style("fill", "none");

    // Define the axes
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(20);

    // svg.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(" + 0 + "," + h - p[2] + ")")
    //     .call(xAxis)
    //     .selectAll("text")
    //     .attr("y", 0)
    //     .attr("x", 9)
    //     .attr("dy", ".35em")
    //     .attr("transform", "rotate(90)")
    //     .style("text-anchor", "start");

    var yAxis = d3.svg.axis()
        .scale(yx)
        .orient("left")
        .ticks(5);

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (p[1] + p[3] - 12) + "," + -(h - p[2] - p[0]) + ")")
        .call(yAxis)
        .selectAll("text")
        .style("text-anchor", "start")
        .attr("font-style", "italic");

    // Add a group for each cause.
    var incident = svg.selectAll("g.incident")
        .data(incidents)
        .enter().append("svg:g")
        .attr("class", "incident")
        .style("fill", function(d, i) { return z(i); });

    // Add a rect for each date.
    var rect = incident.selectAll("rect")
        .data(Object)
        .enter().append("svg:rect")
        .attr("x", function(d) { return x(d.x); })
        .attr("y", function(d) { return -y(d.y0) - y(d.y); })
        .attr("height", function(d) { return y(d.y); })
        .attr("width", x.rangeBand())
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

}

window.onload = graph();

// On move, recalculate center
map.on('moveend', function(e) {
    var center = map.getCenter();
    var lat = center.lat;
    var lng = center.lng;
    console.log(lat, lng);
    // IE: Uncaught TypeError: Cannot read property 'lat' of undefined
    $.ajax({
        url: "/ajax/",
        dataType: "json",
        data: { 'lat_cen': lat, 'lon_cen': lng},
    }).done(function(json) {
        // Update site contents with new data
        $(".crime").children().replaceWith(json.percentages.Crime);
        $(".fire").children().replaceWith(json.percentages.Fire);
        $(".accidents").children().replaceWith(json.percentages.MVI);
        $(".crime_count").contents().replaceWith(json.counts.Crime);
        $(".fire_count").contents().replaceWith(json.counts.Fire);
        $(".accidents_count").contents().replaceWith(json.counts.MVI);
        $(".count").contents().replaceWith(json.count);
        $(".lat").contents().replaceWith(json.lat);
        $(".lon").contents().replaceWith(json.lon);
        $(".neigh").contents().replaceWith(json.neigh);

        // Update graph
        data = json.output;
        if (json.output.length === 0) {
            $(".graph").children().replaceWith('No data available.')
        } else {
            $(".graph").contents().remove();
            graph();
        }
    });
});

