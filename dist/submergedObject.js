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
exports.getSubmergedObject = void 0;
const THREE = __importStar(require("three"));
const loadSubmergedObject = () => {
    // TODO Set up object loader
    // For now using a cube is ok
    // Creates the geometry + materials
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshPhongMaterial({ color: 0xff9900 });
    let cube = new THREE.Mesh(geometry, material);
    return cube;
};
const getSubmergedObject = () => {
    const submergedObject = loadSubmergedObject();
    submergedObject.position.y = 0.5;
    // Sets up outer bounds
    const maxXValue = 5;
    const minXValue = -5;
    const maxZValue = 5;
    const minZValue = -5;
    // Randomizes position and rotation
    const submergedObjectRotation = Math.random() * Math.PI * 2;
    submergedObject.position.x =
        Math.random() * (maxXValue - minXValue) + minXValue;
    submergedObject.position.z =
        Math.random() * (maxZValue - minZValue) + minZValue;
    submergedObject.rotation.setFromVector3(new THREE.Vector3(0, submergedObjectRotation, 0));
    return submergedObject;
};
exports.getSubmergedObject = getSubmergedObject;
//# sourceMappingURL=submergedObject.js.map