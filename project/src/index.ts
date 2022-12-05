import basicScene from './basicScene'
// sets up the scene
let scene = new basicScene()
scene.initialize()
// loops updates
function loop() {
  scene.camera.updateProjectionMatrix()
  scene.renderer.render(scene, scene.camera)
  scene.orbitals.update()

  requestAnimationFrame(loop)
}
// runs a continuous loop
loop()
