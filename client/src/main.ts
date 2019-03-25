import * as d3 from "d3";
import * as dagre from "dagre";
import * as dagreD3 from "dagre-d3";
import {MemoryLocation} from "./location"
// Input related code goes here

function getNodes(nodes: any): MemoryLocation[] {
  let nodes_list: MemoryLocation[] = [];
  Object.keys(nodes).forEach(key => {
    nodes_list.push(
      new MemoryLocation(key, nodes[key])
    );
  })
  return nodes_list
}

function readGraph(nodes: MemoryLocation[]): dagre.graphlib.Graph{
  var g = new dagre.graphlib.Graph;

  // Set an object for the graph label
  g.setGraph({});

  // Default to assigning a new object as a label for each new edge.
  g.setDefaultEdgeLabel(function() { return {}; });

  // Add nodes to the graph. The first argument is the node id. The second is
  // metadata about the node. In this case we're going to add labels to each of
  // our nodes.
  nodes.forEach(obj => {
    g.setNode(obj.id, {label: obj.id})
  })

  // Add edges to the graph.
  nodes.forEach(obj => {
    var ids: object = obj.references;
    Object.keys(ids).forEach((addr: string) => {
      if (addr === "0x0") return;
      g.setEdge(obj.id, addr, {label: (ids as any)[addr]});
    })
  })

  return g;
}
var debugAlignment: String;
var render: any;
var g: dagre.graphlib.Graph;

var graphLink: any = d3.select("#graphLink");
var link: string = "/dump"

fetch(link, { headers: { "Content-Type": "application/json; charset=utf-8" }})
  .then(res => res.text() // parse response as JSON (can be res.text() for plain response)
    .then(response => {
      var json: object = JSON.parse(response);
      g = readGraph(
        getNodes(json)
      );

      // Set margins, if not present
      // if (!g.graph().hasOwnProperty("marginx") && !g.graph().hasOwnProperty("marginy")) {
      //   g.graph().marginx = 20;
      //   g.graph().marginy = 20;
      //  }

      g.graph().transition = function(selection) {
        return selection.transition().duration(500);
      };

      d3.select("svg").call(render, g);
      
      // Set up zoom support
      var svg = d3.select("svg"),
          inner = d3.select("svg g"),
          zoom = d3.zoom().on("zoom", function() {
            inner.attr("transform", d3.event.transform);
          });
      svg.call(zoom as any);
    }).catch(e => {console.log(e)}))

var debugAlignmentRE: RegExp = /[?&]alignment=([^&]+)/;
var debugAlignmentMatch: RegExpMatchArray | null = window.location.search.match(debugAlignmentRE);
if (debugAlignmentMatch != null) debugAlignment = debugAlignmentMatch[1];

// Create and configure the renderer
render = new dagreD3.render() as any;
