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
const THREE = __importStar(require("three"));
const dat_gui_1 = require("dat.gui");
const OrbitControls_1 = require("three/examples/jsm/controls/OrbitControls");
const submergedObject_1 = require("./submergedObject");
// import { createGroundFromHeightmap } from './createGround'
/**
 * A class to set up some basic scene elements to minimize code in the
 * main execution file.
 */
class BasicScene extends THREE.Scene {
    constructor() {
        super(...arguments);
        // A dat.gui class debugger that is added by default
        this.debugger = null;
        // Setups a scene camera
        this.camera = null;
        // setup renderer
        this.renderer = null;
        // setup Orbitals
        this.orbitals = null;
        // Holds the lights for easy reference
        this.lights = [];
        // Number of PointLight objects around origin
        this.lightCount = 6;
        // Distance above ground place
        this.lightDistance = 3;
        // Get some basic params
        this.width = window.innerWidth;
        this.height = window.innerHeight;
    }
    /**
     * Initializes the scene by adding lights, and the geometry
     */
    initialize(debug = true, addGridHelper = true) {
        // setup camera
        this.camera = new THREE.PerspectiveCamera(35, this.width / this.height, 0.1, 1000);
        this.camera.position.z = 12;
        this.camera.position.y = 12;
        this.camera.position.x = 12;
        // setup renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: document.getElementById('app'),
            alpha: true,
        });
        this.renderer.setSize(this.width, this.height);
        // add window resizing
        BasicScene.addWindowResizing(this.camera, this.renderer);
        // sets up the camera's orbital controls
        this.orbitals = new OrbitControls_1.OrbitControls(this.camera, this.renderer.domElement);
        // Adds an origin-centered grid for visual reference
        if (addGridHelper) {
            // Adds a grid
            this.add(new THREE.GridHelper(10, 10, 'red'));
            // Adds an axis-helper
            this.add(new THREE.AxesHelper(3));
        }
        // set the background color
        this.background = new THREE.Color(0xefefef);
        // create the lights
        for (let i = 0; i < this.lightCount; i++) {
            // Positions evenly in a circle pointed at the origin
            const light = new THREE.PointLight(0xffffff, 1);
            let lightX = this.lightDistance * Math.sin(((Math.PI * 2) / this.lightCount) * i);
            let lightZ = this.lightDistance * Math.cos(((Math.PI * 2) / this.lightCount) * i);
            // Create a light
            light.position.set(lightX, this.lightDistance, lightZ);
            light.lookAt(0, 0, 0);
            this.add(light);
            this.lights.push(light);
            // Visual helpers to indicate light positions
            this.add(new THREE.PointLightHelper(light, 0.5, 0xff9900));
        }
        const ambientLight = new THREE.AmbientLight(0x404040); // soft white light
        this.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        this.add(directionalLight);
        // add to scene
        const submergedObject = (0, submergedObject_1.getSubmergedObject)();
        this.add(submergedObject);
        directionalLight.target = submergedObject;
        const groundGeo = new THREE.PlaneGeometry(1000, 1000, 512, 512);
        const sliderHorizontalRepeat = 5;
        const sliderVerticalRepeat = 5;
        let disMap = new THREE.TextureLoader()
            .setPath('../heightmaps/')
            .load('testHeightMap.png');
        disMap.wrapS = disMap.wrapT = THREE.RepeatWrapping;
        disMap.repeat.set(sliderHorizontalRepeat, sliderVerticalRepeat);
        const groundMat = new THREE.MeshStandardMaterial({
            color: 0xff0000,
            wireframe: false,
            displacementMap: disMap,
            displacementScale: 2,
        });
        const groundMesh = new THREE.Mesh(groundGeo, groundMat);
        groundMesh.rotation.x = -Math.PI / 2;
        groundMesh.position.y = -0.5;
        this.add(groundMesh);
        // setup Debugger
        if (debug) {
            this.debugger = new dat_gui_1.GUI();
            // Debug group with all lights in it.
            const lightGroup = this.debugger.addFolder('Lights');
            for (let i = 0; i < this.lights.length; i++) {
                lightGroup.add(this.lights[i], 'visible', true);
            }
            lightGroup.open();
            // Add the submergedObject with some properties
            const submergedObjectGroup = this.debugger.addFolder('submergedObject');
            submergedObjectGroup.add(submergedObject.position, 'x', -10, 10);
            submergedObjectGroup.add(submergedObject.position, 'y', 0.5, 10);
            submergedObjectGroup.add(submergedObject.position, 'z', -10, 10);
            submergedObjectGroup
                .add(submergedObject.rotation, 'y', 0, Math.PI * 2)
                .name('rot');
            submergedObjectGroup.open();
            // Add camera to debugger
            const cameraGroup = this.debugger.addFolder('Camera');
            cameraGroup.add(this.camera, 'fov', 20, 80);
            cameraGroup.add(this.camera, 'zoom', 0, 1);
            cameraGroup.open();
            // const directionalLightGroup = this.debugger.addFolder('DirLight')
            // directionalLightGroup.add(directionalLight.target, 'x', -10, 10)
            // directionalLightGroup.add(directionalLight.target, 'x', -10, 10)
            // directionalLightGroup.add(directionalLight.target, 'x', -10, 10)
        }
    }
    /**
     * Given a ThreeJS camera and renderer, resizes the scene if the
     * browser window is resized.
     * @param camera - a ThreeJS PerspectiveCamera object.
     * @param renderer - a subclass of a ThreeJS Renderer object.
     */
    static addWindowResizing(camera, renderer) {
        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize() {
            // uses the global window widths and height
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }
    }
}
exports.default = BasicScene;
//# sourceMappingURL=basicScene.js.map