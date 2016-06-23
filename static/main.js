'use strict';
var SWPP = (function () {
    var swpp = {
        width: 1400,
        height: 700,
        data: null,
        links: [],
        nodes: [],
        hover: {},
        force: null,
        cluster_foci: {},
        foci: [],
        focus_tick: null,
        theta: null,
    };

    var init_focus_tick = function () {
        swpp.setRingFocus();
        return ring_foci_tick;
    }

    function ring_foci_tick (theta) {
        var r = Math.min(swpp.width, swpp.height) / 3;
        if (theta) {
            swpp.theta = theta;
        } else if (!swpp.theta) {
            swpp.theta = 0;
        }
        var theta = swpp.theta;
        theta += Math.log(swpp.foci.length) / 2500;
        var offset = 2 * Math.PI / (swpp.foci.length)
        for (var i in swpp.foci) {
            swpp.foci[i] = {
                'x': Math.cos(theta + i*offset) * r + swpp.width/2,
                'y': Math.sin(theta + i*offset) * r + swpp.height
            }
        }
        swpp.theta = theta;
        swpp.force.alpha(.1);
    }

    swpp.setRingFocus = function () {
        if (swpp.data) {
            swpp.foci = [];
            var i = 0;
            swpp.data.groups.forEach(function (g_id) {
                swpp.cluster_foci[g_id] = i;
                swpp.foci.push({x:0, y:0});
                i += 1;
            });
            swpp.focus_tick = ring_foci_tick(0);
        }
    }

    swpp.init = function (id) {
        var width = swpp.width,
            height = swpp.height;

        var force = d3.layout.force()
            .charge(-120)
            .gravity(0)
            .linkDistance(30)
            .size([width,height])
        swpp.force = force;

        var color = d3.scale.category20();
        var svg = d3.select("body").append("svg")
            .attr("width",width)
            .attr("height",height)

        d3.json(id + ".json", function (error, json) {
            if (error) reject(error);
            swpp.data = json;
            var graph = json;
            swpp.nodes = graph.nodes;
            for (var i in graph.groups) {
                swpp.cluster_foci[graph.groups[i]] = {'x':width/2, 'y':height/2};
            }
            graph.links.forEach(function (e) {
                var sourceNode = graph.nodes.find(function (n) {
                    return n.id === e.source;
                });
                var targetNode = graph.nodes.find(function (n) {
                    return n.id === e.target;
                });
                swpp.links.push({
                    source: sourceNode,
                    target: targetNode,
                    value: e.value
                });
            });
            force
                .nodes(swpp.nodes)
                .links(swpp.links)
                .on("tick", tick)
                .start();

            // build the arrow.
            svg.append("svg:defs").selectAll("marker")
                .data(["end"])      // Different link/path types can be defined here
              .enter().append("svg:marker")    // This section adds in the arrows
                .attr("id", String)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 15)
                .attr("refY", -1.5)
                .attr("markerWidth", 6)
                .attr("markerHeight", 6)
                .attr("orient", "auto")
              .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5");

            // add the links and the arrows
            var path = svg.append("svg:g").selectAll("path")
                .data(force.links())
              .enter().append("svg:path")
            //    .attr("class", function(d) { return "link " + d.type; })
                .attr("class", "link")
                .attr("marker-end", "url(#end)");

            // define the nodes
            var nodes = svg.selectAll(".node")
                .data(force.nodes())
              .enter().append("g")
                .attr("class", "node")
                .attr("cx", function (d) {return d.x;})
                .attr("cy", function (d) {return d.y;})
                .style("fill", function (d) {return color(d.group); })
                .call(force.drag);

            // add the nodes
            nodes.append("circle")
                .attr("r", 5);

            swpp.focus_tick = init_focus_tick();
            // DEFINE ticks
            function tick(e) {
                swpp.focus_tick(0);
                path.attr("d", function(d) {
                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,
                        dr = Math.sqrt(dx * dx + dy * dy);
                    return "M" + 
                        d.source.x + "," + 
                        d.source.y + "A" + 
                        dr + "," + dr + " 0 0,1 " + 
                        d.target.x + "," + 
                        d.target.y;
                });
                
                nodes.attr("transform", function (d, i) {
                    var focus = swpp.foci[swpp.cluster_foci[d.group]];
                    var x = d.x - focus.x,
                        y = d.y - focus.y,
                        l = Math.sqrt(x*x + y*y);
                    if (l > 1) {
                        l = l / l * e.alpha;
                        d.x -= x *= l;
                        d.y -= y *= l;
                    }
                    return ["translate(",d.x,",",d.y,")"].join(" ");
                });
            }

            // Hovering effects
            d3.selectAll(".node")
              .on("mouseover", function () {
                 id = d3.select(this).data()[0].id;
                 var text = d3.select(this).append("text")
                    .attr('id', 'node' + id.toString())
                    .attr("x", 12)
                    .attr("dy", ".35em")
                    .text(function (d) {
                        var t = document.createElement('a');
                        t.href = d.url;
                        t = t.hostname + t.pathname;
                        t = t.split('www.')
                        t = t.length > 1 ? t[1] : t[0];
                        return t.substring(0, 30);
                    });
              })
              .on("mouseleave", function () {
                 var node = d3.select(this)
                 node.classed('hover', false);
                 id = node.data()[0].id;
                 d3.selectAll('text#node'+id.toString()).remove();
              });
        });
    };
    return swpp;
}());
