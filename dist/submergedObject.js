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
exports.placeSubmergedObjects = void 0;
const THREE = __importStar(require("three"));
const createBall = () => {
    const sphereGeometry = new THREE.SphereGeometry();
    const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xff0099 });
    let sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    return sphere;
};
const createBox = () => {
    const boxGeometry = new THREE.BoxGeometry(10, 10, 10);
    const boxMaterial = new THREE.MeshBasicMaterial({ color: 0xff9900 });
    let cube = new THREE.Mesh(boxGeometry, boxMaterial);
    return cube;
};
const loadSubmergedObjects = () => {
    // TODO Set up object loader
    // For now using a basic shapes is ok
    const submergedObjects = [];
    const amountOfObjects = 5; // Take this as param
    // Randomly creates the geometry + materials
    for (let i = 0; i < amountOfObjects; i++) {
        submergedObjects.push(createBox());
    }
    return submergedObjects;
};
const placeSubmergedObjects = () => {
    const submergedObjects = loadSubmergedObjects();
    // Sets up outer bounds
    const minXValue = -50;
    const maxXValue = 50;
    const minYValue = -1;
    const maxYValue = 30;
    const minZValue = -50;
    const maxZValue = 50;
    submergedObjects.forEach((submergedObject) => {
        submergedObject.position.y = 0.5;
        // Randomizes position and rotation
        const submergedObjectRotation = Math.random() * Math.PI * 2;
        submergedObject.position.x =
            Math.random() * (maxXValue - minXValue) + minXValue;
        submergedObject.position.y =
            Math.random() * (maxXValue - minXValue) + minXValue;
        submergedObject.position.z =
            Math.random() * (maxZValue - minZValue) + minZValue;
        submergedObject.rotation.setFromVector3(new THREE.Vector3(0, submergedObjectRotation, 0));
    });
    return submergedObjects;
};
exports.placeSubmergedObjects = placeSubmergedObjects;
//# sourceMappingURL=submergedObject.js.map