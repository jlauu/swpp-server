'use strict';
var config = {
    charge: -120,
    gravity: 0,
    linkDistance: 30,
    linkStrength: .2,
    friction: .85
};
var sg;
function init (json) {
    config.json = json;
    var ServerGraph = SWPP(mixin);
    sg = ServerGraph.getInstance(config);
    sg.start();
}

var mixin = (function () {
    var cluster_representatives = {};
    var foci = [];
    var ring_clusters = [];
    function extension(SWPPGraph) {
        SWPPGraph.prototype.ring_foci_tick = function (theta) {
            var r = Math.min(this.width, this.height) / 2;
            if (theta) {
                this.theta = theta;
            } else if (!this.theta) {
                this.theta = 0;
            }
            var theta = this.theta;
    /*        theta += Math.log(this.foci.length) / 2500;*/
            var offset = 2 * Math.PI / (foci.length);
            var a = 2 * Math.log(foci.length) * Math.log(foci.length);
            for (var i in foci) {
                foci[i] = {
                    'x': a * Math.cos(theta + i*offset - Math.PI/2) * r + this.width/2,
                    'y': 1.2 * Math.sin(theta + i*offset - Math.PI/2) * r + this.height*2
                }
            }
        }

        SWPPGraph.prototype.tick = function () {
            var swpp = this;
            return function (e) {
                swpp.focus_tick(0);
                swpp.path.attr("d", function (d) {
                    var dx = d.target.x - d.source.x,
                        dy = d.target.y - d.source.y,
                        dr = Math.sqrt(dx * dx + dy * dy);
                    return "M" +
                        d.source.x + "," +
                        d.source.y + "A" +
                        dr + "," + dr + " 0 0,1" +
                        d.target.x + "," +
                        d.target.y;
                });
                swpp.nodes.attr("transform", function (d,i) {
                    var focus, k;
                    if (d.rep) {
                        var index = ring_clusters.indexOf(d.group);
                        if (index > -1) {
                            focus = foci[index];
                        } else {
                            focus = {x:swpp.width/2,y:swpp.height/2};
                        }
                        k = e.alpha * 1.5;
                    } else {
                        var rep = cluster_representatives[d.group];
                        focus = {x:rep.x, y:rep.y};
                        k = e.alpha * .2;
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
        };

        SWPPGraph.prototype.selectCluster = function (id) {
            this.selected = id;
            this.dispatch.select(id);
        };

        SWPPGraph.prototype.ring_shift_left = function () {
            this.force.alpha(.2);
            if (this.selected == 0 || this.selected) {
                ring_clusters.push(this.selected);
                foci.push({x:this.width/2, y:this.height/2});
            }
            this.selectCluster(ring_clusters.shift());
            foci.shift();
        };

        SWPPGraph.prototype.ring_shift_right = function () {
            this.force.alpha(.2);
            if (this.selected == 0 || this.selected) {
                ring_clusters = [this.selected].concat(ring_clusters);
                foci = [{x:this.width/2, y:this.height/2}].concat(foci);
            }
            this.selectCluster(ring_clusters.pop());
            foci.pop();
        };

        SWPPGraph.prototype.setRingFocus = function () {
            if (this.data) {
                foci = [];
                ring_clusters = [];
                var i = 0;
                var swpp = this;
                this.data.groups.forEach(function (g_id) {
                    ring_clusters.push(g_id);
                    foci.push({x:0, y:0});
                });
                this.focus_tick = this.ring_foci_tick;
            }
        };

        SWPPGraph.prototype.postStart = function () {
            this.selected = null; // cluster id
            this.focus_tick = null;
            this.theta = null;
            this.reset_foci = null;
            this.dispatch = null;
            this.selected_nodes = [];
            var swpp = this;
            // reference to cluster representative
            this.nodes.data().map(function (d,i) {
                if (cluster_representatives[d.group]) {
                    d.rep = false;
                } else {
                    d.rep = true;
                    cluster_representatives[d.group] = d;
                }
            });

            this.setRingFocus();
            this.reset_foci = this.setRingFocus;
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
              });

            // Cluster Selected Events
            this.dispatch = d3.dispatch('select');
            this.dispatch.on('select', function (g_id) {
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
                        swpp.ring_shift_left();
                    } else if (d3.event.keyCode == 39) { // right
                        swpp.ring_shift_right();
                    }
                });
            this.force.start();
        }
    }
    return {
        extension: extension
    };
})();

