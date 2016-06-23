var SWPP = (function () {
    var swpp = {
        width: 1400,
        height: 700,
        links: [],
        nodes: [],
        hover: {},
        force: null,
    };
    swpp.init = function (id) {
        var width = swpp.width,
            height = swpp.height;

        var force = d3.layout.force()
            .charge(-120)
            .linkDistance(30)
            .size([width,height])
        swpp.force = force;

        var color = d3.scale.category20();

        var svg = d3.select("body").append("svg")
            .attr("width",width)
            .attr("height",height)
        
        d3.json(id + ".json", function (error, graph) {
            if (error) throw error;
            swpp.nodes = graph.nodes;
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
            var node = svg.selectAll(".node")
                .data(force.nodes())
              .enter().append("g")
                .attr("class", "node")
                .style("fill", function (d) {return color(d.group); })
                .call(force.drag);

            // add the nodes
            node.append("circle")
                .attr("r", 5);

            // add the curvy lines
            function tick() {
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

                node
                    .attr("transform", function(d) { 
                    return "translate(" + d.x + "," + d.y + ")"; });
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
