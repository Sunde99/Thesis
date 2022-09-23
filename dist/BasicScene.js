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
const createGround_1 = require("./createGround");
const pointLights_1 = require("./lights/pointLights");
const ambientLights_1 = require("./lights/ambientLights");
const directionalLights_1 = require("./lights/directionalLights");
const Water2_1 = require("three/examples/jsm/objects/Water2");
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
        this.lightDistance = 30;
        // Get some basic params
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.groundMesh = null;
        this.amountOfObjects = 5;
    }
    /**
     * Initializes the scene by adding lights, and the geometry
     */
    initialize(debug = true, addGridHelper = true) {
        // setup camera
        this.camera = new THREE.PerspectiveCamera(35, this.width / this.height, 0.1, 1000);
        this.camera.position.z = 200;
        this.camera.position.y = 120;
        this.camera.position.x = 120;
        this.background = new THREE.CubeTextureLoader().setPath('../skybox/').load([
            // 'uw_ft.jpg',
            // 'uw_bk.jpg',
            // 'uw_up.jpg',
            // 'uw_dn.jpg',
            // 'uw_rt.jpg',
            // 'uw_lf.jpg',
            'TinesNeck.jpg',
            'TinesNeck.jpg',
            'TinesNeck.jpg',
            'TinesNeck.jpg',
            'TinesNeck.jpg',
            'TinesNeck.jpg',
        ]);
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
        // this.background = new THREE.Color(0xefefef)
        // create the lights
        this.lights = (0, pointLights_1.createPointLights)(this, this.lightCount, this.lightDistance, this.lights);
        const ambientLight = (0, ambientLights_1.createAmbientLights)(this);
        const directionalLight = (0, directionalLights_1.createDirectionalLights)(this);
        // add to scene
        const submergedObjects = (0, submergedObject_1.placeSubmergedObjects)();
        submergedObjects.forEach((submergedObject) => {
            this.add(submergedObject);
        });
        this.groundMesh = (0, createGround_1.createGroundFromHeightmap)();
        this.add(this.groundMesh);
        // Wa'a
        const waterGeometry = new THREE.PlaneGeometry(300, 300);
        const textureLoader = new THREE.TextureLoader();
        const flowMap = textureLoader.load('../flowmap/Water_1_M_Flow.jpg');
        const water = new Water2_1.Water(waterGeometry, {
            scale: 2,
            flowMap: flowMap,
        });
        water.position.y = 70;
        water.rotation.x = -Math.PI / 2;
        this.add(water);
        // Wa'a
        // setup Debugger
        if (debug) {
            this.debugger = new dat_gui_1.GUI();
            // Debug group with all lights in it.
            const lightGroup = this.debugger.addFolder('Lights');
            for (let i = 0; i < this.lights.length; i++) {
                lightGroup.add(this.lights[i], 'visible', false);
            }
            lightGroup.add(ambientLight, 'visible', true).name('visible - ambient');
            lightGroup.add(directionalLight, 'visible', false).name('visible - dir');
            lightGroup.open();
            // Add the submergedObjects with some properties
            for (let i = 0; i < submergedObjects.length; i++) {
                const submergedObjectGroup = this.debugger.addFolder('submergedObject ' + i);
                submergedObjectGroup.add(submergedObjects[i].position, 'x', -75, 75);
                submergedObjectGroup.add(submergedObjects[i].position, 'y', 0.5, 100);
                submergedObjectGroup.add(submergedObjects[i].position, 'z', -75, 75);
                submergedObjectGroup
                    .add(submergedObjects[i].rotation, 'y', 0, Math.PI * 2)
                    .name('rot');
            }
            // Add camera to debugger
            const cameraGroup = this.debugger.addFolder('Camera');
            cameraGroup.add(this.camera, 'fov', 20, 80);
            cameraGroup.add(this.camera, 'zoom', 0, 1);
            cameraGroup.open();
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