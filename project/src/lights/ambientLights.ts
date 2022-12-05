import * as THREE from 'three'

export const createAmbientLights = (scene: THREE.Scene) => {
  const ambientLight = new THREE.AmbientLight(0x404040) // soft white light
  ambientLight.intensity = 0.1
  scene.add(ambientLight)
  return ambientLight
}
