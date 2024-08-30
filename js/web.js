import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
  name: "00_kento_nodes",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "ChainFileReader") {
      const origOnNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = origOnNodeCreated ? origOnNodeCreated.apply(this) : undefined;
        for (const w of this.widgets) {
          if (w.name === "seed") {
            w.type = "converted-widget";
            if (!w.linkedWidgets) continue;
            for (const lw of w.linkedWidgets) {
              lw.type = "converted-widget";
            }
          }
        }
        return r;
      }
    }
  }
})