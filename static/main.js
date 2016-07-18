'use strict';
var config = {
    charge: -300,
    gravity: 0,
    linkDistance: 40,
    linkStrength: .3,
    friction: .4
};
var sg;
function init (json) {
    config.json = json;
    ServerGraph.init(config);
}

var ServerGraph = (function (SWPP) {
    var cluster_representatives = {},
        foci = [],
        ring_clusters = [],
        selected = null,
        focus_tick = null,
        theta = null,
        reset_foci = null,
        dispatch = null,
        selected_nodes = [];

    SWPP.preStart = function (force, svg, nodes, links) {
        function ring_foci_tick (t) {
            var height = svg.attr('height');
            var width = svg.attr('width');
            var r = Math.min(width, height) / 2;
            if (t) {
                theta = t;
            } else if (!theta) {
                theta = 0;
            }
            var offset = 2 * Math.PI / (foci.length);
            var a = 2 * Math.log(foci.length) * Math.log(foci.length);
            for (var i in foci) {
                foci[i] = {
                    'x': a * Math.cos(theta + i*offset - Math.PI/2) * r + width/2,
                    'y': 1.2 * Math.sin(theta + i*offset - Math.PI/2) * r + height*2
                }
            }
        }
        

        function selectCluster (id) {
            selected = id;
            dispatch.select(id);
        };

        function ring_shift_left () {
            force.alpha(.2);
            if (selected == 0 || selected) {
                ring_clusters.push(selected);
                foci.push({x:SWPP.getWidth()/2, y:SWPP.getHeight()/2});
            }
            selectCluster(ring_clusters.shift());
            foci.shift();
        };

        function ring_shift_right () {
            force.alpha(.2);
            if (selected == 0 || selected) {
                ring_clusters = [selected].concat(ring_clusters);
                foci = [{x:SWPP.getWidth()/2, y:SWPP.getHeight()/2}].concat(foci);
            }
            selectCluster(ring_clusters.pop());
            foci.pop();
        };

        function setRingFocus () {
            foci = [];
            ring_clusters = [];
            var i = 0;
            var swpp = this;
            SWPP.data.groups.forEach(function (g_id) {
                ring_clusters.push(g_id);
                foci.push({x:0, y:0});
            });
            focus_tick = ring_foci_tick;
        };

        SWPP.nodeTick = function (e, nodes) {
            nodes.attr("transform", function (d,i) {
                var focus, k;
                if (d.rep) {
                    var index = ring_clusters.indexOf(d.group);
                    if (index > -1) {
                        focus = foci[index];
                    } else {
                        focus = {x:SWPP.getWidth()/2,y:SWPP.getHeight()/2};
                    }
                    k = e.alpha * 1.2;
                } else {
                    var rep = cluster_representatives[d.group];
                    focus = {x:rep.x, y:rep.y};
                    k = e.alpha * .17;
                }
                var x = d.x - focus.x,
                    y = d.y - focus.y,
                    l = Math.sqrt(x*x + y*y);
                if (l > 1) {
                    l = l / l * k;
                    d.x -= x *= l;
                    d.y -= y *= l;
                }
                return ["translate(",d.x,",",d.y,")"].join(" ");
            });
        };

        force.on('tick', function (e) {
            focus_tick(0);
            SWPP.linkTick(e, links);
            SWPP.nodeTick(e, nodes);
        });

        // reference to cluster representative
        nodes.data().map(function (d,i) {
            if (cluster_representatives[d.group]) {
                d.rep = false;
            } else {
                d.rep = true;
                cluster_representatives[d.group] = d;
            }
        });

        setRingFocus();
        reset_foci = setRingFocus;

        // Hovering effects
        d3.selectAll(".node")
          .on("mouseover", function (d) {
             var text = d3.select(this).append("text")
                .attr('id', 'node' + d.id.toString())
                .attr("x", 12)
                .attr("dy", ".35em")
                .text(function (d) {
                    var t = document.createElement('a');
                    t.href = d.url;
                    t = t.hostname + t.pathname;
                    t = t.split('www.')
                    t = t.length > 1 ? t[1] : t[0];
                    return t;
             });
          })
          .on("mouseleave", function (d) {
             var node = d3.select(this)
             node.classed('hover', false);
             d3.selectAll('text#node'+d.id.toString()).remove();
          })
          .on("dblclick", function (d) {
             var win = window.open(d.url, '_blank');
             win.focus();
          });

        // Cluster Selected Events
        dispatch = d3.dispatch('select');
        dispatch.on('select', function (g_id) {
            var urlbox = d3.select("#urlbox");
            var nodes = d3.selectAll('.node')
                .filter(function (d) {return d.group == g_id;});
            urlbox.selectAll("li").remove()
            nodes.each(function (n) {
                urlbox.select("ul").append("li")
                    .text(n.url);
            });
        });

        // Key Events
        d3.select("body")
            .on('keydown', function () {
                if (d3.event.keyCode == 37) { // left
                    ring_shift_left();
                } else if (d3.event.keyCode == 39) { // right
                    ring_shift_right();
                }
            });
    }
    return SWPP;
})(SWPP || {});
