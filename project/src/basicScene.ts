import * as THREE from 'three'
import { GUI } from 'dat.gui'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { placeSubmergedObjects } from './submergedObject'
import {
  PlaneGeometry,
  MeshStandardMaterial,
  DirectionalLight,
  Scene,
  TextureLoader,
} from 'three'
import { createGroundFromHeightmap } from './createGround'
import { createPointLights } from './lights/pointLights'
import { createAmbientLights } from './lights/ambientLights'
import { createDirectionalLights } from './lights/directionalLights'
import { Water } from 'three/examples/jsm/objects/Water2'
// import { createGroundFromHeightmap } from './createGround'
/**
 * A class to set up some basic scene elements to minimize code in the
 * main execution file.
 */
export default class BasicScene extends THREE.Scene {
  // A dat.gui class debugger that is added by default
  debugger: GUI = null
  // Setups a scene camera
  camera: THREE.PerspectiveCamera = null
  // setup renderer
  renderer: THREE.WebGLRenderer = null
  // setup Orbitals
  orbitals: OrbitControls = null

  // Holds the lights for easy reference
  lights: Array<THREE.Light> = []
  // Number of PointLight objects around origin
  lightCount: number = 6
  // Distance above ground place
  lightDistance: number = 30

  // Get some basic params
  width = window.innerWidth
  height = window.innerHeight

  groundMesh: THREE.Mesh<PlaneGeometry, MeshStandardMaterial> = null

  amountOfObjects: number = 5

  /**
   * Initializes the scene by adding lights, and the geometry
   */
  initialize(debug: boolean = true, addGridHelper: boolean = true) {
    // setup camera
    this.camera = new THREE.PerspectiveCamera(
      35,
      this.width / this.height,
      0.1,
      1000,
    )
    this.camera.position.z = 200
    this.camera.position.y = 120
    this.camera.position.x = 120

    this.background = new THREE.CubeTextureLoader()
      .setPath('../skybox/')
      .load([
        'uw_ft.jpg',
        'uw_bk.jpg',
        'uw_up.jpg',
        'uw_dn.jpg',
        'uw_rt.jpg',
        'uw_lf.jpg',
      ])

    // setup renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas: document.getElementById('app') as HTMLCanvasElement,
      alpha: true,
    })
    this.renderer.setSize(this.width, this.height)

    // add window resizing
    BasicScene.addWindowResizing(this.camera, this.renderer)

    // sets up the camera's orbital controls
    this.orbitals = new OrbitControls(this.camera, this.renderer.domElement)

    // Adds an origin-centered grid for visual reference
    if (addGridHelper) {
      // Adds a grid
      this.add(new THREE.GridHelper(10, 10, 'red'))
      // Adds an axis-helper
      this.add(new THREE.AxesHelper(3))
    }
    // set the background color
    // this.background = new THREE.Color(0xefefef)

    // create the lights
    this.lights = createPointLights(
      this,
      this.lightCount,
      this.lightDistance,
      this.lights,
    )

    const ambientLight = createAmbientLights(this)

    const directionalLight = createDirectionalLights(this)

    // add to scene
    const submergedObjects = placeSubmergedObjects()
    submergedObjects.forEach((submergedObject) => {
      this.add(submergedObject)
    })

    this.groundMesh = createGroundFromHeightmap()
    this.add(this.groundMesh)

    const waterGeometry = new THREE.PlaneGeometry(300, 300)

    const textureLoader = new THREE.TextureLoader()
    const flowMap = textureLoader.load('../flowmap/Water_1_M_Flow.jpg')

    const water = new Water(waterGeometry, {
      scale: 2,
      flowMap: flowMap,
    })

    water.position.y = 70
    water.rotation.x = -Math.PI / 2
    this.add(water)

    // setup Debugger
    if (debug) {
      this.debugger = new GUI()
      // Debug group with all lights in it.
      const lightGroup = this.debugger.addFolder('Lights')
      for (let i = 0; i < this.lights.length; i++) {
        lightGroup.add(this.lights[i], 'visible', false)
      }
      lightGroup.add(ambientLight, 'visible', true).name('visible - ambient')
      lightGroup.add(directionalLight, 'visible', false).name('visible - dir')

      lightGroup.open()

      // const waterGroup = this.debugger.addFolder('Water')
      // waterGroup.add(water, 'scale')

      // Add the submergedObjects with some properties
      for (let i = 0; i < submergedObjects.length; i++) {
        const submergedObjectGroup = this.debugger.addFolder(
          'SubmergedObject ' + i,
        )
        submergedObjectGroup.add(submergedObjects[i].position, 'x', -75, 75)
        submergedObjectGroup.add(submergedObjects[i].position, 'y', 0.5, 100)
        submergedObjectGroup.add(submergedObjects[i].position, 'z', -75, 75)
        submergedObjectGroup
          .add(submergedObjects[i].rotation, 'y', 0, Math.PI * 2)
          .name('rot')
      }
      // Add camera to debugger
      const cameraGroup = this.debugger.addFolder('Camera')
      cameraGroup.add(this.camera, 'fov', 20, 80)
      cameraGroup.add(this.camera, 'zoom', 0, 1)
      cameraGroup.open()
    }
  }

  /**
   * Given a ThreeJS camera and renderer, resizes the scene if the
   * browser window is resized.
   * @param camera - a ThreeJS PerspectiveCamera object.
   * @param renderer - a subclass of a ThreeJS Renderer object.
   */
  static addWindowResizing(
    camera: THREE.PerspectiveCamera,
    renderer: THREE.Renderer,
  ) {
    window.addEventListener('resize', onWindowResize, false)
    function onWindowResize() {
      // uses the global window widths and height
      camera.aspect = window.innerWidth / window.innerHeight
      camera.updateProjectionMatrix()
      renderer.setSize(window.innerWidth, window.innerHeight)
    }
  }
}
