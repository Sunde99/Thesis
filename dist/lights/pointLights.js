"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createPointLights = void 0;
const THREE = __importStar(require("three"));
const createPointLights = (scene, lightCount, lightDistance, lights) => {
    for (let i = 0; i < lightCount; i++) {
        // Positions evenly in a circle pointed at the origin
        const light = new THREE.PointLight(0xffffff, 1);
        let lightX = lightDistance * Math.sin(((Math.PI * 2) / lightCount) * i);
        let lightZ = lightDistance * Math.cos(((Math.PI * 2) / lightCount) * i);
        // Create a light
        light.position.set(lightX, lightDistance, lightZ);
        light.lookAt(0, 0, 0);
        scene.add(light);
        lights.push(light);
        // Visual helpers to indicate light positions
        scene.add(new THREE.PointLightHelper(light, 0.5, 0xff9900));
    }
    return lights;
};
exports.createPointLights = createPointLights;
//# sourceMappingURL=pointLights.js.map