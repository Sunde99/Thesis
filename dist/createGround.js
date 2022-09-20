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
exports.createGroundFromHeightmap = void 0;
const THREE = __importStar(require("three"));
const createGroundFromHeightmap = () => {
    const groundGeo = new THREE.PlaneGeometry(100, 100, 64, 64);
    const horizontalRepeat = 1;
    const verticalRepeat = 1;
    let disMap = new THREE.TextureLoader()
        .setPath('../heightmaps/')
        .load('testHeightMap.png');
    disMap.wrapS = disMap.wrapT = THREE.RepeatWrapping;
    disMap.repeat.set(horizontalRepeat, verticalRepeat);
    const groundMat = new THREE.MeshStandardMaterial({
        color: 0xff0000,
        wireframe: false,
        displacementMap: disMap,
        emissive: 0xff00ff,
        emissiveMap: disMap,
        displacementScale: 50,
    });
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.y = -0.5;
    groundMesh.castShadow = true;
    groundMesh.receiveShadow = true;
    return groundMesh;
};
exports.createGroundFromHeightmap = createGroundFromHeightmap;
//# sourceMappingURL=createGround.js.map