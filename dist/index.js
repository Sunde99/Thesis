"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const basicScene_1 = __importDefault(require("./basicScene"));
// sets up the scene
let scene = new basicScene_1.default();
scene.initialize();
// loops updates
function loop() {
    scene.camera.updateProjectionMatrix();
    scene.renderer.render(scene, scene.camera);
    scene.orbitals.update();
    requestAnimationFrame(loop);
}
// runs a continuous loop
loop();
//# sourceMappingURL=index.js.map